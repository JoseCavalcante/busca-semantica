import requests
import json

# Setup
BASE_URL = "http://127.0.0.1:8001"
# Login to get token (assuming test user exists, otherwise we might need to create one or use existing token if I can find it)
# For simplicity, I will try to use the token if I can find it in the browser logs, but I can't.
# So I'll just rely on the fact that I can't easily authenticate without a user.
# Wait, I can import the service and run the function directly! Much better than HTTP request which needs auth.

import sys
import os
sys.path.append(os.getcwd())

import asyncio
from db.database import SessionLocal
from db.models import Job, User
from api.jobrouter import get_job_matches, JobResponse

# Mock dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def test_backend_logic():
    db = SessionLocal()
    try:
        # Get first job
        job = db.query(Job).first()
        if not job:
            print("No jobs found in DB.")
            return

        print(f"Testing with Job ID: {job.id}")
        
        # Manual Override for Testing (since DB might be empty)
        job.skills_required = ["Python", "SQL", "React", "AWS", "Docker", "Machine Learning"] 
        
        print(f"Job Title: {job.title}")
        print(f"Job Skills: {job.skills_required}")

        # Call get_job_matches logic directly (simulating the router)
        # We need to manually construct the logic since calling the router function requires dependencies
        # Actually, let's just copy the logic snippet to verify it works "in principle" with real DB data
        
        from service.queryservice import query_simples
        
        # LOGIC FROM jobrouter.py
        skills_str = ", ".join(job.skills_required) if isinstance(job.skills_required, list) else str(job.skills_required)
        query_text = f"Título: {job.title}. Habilidades: {skills_str}. Requisitos: {job.requirements or ''}. Descrição: {(job.description or '')[:500]}"
        
        print(f"Query Text: {query_text}")
        
        response = query_simples(search=query_text)
        
        if "matches" in response:
            print(f"\nFound {len(response['matches'])} matches.")
            
            # Prepare Job Skills Set
            job_skills_set = set()
            if isinstance(job.skills_required, list):
                job_skills_set = set(s.lower().strip() for s in job.skills_required)
            elif isinstance(job.skills_required, str):
                try:
                     parsed = json.loads(job.skills_required)
                     if isinstance(parsed, list):
                         job_skills_set = set(s.lower().strip() for s in parsed)
                except:
                     job_skills_set = {job.skills_required.lower().strip()}
            
            print(f"Job Skills Set: {job_skills_set}")

            for i, match in enumerate(response['matches'][:3]): # Check top 3
                print(f"\n--- Match {i+1} ---")
                print(f"ID: {match.id}")
                
                # Parse candidate skills
                candidate_skills = []
                if "skills" in match.metadata:
                    if isinstance(match.metadata["skills"], str):
                        try:
                            match.metadata["skills"] = json.loads(match.metadata["skills"])
                            candidate_skills = match.metadata["skills"]
                        except:
                            candidate_skills = [s.strip() for s in match.metadata["skills"].split(',')]
                    elif isinstance(match.metadata["skills"], list):
                        candidate_skills = match.metadata["skills"]
                
                print(f"Candidate Skills: {candidate_skills}")
                
                # Calculate Intersection
                candidate_skills_set = set(str(s).lower().strip() for s in candidate_skills)
                common = job_skills_set.intersection(candidate_skills_set)
                common_display = [s for s in candidate_skills if str(s).lower().strip() in common]
                
                print(f"Calculated Common Skills: {common_display}")
                
                if common_display:
                    print("SUCCESS: Common skills found.")
                else:
                    print("WARNING: No common skills found (Intersection empty).")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_backend_logic())
