"""
WhatsApp Cloud API client (Meta's official API).
Docs: https://developers.facebook.com/docs/whatsapp/cloud-api
"""

import os
import requests

_PHONE_NUMBER_ID = os.environ["WHATSAPP_PHONE_NUMBER_ID"]
_ACCESS_TOKEN = os.environ["WHATSAPP_ACCESS_TOKEN"]
_API_VERSION = "v20.0"
_BASE_URL = f"https://graph.facebook.com/{_API_VERSION}/{_PHONE_NUMBER_ID}/messages"


def send_text(to: str, text: str) -> dict:
    """Send a plain text message."""
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text, "preview_url": False},
    }
    return _post(payload)


def send_template(to: str, template_name: str, language_code: str = "en_US") -> dict:
    """Send an approved template message (for 24-hour window re-engagement)."""
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
        },
    }
    return _post(payload)


def mark_read(message_id: str) -> None:
    """Mark an incoming message as read (shows double blue ticks)."""
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }
    _post(payload)


def _post(payload: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    resp = requests.post(_BASE_URL, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()
