import httpx
import logging
from config import settings

logger = logging.getLogger(__name__)

WA_API_URL = f"https://graph.facebook.com/v21.0/{settings.phone_number_id}/messages"
HEADERS = {
    "Authorization": f"Bearer {settings.access_token}",
    "Content-Type": "application/json"
}


async def send_message(payload: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(WA_API_URL, json=payload, headers=HEADERS)
        data = response.json()
        if response.status_code != 200:
            logger.error(f"WhatsApp API error: {data}")
        else:
            logger.info(f"Message sent: {data.get('messages', [{}])[0].get('id')}")
        return data


async def send_text(to: str, body: str):
    from helpers.message_types import text_msg
    return await send_message(text_msg(to, body))


async def send_button(to: str, body: str, buttons: list[str], header: str = None, footer: str = None):
    from helpers.message_types import button_msg
    return await send_message(button_msg(to, body, buttons, header, footer))


async def send_list(to: str, body: str, button_label: str, sections: list[dict], header: str = None, footer: str = None):
    from helpers.message_types import list_msg
    return await send_message(list_msg(to, body, button_label, sections, header, footer))


async def send_template(to: str, template_name: str, language_code: str = "en_US", components: list = None):
    from helpers.message_types import template_msg
    return await send_message(template_msg(to, template_name, language_code, components))


def mark_as_read(wa_message_id: str):
    import httpx
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": wa_message_id
    }
    with httpx.Client() as client:
        client.post(WA_API_URL, json=payload, headers=HEADERS)
