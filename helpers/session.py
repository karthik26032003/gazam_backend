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
