"""
Royal Arabian Safari — WhatsApp Agent
Flask webhook server for Meta WhatsApp Cloud API.

Endpoints:
  GET  /webhook  — Meta verification challenge
  POST /webhook  — Incoming messages
  GET  /health   — Health check
"""

import logging
import os

from flask import Flask, jsonify, request

import agent
import notifications
import sessions
import whatsapp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

app = Flask(__name__)

VERIFY_TOKEN = os.environ["WHATSAPP_VERIFY_TOKEN"]


# ── Health check ────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return jsonify({"status": "ok", "agent": "Royal Arabian Safari WhatsApp Bot"})


# ── Meta webhook verification ────────────────────────────────────────────────

@app.get("/webhook")
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        log.info("Webhook verified by Meta.")
        return challenge, 200

    log.warning("Webhook verification failed — wrong token.")
    return "Forbidden", 403


# ── Incoming messages ────────────────────────────────────────────────────────

@app.post("/webhook")
def receive():
    data = request.get_json(silent=True) or {}

    try:
        entries = data.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                _process_messages(value)
    except Exception as exc:
        log.exception("Unhandled error in webhook handler")
        return jsonify({"status": "error", "detail": str(exc)}), 500

    # Always return 200 so Meta doesn't retry
    return jsonify({"status": "ok"}), 200


def _process_messages(value: dict) -> None:
    messages = value.get("messages", [])
    for msg in messages:
        msg_type = msg.get("type")
        phone = msg.get("from")
        message_id = msg.get("id")

        if not phone or msg_type != "text":
            continue  # Skip non-text messages (images, stickers, etc.) for now

        text = msg["text"]["body"].strip()
        log.info("Incoming from %s: %s", phone, text[:80])

        # Mark as read (blue ticks)
        try:
            whatsapp.mark_read(message_id)
        except Exception:
            pass

        _handle_message(phone, text)


def _handle_message(phone: str, text: str) -> None:
    session = sessions.get(phone)

    try:
        reply, booking_data = agent.get_reply(session, text)
    except Exception as exc:
        log.exception("Agent error for %s", phone)
        notifications.notify_owner_error(phone, str(exc))
        whatsapp.send_text(
            phone,
            "Sorry, I'm having trouble right now. Please WhatsApp us directly at +971 58 228 2683 and we'll help you immediately! 🙏",
        )
        return

    sessions.save(phone, session)

    # Send the customer reply
    if reply:
        try:
            whatsapp.send_text(phone, reply)
            log.info("Replied to %s (%d chars)", phone, len(reply))
        except Exception as exc:
            log.error("Failed to send reply to %s: %s", phone, exc)

    # If a booking was completed, notify the owner
    if booking_data:
        log.info("BOOKING CONFIRMED for %s: %s", phone, booking_data)
        notifications.notify_owner_new_booking(booking_data, phone)
        session["stage"] = "confirmed"
        session["booking"] = booking_data
        sessions.save(phone, session)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    log.info("Starting Royal Arabian Safari WhatsApp Agent on port %d", port)
    app.run(host="0.0.0.0", port=port, debug=debug)
