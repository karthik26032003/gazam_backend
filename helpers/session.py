import json
from redis_client import redis_client

SESSION_TTL = 60 * 30  # 30 minutes


def get_session(phone: str) -> dict:
    data = redis_client.get(f"session:{phone}")
    return json.loads(data) if data else {}


def set_session(phone: str, data: dict):
    redis_client.setex(f"session:{phone}", SESSION_TTL, json.dumps(data))


def update_session(phone: str, updates: dict):
    session = get_session(phone)
    session.update(updates)
    set_session(phone, session)


def clear_session(phone: str):
    redis_client.delete(f"session:{phone}")


def get_flow(phone: str) -> str | None:
    return get_session(phone).get("flow")


def get_step(phone: str) -> str | None:
    return get_session(phone).get("step")


# ── Chat history for AI conversations ────────────────────────────────────────

HISTORY_TTL = 60 * 60  # 1 hour
HISTORY_MAX = 10        # keep last 10 messages (5 exchanges)


def get_chat_history(phone: str) -> list[dict]:
    data = redis_client.get(f"history:{phone}")
    return json.loads(data) if data else []


def append_chat_history(phone: str, role: str, content: str):
    history = get_chat_history(phone)
    history.append({"role": role, "content": content})
    if len(history) > HISTORY_MAX:
        history = history[-HISTORY_MAX:]
    redis_client.setex(f"history:{phone}", HISTORY_TTL, json.dumps(history))


def clear_chat_history(phone: str):
    redis_client.delete(f"history:{phone}")
