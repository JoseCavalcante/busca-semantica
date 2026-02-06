from db.database import engine
from db.models import Base

def create_jobs_table():
    print("Attempting to create 'jobs' table if not exists...")
    # This will only create tables that don't exist
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    create_jobs_table()
