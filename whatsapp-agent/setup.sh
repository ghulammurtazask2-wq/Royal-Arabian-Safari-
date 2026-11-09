#!/bin/bash
# Royal Arabian Safari — WhatsApp Agent Automated Setup
# Run this once: bash setup.sh

set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Royal Arabian Safari — WhatsApp Agent Setup      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Step 1: Check Python ────────────────────────────────────────────────────
echo -e "${YELLOW}[1/5] Checking Python...${NC}"
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Python3 not found. Install from https://python.org${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python3 --version) found${NC}"

# ── Step 2: Install dependencies ────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[2/5] Installing dependencies...${NC}"
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Dependencies installed${NC}"

# ── Step 3: Collect credentials ─────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[3/5] Setting up credentials...${NC}"
echo ""

if [ -f .env ]; then
    read -p "  .env file already exists. Overwrite? (y/N): " overwrite
    [[ "$overwrite" != "y" && "$overwrite" != "Y" ]] && echo "Keeping existing .env" && SKIP_CREDS=1
fi

if [ -z "$SKIP_CREDS" ]; then
    echo -e "  ${BLUE}── Anthropic API Key ──${NC}"
    echo "  Get from: https://console.anthropic.com/settings/keys"
    read -p "  Paste your Anthropic API key (sk-ant-...): " ANTHROPIC_KEY
    echo ""

    echo -e "  ${BLUE}── WhatsApp Business API ──${NC}"
    echo "  Get from: https://developers.facebook.com → Your App → WhatsApp → API Setup"
    read -p "  Phone Number ID (15-digit number): " WA_PHONE_ID
    read -p "  Permanent Access Token (EAAxxxxx...): " WA_TOKEN
    echo ""

    echo -e "  ${BLUE}── Webhook Verify Token ──${NC}"
    echo "  Any secret word you choose (you'll enter this in Meta dashboard)"
    read -p "  Verify Token [royal_safari_2024]: " WA_VERIFY
    WA_VERIFY="${WA_VERIFY:-royal_safari_2024}"
    echo ""

    echo -e "  ${BLUE}── Owner WhatsApp Number ──${NC}"
    echo "  Your number to receive booking notifications"
    read -p "  Owner number [+971582282683]: " OWNER_NUM
    OWNER_NUM="${OWNER_NUM:-+971582282683}"

    cat > .env <<EOF
ANTHROPIC_API_KEY=${ANTHROPIC_KEY}
WHATSAPP_PHONE_NUMBER_ID=${WA_PHONE_ID}
WHATSAPP_ACCESS_TOKEN=${WA_TOKEN}
WHATSAPP_VERIFY_TOKEN=${WA_VERIFY}
OWNER_WHATSAPP_NUMBER=${OWNER_NUM}
PORT=5000
FLASK_DEBUG=0
EOF

    echo ""
    echo -e "${GREEN}✓ .env file created${NC}"
fi

# ── Step 4: Install ngrok for public URL ────────────────────────────────────
echo ""
echo -e "${YELLOW}[4/5] Setting up public URL (ngrok)...${NC}"

if ! command -v ngrok &>/dev/null; then
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)
    [[ "$ARCH" == "x86_64" ]] && ARCH="amd64"
    [[ "$ARCH" == "aarch64" ]] && ARCH="arm64"
    echo "  Downloading ngrok for ${OS}/${ARCH}..."
    curl -sL "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-${OS}-${ARCH}.tgz" -o /tmp/ngrok.tgz
    tar -xf /tmp/ngrok.tgz -C /usr/local/bin/
    echo -e "${GREEN}✓ ngrok installed${NC}"
else
    echo -e "${GREEN}✓ ngrok already installed${NC}"
fi

# ── Step 5: Launch everything ────────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[5/5] Starting the agent...${NC}"
echo ""

# Load .env
export $(grep -v '^#' .env | xargs)

# Start Flask server in background
python app.py &
SERVER_PID=$!
sleep 2

# Check server started
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${RED}ERROR: Server failed to start. Check your ANTHROPIC_API_KEY.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Agent server running (PID $SERVER_PID)${NC}"

# Start ngrok
echo -e "${GREEN}✓ Starting public tunnel...${NC}"
echo ""
ngrok http 5000 --log=stdout &
NGROK_PID=$!
sleep 3

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['tunnels'][0]['public_url'])" 2>/dev/null || echo "")

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              AGENT IS LIVE! 🚀                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

if [ -n "$NGROK_URL" ]; then
    echo -e "  Your webhook URL: ${GREEN}${NGROK_URL}/webhook${NC}"
    echo ""
    echo -e "  ${YELLOW}FINAL STEP — Paste this URL in Meta Developer Console:${NC}"
    echo "  1. Go to: https://developers.facebook.com → Your App → WhatsApp → Configuration"
    echo "  2. Callback URL: ${NGROK_URL}/webhook"
    echo "  3. Verify Token: $(grep WHATSAPP_VERIFY_TOKEN .env | cut -d= -f2)"
    echo "  4. Click 'Verify and Save'"
    echo "  5. Subscribe to 'messages' field"
    echo ""
    echo "  Then message your WhatsApp business number — the bot will reply!"
else
    echo "  Ngrok URL: Check http://localhost:4040 in your browser"
fi

echo ""
echo "  Press Ctrl+C to stop the agent."
echo ""

# Keep running
wait $SERVER_PID
