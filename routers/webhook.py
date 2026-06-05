import hashlib
import hmac
import json
import logging

from fastapi import APIRouter, Request, Response, HTTPException, Query
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.get("")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """Meta webhook verification handshake."""
    if hub_mode == "subscribe" and hub_verify_token == settings.verify_token:
        logger.info("Webhook verified successfully")
        return Response(content=hub_challenge, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("")
async def receive_webhook(request: Request):
    """Receive incoming WhatsApp messages and status updates."""
    # Verify request signature
    signature = request.headers.get("x-hub-signature-256", "")
    body = await request.body()

    if not _verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(body)
    logger.info(f"Webhook received: {json.dumps(payload, indent=2)}")

    # Process each entry
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})

            # Incoming messages
            for message in value.get("messages", []):
                await _handle_message(message, value.get("metadata", {}))

            # Message status updates (sent/delivered/read)
            for status in value.get("statuses", []):
                await _handle_status_update(status)

    return {"status": "ok"}


async def _handle_message(message: dict, metadata: dict):
    """Route incoming message to the correct flow handler."""
    phone_number = message.get("from")
    message_type = message.get("type")
    wa_message_id = message.get("id")

    logger.info(f"Message from {phone_number} | type: {message_type} | id: {wa_message_id}")

    # Mark message as read
    from helpers.whatsapp_client import mark_as_read, send_text
    mark_as_read(wa_message_id)

    # TODO: Route to flow handler (Phase 3)
    # Temporary echo reply for testing Phase 2
    await send_text(phone_number, f"✅ Bot received your message! (Phase 2 test)")


async def _handle_status_update(status: dict):
    """Handle delivery/read receipts."""
    wa_message_id = status.get("id")
    status_value = status.get("status")
    recipient = status.get("recipient_id")

    logger.info(f"Status update: {wa_message_id} → {status_value} for {recipient}")

    # TODO: Update wa_messages table status (Phase 2+)


def _verify_signature(body: bytes, signature: str) -> bool:
    """Verify Meta webhook signature using HMAC-SHA256."""
    if not signature.startswith("sha256="):
        return False
    expected = hmac.new(
        settings.app_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
