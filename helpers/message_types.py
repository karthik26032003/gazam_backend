def text_msg(to: str, body: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body}
    }


def button_msg(to: str, body: str, buttons: list[str], header: str = None, footer: str = None) -> dict:
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": f"btn_{i}", "title": btn}}
                    for i, btn in enumerate(buttons)
                ]
            }
        }
    }
    if header:
        payload["interactive"]["header"] = {"type": "text", "text": header}
    if footer:
        payload["interactive"]["footer"] = {"text": footer}
    return payload


def list_msg(to: str, body: str, button_label: str, sections: list[dict], header: str = None, footer: str = None) -> dict:
    """
    sections format:
    [
      {
        "title": "Section Title",
        "rows": [
          {"id": "row_id", "title": "Row Title", "description": "Optional desc"}
        ]
      }
    ]
    """
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body},
            "action": {
                "button": button_label,
                "sections": sections
            }
        }
    }
    if header:
        payload["interactive"]["header"] = {"type": "text", "text": header}
    if footer:
        payload["interactive"]["footer"] = {"text": footer}
    return payload


def template_msg(to: str, template_name: str, language_code: str = "en_US", components: list = None) -> dict:
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code}
        }
    }
    if components:
        payload["template"]["components"] = components
    return payload
