#!/bin/bash

echo "🏥 CuanBot Health Check"
echo "======================="

echo ""
echo "📊 Docker Services:"
docker-compose ps

echo ""
echo "🔧 Backend API:"
curl -s http://localhost:8000/health | python3 -m json.tool || echo "❌ Backend not responding"

echo ""
echo "📡 Ngrok Status:"
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool 2>/dev/null | grep -A 1 "public_url" || echo "❌ Ngrok not responding"

echo ""
echo "🗄️  Database:"
docker-compose exec -T postgres pg_isready -U cuanbot || echo "❌ Database not responding"

echo ""
echo "✅ Health check complete!"
