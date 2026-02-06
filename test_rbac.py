
from fastapi.testclient import TestClient
from main import app
from db.models import User
from api.authenticationrouter import get_current_user, create_access_token
from datetime import timedelta

# Mock user dependency explicitly for granular control? 
# Or just generate tokens. Tokens are easier if we mock the DB or just rely on a mock dependency override.

client = TestClient(app)


def test_rbac_protection():
    # 1. Simulate Member User
    member_user = User(username="member_test", role="member", tenant_id=1, id=998)
    token_member = create_access_token(data={"sub": "member_test"})
    
    print(f"\n--- Testing with User Role: {member_user.role} ---")
    
    # Override dependency to return this user
    app.dependency_overrides[get_current_user] = lambda: member_user
    
    # Try to CREATE a job
    print("Attempting to CREATE job...")
    response = client.post(
        "/api/jobs/",
        json={"title": "Unauthorized Job", "status": "Open"},
        headers={"Authorization": f"Bearer {token_member}"}
    )
    
    print(f"Member Create Job Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 403:
        print("✅ MEMBER BLOCKED (Success)")
    else:
        print("❌ MEMBER ALLOWED (FAILURE!)")

    # Try to DELETE a job (ID 1)
    print("Attempting to DELETE job 1...")
    response_del = client.delete(
        "/api/jobs/1",
        headers={"Authorization": f"Bearer {token_member}"}
    )
    print(f"Member Delete Job Status: {response_del.status_code}")
    if response_del.status_code == 403:
        print("✅ MEMBER DELETE BLOCKED (Success)")
    else:
        print("❌ MEMBER DELETE ALLOWED (FAILURE!)")

if __name__ == "__main__":
    test_rbac_protection()
