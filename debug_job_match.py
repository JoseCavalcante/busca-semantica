import sys
import os
sys.path.append(os.getcwd())

import asyncio
from db.database import SessionLocal
from db.models import Job
from service.queryservice import query_simples
import json

async def inspect_job_matching():
    db = SessionLocal()
    try:
        # 1. Find the specific job
        search_title = "Especialista em Segurança de Dados"
        job = db.query(Job).filter(Job.title.ilike(f"%{search_title}%")).first()
        
        if not job:
            print(f"❌ Job '{search_title}' not found in DB.")
            # List all jobs to see what's there
            print("Available Jobs:")
            for j in db.query(Job).all():
                print(f" - {j.title} (ID: {j.id})")
            return

        print(f"\n✅ Found Job: {job.title} (ID: {job.id})")
        print(f"   Requirements: {job.requirements}")
        print(f"   Skills Required (Raw): {job.skills_required}")

        # 2. Reconstruct the Query Logic from jobrouter.py
        # helper to clean skills
        def clean_skills(source):
            if isinstance(source, list):
                return set(s.lower().strip() for s in source)
            elif isinstance(source, str):
                try:
                    parsed = json.loads(source)
                    if isinstance(parsed, list):
                        return set(s.lower().strip() for s in parsed)
                except:
                    pass
                return set(s.lower().strip() for s in source.replace('\n', ',').split(',') if s.strip())
            return set()

        job_skills_set = clean_skills(job.skills_required)
        if not job_skills_set and job.requirements:
            job_skills_set = clean_skills(job.requirements)
        
        print(f"   Parsed Skills Set: {job_skills_set}")

        # Construct Query
        skills_str = ", ".join(job_skills_set) # Use the parsed set for display
        query_text = f"Título: {job.title}. Habilidades: {skills_str}. Requisitos: {job.requirements or ''}. Descrição: {(job.description or '')[:500]}"
        
        print(f"\n🔍 Generated Query Text:\n   '{query_text}'")

        # 3. Serialize Query
        print("\n🚀 Running similarity search...")
        # Assuming tenant_id 1 for debug or fetch from job if available (job model usually has tenant_id)
        tenant_id = job.tenant_id if hasattr(job, 'tenant_id') else 1
        response = await query_simples(search=query_text, tenant_id=tenant_id, db=db)

        if "matches" in response:
            matches = response['matches']
            print(f"\nfound {len(matches)} matches.")
            
            for i, match in enumerate(matches):
                # Calculate Common Skills
                candidate_skills = []
                metadata = match.get('metadata', {})
                
                if "skills" in metadata:
                    if isinstance(metadata["skills"], str):
                        try:
                            candidate_skills = json.loads(metadata["skills"])
                        except:
                            candidate_skills = [s.strip() for s in metadata["skills"].split(',')]
                    elif isinstance(metadata["skills"], list):
                        candidate_skills = metadata["skills"]
                
                candidate_skills_set = set(str(s).lower().strip() for s in candidate_skills)
                common = job_skills_set.intersection(candidate_skills_set)
                
                score = match.get('score', 0)
                match_id = match.get('id', 'unknown')
                
                print(f"   [{i+1}] Score: {score:.4f} - ID: {match_id}")
                print(f"       Metadata Keys: {list(metadata.keys())}")
                print(f"       Filename: {metadata.get('filename', 'N/A')}")
                print(f"       Source File: {metadata.get('source_file', 'N/A')}")
                
                print(f"       Common Skills: {common}")
                if not common:
                    print("       ⚠️ High score but NO common skills.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(inspect_job_matching())
