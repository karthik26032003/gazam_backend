from helpers.whatsapp_client import send_button, send_text
from helpers.session import update_session, get_session

AGENT_HELP_TYPES = {
    "btn_0": "Buy Property",
    "btn_1": "Sell Property",
    "btn_2": "Loan / Finance",
}


async def start_agent_flow(phone: str):
    await send_button(
        to=phone,
        body=(
            "Sure! Our verified agents are ready to help you 🤝\n\n"
            "They'll call you directly and guide you through everything.\n\n"
            "What do you need help with?"
        ),
        buttons=["🏠 Buy Property", "📋 Sell Property", "💰 Loan / Finance"],
        header="🤝 Talk to an Agent"
    )
    update_session(phone, {"flow": "agent", "step": "help_type"})


async def handle_help_type(phone: str, button_id: str):
    help_type = AGENT_HELP_TYPES.get(button_id, "General")
    update_session(phone, {"help_type": help_type})

    await send_text(
        phone,
        (
            f"Got it! Our agent will help you with *{help_type}* 👍\n\n"
            "📝 Give us a *brief note* about what you're looking for.\n\n"
            "_For example:_\n"
            "• _3BHK flat in Gachibowli under 80 lakhs_\n"
            "• _Want to sell my 2BHK in Miyapur_\n"
            "• _Need home loan of 50 lakhs, salaried_"
        )
    )
    update_session(phone, {"step": "agent_note"})


async def handle_agent_note(phone: str, text: str):
    update_session(phone, {"agent_note": text})
    session = get_session(phone)
    _save_agent_request(phone, session)

    help_type = session.get("help_type", "")

    await send_button(
        to=phone,
        body=(
            "✅ *Request received!*\n\n"
            f"📌 *Topic:* {help_type}\n\n"
            "A verified Gazam agent will *call you within 2 hours* 📞\n\n"
            "Is there anything else we can help you with?"
        ),
        buttons=["🏠 Main Menu", "💬 Support"],
        header="🎉 Agent Assigned!"
    )
    update_session(phone, {"step": "post_agent"})


def _save_agent_request(phone: str, session: dict):
    from database import SessionLocal
    from models.db import WALead, LeadType

    db = SessionLocal()
    try:
        lead = WALead(
            phone_number=phone,
            lead_type=LeadType.agent,
            data={
                "help_type": session.get("help_type"),
                "note": session.get("agent_note"),
            }
        )
        db.add(lead)
        db.commit()
    finally:
        db.close()
