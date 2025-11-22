#!/bin/bash

echo "🎯 SkillPilot AI - Starting Application"
echo "======================================"
echo ""

# Clean up old containers
echo "🧹 Cleaning up old containers..."
sudo docker-compose down -v 2>/dev/null || true
sudo docker rm -f skillpilot_backend skillpilot_frontend skillpilot_mysql 2>/dev/null || true
sudo docker system prune -f 2>/dev/null || true

echo ""
echo "🔨 Building backend (using cache if available)..."
sudo docker-compose build backend

echo ""
echo "🚀 Starting all services..."
sudo docker-compose up -d

echo ""
echo "⏳ Waiting for services to initialize..."
echo "   MySQL is starting..."
sleep 10
echo "   Backend is starting..."
sleep 10
echo "   Services should be ready..."

echo ""
echo "📊 Checking service status..."
sudo docker-compose ps

echo ""
echo "📋 Recent backend logs:"
sudo docker-compose logs --tail=20 backend

echo ""
echo "🔍 Testing backend health..."
sleep 2
HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "Backend not responding yet")
echo "   Response: $HEALTH"

echo ""
if [[ "$HEALTH" == *"healthy"* ]]; then
    echo "✅ SkillPilot AI is running successfully!"
else
    echo "⚠️  Backend might still be starting. Check logs with:"
    echo "   sudo docker-compose logs backend"
fi

echo ""
echo "📍 Access the application:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔑 Demo Credentials:"
echo "   OD Manager: admin@skillpilot.com / admin123"
echo "   Employee: john.doe@skillpilot.com / admin123"
echo ""
echo "💡 Useful Commands:"
echo "   View logs: sudo docker-compose logs -f"
echo "   Backend logs: sudo docker-compose logs -f backend"
echo "   Restart: sudo docker-compose restart"
echo "   Stop: sudo docker-compose down"
echo ""
echo "💾 Note: Docker is caching dependencies for faster future builds!"
echo ""
