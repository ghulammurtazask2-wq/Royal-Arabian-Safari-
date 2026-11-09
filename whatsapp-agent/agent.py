"""
Claude-powered WhatsApp agent for Royal Arabian Safari.
Handles pricing queries, booking collection, and confirmation.
"""

import json
import os
import re
from datetime import datetime

import anthropic

from prices import SERVICES, BOOKING_POLICIES, QUICK_PRICE_SUMMARY, WEBSITE

_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = f"""You are the booking assistant for Royal Arabian Safari (arabiansafariroyal.com).
You answer customer WhatsApp messages in a warm, concise, professional tone.

━━ YOUR ROLE ━━
1. Answer any question about tours, prices or logistics.
2. When a customer is ready to book, collect these details one by one:
   - Full name
   - Tour/service they want
   - Date (DD/MM/YYYY)
   - Number of guests (adults + children separately)
   - Hotel name or pickup address in Dubai / Abu Dhabi
   - Contact number (if different from WhatsApp)
3. Once ALL 6 details are collected, output a JSON block wrapped in <BOOKING> ... </BOOKING> tags
   containing: name, service, date, adults, children, pickup, phone.
   Example:
   <BOOKING>{{"name":"Ahmed Ali","service":"Dubai City Tour","date":"15/12/2026","adults":4,"children":2,"pickup":"Atlantis The Palm, Dubai","phone":"+971501234567"}}</BOOKING>
   After that, send a human-readable confirmation summary to the customer.
4. If the customer asks for prices or a price list, share the summary below.
5. Never invent prices. Only quote from the list below.
6. Reply in the same language the customer uses (Arabic or English).
   If they mix languages, prefer English for prices/numbers but match their greeting.
7. Keep messages SHORT — max 5 lines per message on WhatsApp.
   For price lists, use bullet formatting with emoji.

━━ BOOKING POLICIES ━━
{BOOKING_POLICIES}

━━ ALL SERVICES & PRICES ━━
{json.dumps(SERVICES, indent=2, ensure_ascii=False)}

━━ QUICK PRICE SUMMARY (use when customer asks for prices) ━━
{QUICK_PRICE_SUMMARY}

━━ IMPORTANT RULES ━━
- Do NOT make up prices or services not in the list above.
- If you don't know something, say "Let me check that for you — please WhatsApp +971 58 228 2683 directly."
- Never promise availability — that is confirmed after the owner reviews the booking.
- After collecting all booking info, ALWAYS output the <BOOKING>...</BOOKING> JSON before the confirmation text.
- Today's date: {datetime.now().strftime("%d/%m/%Y")}
"""


def get_reply(session: dict, incoming_message: str) -> tuple[str, dict | None]:
    """
    Process incoming message, update session history, return (reply_text, booking_data_or_None).
    """
    # Append user message
    session["history"].append({"role": "user", "content": incoming_message})

    # Build messages list (keep last 20 turns to stay within context)
    messages = session["history"][-20:]

    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    reply_text = response.content[0].text

    # Append assistant reply to history
    session["history"].append({"role": "assistant", "content": reply_text})

    # Check for booking JSON
    booking_data = _extract_booking(reply_text)

    # Strip the JSON tag from the customer-facing reply
    clean_reply = re.sub(r"<BOOKING>.*?</BOOKING>", "", reply_text, flags=re.DOTALL).strip()

    return clean_reply, booking_data


def _extract_booking(text: str) -> dict | None:
    match = re.search(r"<BOOKING>(.*?)</BOOKING>", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1).strip())
    except json.JSONDecodeError:
        return None
