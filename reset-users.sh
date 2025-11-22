#!/bin/bash

echo "🔄 Resetting Demo Users (Handling Foreign Keys)"
echo "==============================================="
echo ""

echo "Disabling foreign key checks and recreating users..."
sudo docker-compose exec -T mysql mysql -u skillpilot -pskillpilot123 skillpilot_db <<EOF
SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM employee_skills;
DELETE FROM assessment_results;
DELETE FROM learning_roadmaps;
DELETE FROM users;

INSERT INTO users (id, name, email, password_hash, role, job_title_id, years_of_experience) VALUES
(1, 'Admin User', 'admin@skillpilot.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYNq8QQ8pKS', 'OD_MANAGER', NULL, 10),
(2, 'John Doe', 'john.doe@skillpilot.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYNq8QQ8pKS', 'EMPLOYEE', 1, 1.5);

SET FOREIGN_KEY_CHECKS = 1;

SELECT id, name, email, role FROM users;
EOF

echo ""
echo "✅ Users reset complete!"
echo ""
echo "🔑 Demo Credentials:"
echo "   OD Manager: admin@skillpilot.com / admin123"
echo "   Employee: john.doe@skillpilot.com / admin123"
echo ""
echo "🧪 Testing login..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@skillpilot.com","password":"admin123"}')

echo "$RESPONSE" | grep -q "access_token" && echo "✅ Login working! Got access token" || echo "❌ Login failed: $RESPONSE"
echo ""
echo "🌐 Now try logging in at: http://localhost"
echo ""
