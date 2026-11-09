"""
Owner notification system.
Sends a WhatsApp message to the owner when a booking is confirmed.
"""

import os
from datetime import datetime

import whatsapp

OWNER_NUMBER = os.environ.get("OWNER_WHATSAPP_NUMBER", "+971582282683")


def notify_owner_new_booking(booking: dict, customer_phone: str) -> None:
    """
    Send a WhatsApp notification to the owner with full booking details.
    booking keys: name, service, date, adults, children, pickup, phone
    """
    adults = booking.get("adults", "?")
    children = booking.get("children", 0)
    guests_line = f"{adults} adults" + (f" + {children} children" if children else "")

    message = (
        "🔔 *NEW BOOKING — Royal Arabian Safari*\n\n"
        f"👤 *Name:* {booking.get('name', '—')}\n"
        f"🏜️ *Tour:* {booking.get('service', '—')}\n"
        f"📅 *Date:* {booking.get('date', '—')}\n"
        f"👥 *Guests:* {guests_line}\n"
        f"🏨 *Pickup:* {booking.get('pickup', '—')}\n"
        f"📱 *Customer Phone:* {booking.get('phone') or customer_phone}\n"
        f"📲 *WhatsApp:* {customer_phone}\n\n"
        f"⏰ Received: {datetime.now().strftime('%d/%m/%Y %H:%M')} (server time)\n\n"
        "✅ Please confirm availability and reply to the customer."
    )

    try:
        whatsapp.send_text(OWNER_NUMBER, message)
        print(f"[notifications] Owner notified about booking for {booking.get('name')}")
    except Exception as exc:
        print(f"[notifications] ERROR sending owner notification: {exc}")


def notify_owner_error(customer_phone: str, error: str) -> None:
    """Alert owner about a processing error so they can follow up manually."""
    message = (
        f"⚠️ *Agent Error — Manual Follow-up Needed*\n\n"
        f"Customer: {customer_phone}\n"
        f"Error: {error}\n"
        f"Time: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    try:
        whatsapp.send_text(OWNER_NUMBER, message)
    except Exception as exc:
        print(f"[notifications] ERROR sending error notification: {exc}")
