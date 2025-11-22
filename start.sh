#!/bin/bash

echo "🎯 SkillPilot AI - Starting Application"
echo "======================================"
echo ""

# Clean up any old containers
echo "🧹 Cleaning up old containers..."
sudo docker-compose down -v 2>/dev/null || true
sudo docker system prune -f 2>/dev/null || true

echo ""
echo "🚀 Starting fresh containers..."
sudo docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to start..."
sleep 15

echo ""
echo "📊 Checking service status..."
sudo docker-compose ps

echo ""
echo "✅ SkillPilot AI is running!"
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
echo "📊 View logs: sudo docker-compose logs -f"
echo "🛑 Stop: sudo docker-compose down"
echo ""

