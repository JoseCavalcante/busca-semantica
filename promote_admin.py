import sys
import os
sys.path.append(os.getcwd())

from db.database import SessionLocal
from db.models import User

def promoting_user_to_admin(username):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"❌ User '{username}' not found.")
            return

        print(f"Current Role for {username}: {user.role}")
        user.role = "admin"
        db.commit()
        print(f"✅ User '{username}' promoted to ADMIN successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Promoting 'jose' to admin based on previous context
    promoting_user_to_admin("jose")
