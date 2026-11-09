"""
In-memory conversation sessions with auto-expiry (24 hours).
In production, replace with Redis or a database.
"""

import time
from typing import Optional

_sessions: dict[str, dict] = {}
_SESSION_TTL = 86400  # 24 hours


def get(phone: str) -> dict:
    """Return existing session or create a fresh one."""
    _cleanup()
    if phone not in _sessions:
        _sessions[phone] = {
            "phone": phone,
            "history": [],       # list of {"role": "user"|"assistant", "content": str}
            "booking": {},       # collected booking fields
            "stage": "chat",     # "chat" | "collecting" | "confirmed"
            "created_at": time.time(),
            "updated_at": time.time(),
        }
    _sessions[phone]["updated_at"] = time.time()
    return _sessions[phone]


def save(phone: str, session: dict) -> None:
    session["updated_at"] = time.time()
    _sessions[phone] = session


def clear(phone: str) -> None:
    _sessions.pop(phone, None)


def _cleanup() -> None:
    now = time.time()
    stale = [k for k, v in _sessions.items() if now - v["updated_at"] > _SESSION_TTL]
    for k in stale:
        del _sessions[k]
