"""
Local terminal test — chat with the agent without WhatsApp.
Run: python test_chat.py
"""

import sys
import os

# Use session's built-in Anthropic access
# If ANTHROPIC_API_KEY is not set, the SDK picks it up from the proxy
import agent
import sessions

PHONE = "test_user"

print("\n" + "=" * 55)
print("  Royal Arabian Safari — WhatsApp Agent (Test Mode)")
print("=" * 55)
print("Type your message and press Enter.")
print("Type 'quit' to exit.\n")

session = sessions.get(PHONE)

while True:
    try:
        user_input = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nBye!")
        sys.exit(0)

    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit", "q"):
        print("Bye!")
        sys.exit(0)

    try:
        reply, booking = agent.get_reply(session, user_input)
        sessions.save(PHONE, session)

        print(f"\nBot: {reply}\n")

        if booking:
            print("=" * 55)
            print("  *** BOOKING CAPTURED ***")
            print(f"  Name:    {booking.get('name')}")
            print(f"  Tour:    {booking.get('service')}")
            print(f"  Date:    {booking.get('date')}")
            print(f"  Adults:  {booking.get('adults')}")
            print(f"  Kids:    {booking.get('children', 0)}")
            print(f"  Pickup:  {booking.get('pickup')}")
            print(f"  Phone:   {booking.get('phone')}")
            print("  (In production this is sent to owner's WhatsApp)")
            print("=" * 55 + "\n")

    except Exception as e:
        print(f"\n[Error] {e}\n")
