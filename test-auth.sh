#!/bin/bash

echo "🔍 Testing Token Authentication"
echo "==============================="
echo ""

echo "1️⃣ Getting a fresh login token..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@skillpilot.com","password":"admin123"}')

echo "Login response:"
echo "$RESPONSE"
echo ""

TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Failed to get token from login!"
    exit 1
fi

echo "✅ Token received: ${TOKEN:0:20}..."
echo ""

echo "2️⃣ Testing token with protected endpoint..."
curl -v -X GET http://localhost:8000/api/reports/employees \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  2>&1 | grep -E "< HTTP|< content-type|employees"

echo ""
echo "3️⃣ Checking backend logs for auth errors..."
sudo docker-compose logs backend | tail -30 | grep -E "401|Unauthorized|JWT|token"

echo ""
echo "Done!"

