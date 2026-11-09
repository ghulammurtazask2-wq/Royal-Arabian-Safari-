# Royal Arabian Safari — WhatsApp Agent Setup Guide

## What This Does

A Claude-powered WhatsApp bot connected to your business WhatsApp number (+971 58 228 2683) that:

1. **Answers** every customer message about tours & prices (from your website)
2. **Guides** customers through booking — collects name, tour, date, guests, pickup location
3. **Confirms** the booking to the customer via WhatsApp
4. **Notifies you** instantly with full booking details so you can confirm availability

---

## Step 1 — Get a Meta WhatsApp Business API Account (Free)

1. Go to [developers.facebook.com](https://developers.facebook.com) → **My Apps → Create App**
2. Choose **Business** type
3. Add **WhatsApp** product to your app
4. Under **WhatsApp → API Setup**, you'll see:
   - **Phone Number ID** → copy this
   - **Temporary Access Token** → copy this (create a Permanent System User for production)
5. Add your WhatsApp number (+971 58 228 2683) as the Business Phone Number

---

## Step 2 — Get Your Anthropic API Key

1. Go to [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Create a new API key → copy it

---

## Step 3 — Deploy the Agent (choose one)

### Option A: Railway (Easiest — Free Tier Available)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy from the whatsapp-agent folder
cd whatsapp-agent
railway init
railway up

# 4. Set environment variables in Railway dashboard:
#    ANTHROPIC_API_KEY, WHATSAPP_PHONE_NUMBER_ID,
#    WHATSAPP_ACCESS_TOKEN, WHATSAPP_VERIFY_TOKEN,
#    OWNER_WHATSAPP_NUMBER
```

Your webhook URL will be: `https://your-app.railway.app/webhook`

### Option B: Local + ngrok (For Testing)

```bash
cd whatsapp-agent

# Install dependencies
pip install -r requirements.txt

# Copy and fill in your credentials
cp .env.example .env
nano .env

# Run the server
python app.py

# In another terminal, expose it publicly
ngrok http 5000
```

Your webhook URL: `https://xxxx.ngrok.io/webhook`

### Option C: Any VPS / Ubuntu Server

```bash
# Install
git clone <your-repo>
cd whatsapp-agent
pip install -r requirements.txt
cp .env.example .env
# edit .env with your keys

# Run with Gunicorn (production)
gunicorn -w 2 -b 0.0.0.0:5000 app:app

# Optional: use nginx as reverse proxy on port 443 with SSL
```

---

## Step 4 — Connect Webhook to Meta

1. In Meta Developer Console → **WhatsApp → Configuration → Webhook**
2. Enter:
   - **Callback URL**: `https://your-domain.com/webhook`
   - **Verify Token**: the value you set for `WHATSAPP_VERIFY_TOKEN` in your `.env`
3. Click **Verify and Save**
4. Under **Webhook fields**, subscribe to: `messages`

---

## Step 5 — Test It

Send a WhatsApp message to your business number. You should get a reply within 5 seconds.

**Test messages to try:**
- "Hi, what are your prices?"
- "How much is the desert safari?"
- "I want to book the Abu Dhabi city tour for 4 people on 20 December"

---

## How the Booking Flow Works

```
Customer: "Hi, I want to book a desert safari"
Bot: "Welcome! 🏜️ Our Desert Safari Dubai is AED 799/car (up to 6 guests). 
      Ready to book? Can I have your full name?"

Customer: "Ahmed Al Rashid"
Bot: "Great, Ahmed! Which date works for you? (DD/MM/YYYY)"

Customer: "15 December 2026"
Bot: "Perfect — how many guests? (adults + children separately)"

Customer: "3 adults, 2 kids"
Bot: "And which hotel are you staying at for pickup?"

Customer: "Atlantis The Palm"
Bot: "✅ Booking Confirmed!
     Name: Ahmed Al Rashid
     Tour: Desert Safari Dubai
     Date: 15/12/2026
     Guests: 3 adults + 2 children
     Pickup: Atlantis The Palm
     
     We'll confirm your slot within 2 hours. No deposit needed! 🎉"

[YOU receive on YOUR WhatsApp:]
🔔 NEW BOOKING — Royal Arabian Safari
👤 Name: Ahmed Al Rashid
🏜️ Tour: Desert Safari Dubai
📅 Date: 15/12/2026
👥 Guests: 3 adults + 2 children
🏨 Pickup: Atlantis The Palm
📱 Customer Phone: +971501234567
✅ Please confirm availability and reply to the customer.
```

---

## Environment Variables Reference

| Variable | Where to Get |
|----------|-------------|
| `ANTHROPIC_API_KEY` | console.anthropic.com |
| `WHATSAPP_PHONE_NUMBER_ID` | Meta Developer Console → WhatsApp → API Setup |
| `WHATSAPP_ACCESS_TOKEN` | Meta Developer Console → WhatsApp → API Setup |
| `WHATSAPP_VERIFY_TOKEN` | Any secret string you choose |
| `OWNER_WHATSAPP_NUMBER` | Your number e.g. +971582282683 |

---

## File Structure

```
whatsapp-agent/
├── app.py           # Flask webhook server (main entry point)
├── agent.py         # Claude AI conversation logic
├── prices.py        # All your services & prices
├── sessions.py      # Conversation memory per customer
├── whatsapp.py      # Meta WhatsApp API client
├── notifications.py # Owner notification system
├── requirements.txt
└── .env.example     # Template for your credentials
```

---

## Support

If you need help with deployment, WhatsApp: **+971 58 228 2683**
