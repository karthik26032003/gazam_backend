from helpers.session import get_session
from routers.flows.main_menu import (
    send_language_selection,
    send_main_menu,
    handle_language_selection,
    handle_menu_selection,
)
from routers.flows.buyer import (
    start_buyer_flow,
    handle_property_type as buyer_handle_property_type,
    handle_sub_type as buyer_handle_sub_type,
    handle_location as buyer_handle_location,
    handle_budget,
    handle_enquiry,
)
from routers.flows.seller import (
    start_seller_flow,
    handle_property_type as seller_handle_property_type,
    handle_sub_type as seller_handle_sub_type,
    handle_location as seller_handle_location,
    handle_price,
    handle_description,
)


async def route_message(phone: str, message: dict):
    session = get_session(phone)
    flow = session.get("flow")
    step = session.get("step")
    message_type = message.get("type")

    # New user or expired session
    if not flow:
        await send_language_selection(phone)
        return

    # ── Free text input ───────────────────────────────────────────────────────
    if message_type == "text":
        text = message.get("text", {}).get("body", "").strip()

        if flow == "seller":
            if step == "price":
                await handle_price(phone, text)
                return
            if step == "description":
                await handle_description(phone, text)
                return

        await send_main_menu(phone)
        return

    # ── Interactive messages ──────────────────────────────────────────────────
    if message_type == "interactive":
        interactive = message.get("interactive", {})
        interactive_type = interactive.get("type")

        # ── Button replies ────────────────────────────────────────────────────
        if interactive_type == "button_reply":
            button_id = interactive["button_reply"]["id"]

            if flow == "welcome" and step == "language_select":
                await handle_language_selection(phone, button_id)
                return

            if flow == "buyer":
                if step == "property_type":
                    await buyer_handle_property_type(phone, button_id)
                    return
                if step == "post_enquiry":
                    if button_id == "btn_0":
                        await send_main_menu(phone)
                    elif button_id == "btn_1":
                        await start_buyer_flow(phone)
                    return

            if flow == "seller":
                if step == "property_type":
                    await seller_handle_property_type(phone, button_id)
                    return
                if step == "post_listing":
                    if button_id == "btn_0":
                        await send_main_menu(phone)
                    elif button_id == "btn_1":
                        await start_seller_flow(phone)
                    return

        # ── List replies ──────────────────────────────────────────────────────
        elif interactive_type == "list_reply":
            row_id = interactive["list_reply"]["id"]
            row_title = interactive["list_reply"]["title"]

            if flow == "main_menu" and step == "menu":
                if row_id == "menu_find":
                    await start_buyer_flow(phone)
                elif row_id == "menu_post":
                    await start_seller_flow(phone)
                else:
                    await handle_menu_selection(phone, row_id)
                return

            if flow == "buyer":
                if step == "sub_type":
                    await buyer_handle_sub_type(phone, row_id, row_title)
                    return
                if step == "location":
                    await buyer_handle_location(phone, row_id, row_title)
                    return
                if step == "budget":
                    await handle_budget(phone, row_id, row_title)
                    return
                if step == "enquiry":
                    await handle_enquiry(phone, row_id, row_title)
                    return

            if flow == "seller":
                if step == "sub_type":
                    await seller_handle_sub_type(phone, row_id, row_title)
                    return
                if step == "location":
                    await seller_handle_location(phone, row_id, row_title)
                    return

    # Fallback — show main menu
    await send_main_menu(phone)
