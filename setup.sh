#!/bin/bash

echo "🚀 CuanBot Setup Script"
echo "======================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials!"
    echo ""
    echo "Required:"
    echo "  - TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "  - GEMINI_API_KEY (from Google AI Studio)"
    echo "  - NGROK_AUTHTOKEN (from ngrok.com)"
    echo ""
    read -p "Press enter to continue after editing .env..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "✅ CuanBot is starting!"
echo ""
echo "📊 Dashboard: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📡 Ngrok Dashboard: http://localhost:4040"
echo ""
echo "🤖 To setup Telegram webhook:"
echo "1. Open http://localhost:4040 to get your ngrok URL"
echo "2. Update TELEGRAM_WEBHOOK_URL in .env"
echo "3. Run: docker-compose restart backend"
echo ""
echo "📋 View logs: docker-compose logs -f"
echo ""
