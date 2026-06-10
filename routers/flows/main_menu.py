from helpers.whatsapp_client import send_button, send_list, send_text
from helpers.session import set_session, update_session

WELCOME_MSG = (
    "👋 Welcome to *Gazam Associates!*\n\n"
    "🏠 Hyderabad's trusted real estate platform — buying, selling, renting & loans, all in one place.\n\n"
    "─────────────────────\n"
    "🌐 Please select your language to get started:"
)

MAIN_MENU_BODY = (
    "Great! What are you looking for today? 😊\n\n"
    "We're here to help you with properties, loans & more.\n\n"
    "👇 Tap *View Options* to explore:"
)


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
                    "description": "Flats, villas, plots & more near you"
                },
                {
                    "id": "menu_post",
                    "title": "📋 Post Property",
                    "description": "Sell or rent your property for free"
                },
                {
                    "id": "menu_loan",
                    "title": "💰 Loan Services",
                    "description": "Best rates on home & property loans"
                },
                {
                    "id": "menu_agent",
                    "title": "🤝 Talk to Agent",
                    "description": "Get expert help from a verified agent"
                },
                {
                    "id": "menu_support",
                    "title": "💬 Support",
                    "description": "Questions? We're here to help 24/7"
                },
            ]
        }
    ]
    await send_list(
        to=phone,
        body=MAIN_MENU_BODY,
        button_label="🏠 Explore Now",
        sections=sections,
        header="🏢 Gazam Associates"
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
