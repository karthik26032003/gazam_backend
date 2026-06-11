from helpers.whatsapp_client import send_button, send_text
from helpers.session import update_session, get_session


async def start_support_flow(phone: str):
    await send_text(
        phone,
        (
            "Hi! 👋 We're here to help you 24/7 💬\n\n"
            "Please *describe your issue or question* and our support team will get back to you shortly.\n\n"
            "_For example:_\n"
            "• _I registered interest in a property but got no call_\n"
            "• _I want to update my listing details_\n"
            "• _I have a question about the loan process_"
        )
    )
    update_session(phone, {"flow": "support", "step": "issue"})


async def handle_issue(phone: str, text: str):
    update_session(phone, {"issue": text})
    _save_support_ticket(phone, text)

    await send_button(
        to=phone,
        body=(
            "✅ *Support ticket raised!*\n\n"
            "Our team will respond within *4 working hours* 📞\n\n"
            "Thank you for reaching out to Gazam Associates 🙏"
        ),
        buttons=["🏠 Main Menu", "➕ New Issue"],
        header="💬 We Got Your Message!"
    )
    update_session(phone, {"step": "post_support"})


def _save_support_ticket(phone: str, issue: str):
    from database import SessionLocal
    from models.db import WALead, LeadType

    db = SessionLocal()
    try:
        lead = WALead(
            phone_number=phone,
            lead_type=LeadType.support,
            data={"issue": issue}
        )
        db.add(lead)
        db.commit()
    finally:
        db.close()
