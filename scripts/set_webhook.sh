#!/bin/bash

# Script to set Telegram webhook

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./set_webhook.sh <BOT_TOKEN> <WEBHOOK_URL>"
    echo "Example: ./set_webhook.sh 123456:ABC-DEF https://abc123.ngrok.io/webhook/telegram"
    exit 1
fi

BOT_TOKEN=$1
WEBHOOK_URL=$2

echo "Setting webhook for bot..."
echo "Token: $BOT_TOKEN"
echo "Webhook URL: $WEBHOOK_URL"

RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=${WEBHOOK_URL}")

echo ""
echo "Response: $RESPONSE"

# Check webhook info
echo ""
echo "Checking webhook info..."
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool
