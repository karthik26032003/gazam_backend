from helpers.whatsapp_client import send_button, send_list, send_text
from helpers.session import set_session, update_session

WELCOME_MSG = (
    "Welcome to Gazam Associates! 🏠\n\n"
    "India's trusted real estate platform.\n\n"
    "Please select your preferred language:"
)

MAIN_MENU_BODY = "How can we help you today?\n\nChoose an option from the menu below 👇"


async def send_language_selection(phone: str):
    await send_button(
        to=phone,
        body=WELCOME_MSG,
        buttons=["English", "తెలుగు", "हिंदी"],
    )
    set_session(phone, {"flow": "welcome", "step": "language_select"})


async def send_main_menu(phone: str):
    sections = [
        {
            "title": "Our Services",
            "rows": [
                {
                    "id": "menu_find",
                    "title": "🔍 Find Property",
                    "description": "Browse listings by location, budget & type"
                },
                {
                    "id": "menu_post",
                    "title": "📋 Post Property",
                    "description": "List your property for sale or rent"
                },
                {
                    "id": "menu_loan",
                    "title": "💰 Loan Services",
                    "description": "Home loans, EMI calculator & more"
                },
                {
                    "id": "menu_agent",
                    "title": "🤝 Talk to Agent",
                    "description": "Connect with a verified real estate agent"
                },
                {
                    "id": "menu_support",
                    "title": "💬 Support",
                    "description": "Help & frequently asked questions"
                },
            ]
        }
    ]
    await send_list(
        to=phone,
        body=MAIN_MENU_BODY,
        button_label="View Options",
        sections=sections,
        header="Gazam Associates"
    )
    update_session(phone, {"flow": "main_menu", "step": "menu"})


async def handle_language_selection(phone: str, button_id: str):
    language_map = {
        "btn_0": "en",
        "btn_1": "te",
        "btn_2": "hi",
    }
    language = language_map.get(button_id, "en")
    update_session(phone, {"language": language})
    await send_main_menu(phone)


async def handle_menu_selection(phone: str, row_id: str):
    # TODO: Route to actual flow handlers (Phase 4+)
    await send_text(phone, "✅ Coming soon! We're building this flow.")
