from helpers.whatsapp_client import send_button, send_text
from helpers.session import update_session, get_session

LOAN_TYPES = {
    "btn_0": "Home Loan",
    "btn_1": "Loan Against Property",
    "btn_2": "Build / Construction Loan",
}

EMPLOYMENT_TYPES = {
    "btn_0": "Salaried",
    "btn_1": "Self-Employed",
    "btn_2": "Business Owner",
}


async def start_loan_flow(phone: str):
    await send_button(
        to=phone,
        body=(
            "Great! Let's help you get the *best loan deal* 💰\n\n"
            "We work with top banks and NBFCs to get you:\n"
            "• Lowest interest rates\n"
            "• Fast approvals\n"
            "• Minimum paperwork\n\n"
            "What type of loan are you looking for?"
        ),
        buttons=["🏠 Home Loan", "🏦 Against Property", "🏗 Build Loan"],
        header="💰 Loan Services"
    )
    update_session(phone, {"flow": "loan", "step": "loan_type"})


async def handle_loan_type(phone: str, button_id: str):
    loan_type = LOAN_TYPES.get(button_id, "Home Loan")
    update_session(phone, {"loan_type": loan_type})

    await send_text(
        phone,
        (
            f"Perfect! *{loan_type}* selected 👍\n\n"
            "💵 How much loan amount are you looking for?\n\n"
            "Just type the amount — for example:\n"
            "• _40 lakhs_\n"
            "• _1.5 crore_\n"
            "• _75,00,000_"
        )
    )
    update_session(phone, {"step": "loan_amount"})


async def handle_loan_amount(phone: str, text: str):
    update_session(phone, {"loan_amount": text})

    await send_button(
        to=phone,
        body=(
            f"Got it! *{text}* noted 💰\n\n"
            "👔 What is your employment type?"
        ),
        buttons=["💼 Salaried", "👔 Self-Employed", "🏢 Business Owner"],
        header="Employment Details"
    )
    update_session(phone, {"step": "employment_type"})


async def handle_employment_type(phone: str, button_id: str):
    emp_type = EMPLOYMENT_TYPES.get(button_id, "Salaried")
    update_session(phone, {"employment_type": emp_type})

    await send_text(
        phone,
        (
            f"Got it! *{emp_type}* 👍\n\n"
            "📊 What is your *monthly income?*\n\n"
            "Just type it — for example:\n"
            "• _80,000_\n"
            "• _1.5 lakhs_\n"
            "• _2,00,000_"
        )
    )
    update_session(phone, {"step": "monthly_income"})


async def handle_monthly_income(phone: str, text: str):
    update_session(phone, {"monthly_income": text})
    session = get_session(phone)
    _save_loan_lead(phone, session)

    loan_type = session.get("loan_type", "")
    loan_amount = session.get("loan_amount", "")
    emp_type = session.get("employment_type", "")

    await send_button(
        to=phone,
        body=(
            "✅ *Loan enquiry submitted!*\n\n"
            f"🏦 *Loan Type:* {loan_type}\n"
            f"💵 *Amount:* {loan_amount}\n"
            f"👔 *Employment:* {emp_type}\n\n"
            "Our loan expert will call you within *4 working hours* 📞\n\n"
            "We'll find you the *best rate* available!"
        ),
        buttons=["🏠 Main Menu", "📞 Talk to Agent"],
        header="🎉 Enquiry Received!"
    )
    update_session(phone, {"step": "post_loan"})


def _save_loan_lead(phone: str, session: dict):
    from database import SessionLocal
    from models.db import WALead, LeadType

    db = SessionLocal()
    try:
        lead = WALead(
            phone_number=phone,
            lead_type=LeadType.loan,
            data={
                "loan_type": session.get("loan_type"),
                "loan_amount": session.get("loan_amount"),
                "employment_type": session.get("employment_type"),
                "monthly_income": session.get("monthly_income"),
            }
        )
        db.add(lead)
        db.commit()
    finally:
        db.close()
