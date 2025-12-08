#!/bin/bash

# Script to update Telegram webhook with current ngrok URL

echo "🔄 Updating Telegram Webhook..."

# Get ngrok URL from API
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | head -1 | cut -d'"' -f4)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Error: Could not get ngrok URL. Make sure ngrok is running."
    exit 1
fi

echo "📡 Ngrok URL: $NGROK_URL"

# Update webhook URL
WEBHOOK_URL="${NGROK_URL}/webhook/telegram"
echo "🔗 Webhook URL: $WEBHOOK_URL"

# Get bot token from .env
BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN .env | cut -d'=' -f2)

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN not found in .env"
    exit 1
fi

# Set webhook
RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"${WEBHOOK_URL}\"}")

echo "📥 Response: $RESPONSE"

# Check if successful
if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ Webhook updated successfully!"
    echo ""
    echo "📝 To make this permanent, update your .env file:"
    echo "TELEGRAM_WEBHOOK_URL=${WEBHOOK_URL}"
else
    echo "❌ Failed to update webhook"
    exit 1
fi
