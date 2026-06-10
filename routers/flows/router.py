from helpers.session import get_session
from routers.flows.main_menu import (
    send_language_selection,
    send_main_menu,
    handle_language_selection,
    handle_menu_selection,
)


async def route_message(phone: str, message: dict):
    session = get_session(phone)
    flow = session.get("flow")
    step = session.get("step")
    message_type = message.get("type")

    # New user or expired session → send welcome + language selection
    if not flow:
        await send_language_selection(phone)
        return

    if message_type == "interactive":
        interactive = message.get("interactive", {})
        interactive_type = interactive.get("type")

        if interactive_type == "button_reply":
            button_id = interactive["button_reply"]["id"]

            if flow == "welcome" and step == "language_select":
                await handle_language_selection(phone, button_id)
                return

        elif interactive_type == "list_reply":
            row_id = interactive["list_reply"]["id"]

            if flow == "main_menu" and step == "menu":
                await handle_menu_selection(phone, row_id)
                return

    # Fallback — any unrecognised message → show main menu again
    await send_main_menu(phone)
