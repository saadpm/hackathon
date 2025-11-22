#!/bin/bash

echo "🔍 Complete System Check & Test"
echo "==============================="
echo ""

echo "1️⃣ Checking users in database..."
sudo docker-compose exec -T mysql mysql -u skillpilot -pskillpilot123 skillpilot_db -e "SELECT id, name, email, role FROM users;" 2>/dev/null

echo ""
echo "2️⃣ Testing login and getting NEW token..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@skillpilot.com","password":"admin123"}')

echo "Login response:"
echo "$RESPONSE" | head -c 300
echo ""

TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed!"
    echo "Full response: $RESPONSE"
    exit 1
fi

echo ""
echo "✅ Token received: ${TOKEN:0:30}..."
echo ""

echo "3️⃣ Testing protected endpoint with NEW token..."
EMPLOYEES=$(curl -s -X GET http://localhost:8000/api/reports/employees \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json")

echo "Employees response:"
echo "$EMPLOYEES" | head -c 200
echo ""

if echo "$EMPLOYEES" | grep -q "email"; then
    echo ""
    echo "✅ SUCCESS! Authentication is working!"
    echo ""
    echo "🎉 Your credentials work:"
    echo "   Email: admin@skillpilot.com"
    echo "   Password: admin123"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Go to: http://localhost"
    echo "   2. Open Console (F12)"
    echo "   3. Run: localStorage.clear()"
    echo "   4. Refresh page"
    echo "   5. Login with above credentials"
    echo ""
else
    echo ""
    echo "❌ Still failing. Checking backend logs..."
    sudo docker-compose logs backend | grep -E "\[AUTH\]|\[DECODE\]" | tail -10
fi

