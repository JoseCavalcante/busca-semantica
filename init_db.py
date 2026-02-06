
from db.database import engine
from db.models import Base, CandidateDocument

# This will create tables that don't exist yet
# It won't modify existing tables (SQLAlchemy limitation without alembic), 
# but since CandidateDocument is new, it works perfectly.
def init_db():
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
