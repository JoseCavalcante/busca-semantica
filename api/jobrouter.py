from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import json

from db.database import get_db
from db.models import Job, User
from api.authenticationrouter import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

# --- Pydantic Models ---

class JobBase(BaseModel):
    title: str
    department: Optional[str] = None
    location: Optional[str] = None
    contract_type: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    salary_range: Optional[str] = None
    skills_required: Optional[List[str]] = []
    status: Optional[str] = "Open"

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    tenant_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    # Convert list to JSON string for storage
    skills_json = json.dumps(job.skills_required) if job.skills_required else "[]"
    
    new_job = Job(
        tenant_id=current_user.tenant_id,
        title=job.title,
        department=job.department,
        location=job.location,
        contract_type=job.contract_type,
        description=job.description,
        requirements=job.requirements,
        benefits=job.benefits,
        salary_range=job.salary_range,
        skills_required=skills_json,
        status=job.status
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    # Parse back for response
    new_job.skills_required = json.loads(new_job.skills_required) if new_job.skills_required else []
    
    return new_job

@router.get("/", response_model=List[JobResponse])
async def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    jobs = db.query(Job).filter(Job.tenant_id == current_user.tenant_id).offset(skip).limit(limit).all()
    
    # Parse JSON fields
    for job in jobs:
        if job.skills_required:
            try:
                job.skills_required = json.loads(job.skills_required)
            except:
                job.skills_required = []
                
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id, Job.tenant_id == current_user.tenant_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.skills_required:
        try:
            job.skills_required = json.loads(job.skills_required)
        except:
            job.skills_required = []
            
    return job

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_job = db.query(Job).filter(Job.id == job_id, Job.tenant_id == current_user.tenant_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update fields
    for key, value in job_update.dict(exclude_unset=True).items():
        if key == "skills_required":
            setattr(db_job, key, json.dumps(value))
        else:
            setattr(db_job, key, value)
            
    db.commit()
    db.refresh(db_job)
    
    if db_job.skills_required:
        try:
            db_job.skills_required = json.loads(db_job.skills_required)
        except:
            db_job.skills_required = []
            
    return db_job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_job = db.query(Job).filter(Job.id == job_id, Job.tenant_id == current_user.tenant_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(db_job)
    db.commit()
    
# --- Matching Logic ---

from service.queryservice import query_simples

@router.get("/{job_id}/matches", status_code=status.HTTP_200_OK)
async def get_job_matches(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id, Job.tenant_id == current_user.tenant_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Ensure job metadata is parsed for response (optional but good practice)
    if job.skills_required:
         try:
            # It's already loaded as string from DB, we want object for Pydantic info
            # BUT: accessing .skills_required on ORM object returns the string from DB.
            # We need to temporarily set it or let Pydantic handle it?
            # Actually, Pydantic from_attributes will take the attribute. 
            # If it's a string in DB, Pydantic expects List[str].
            # We must parse it.
            job.skills_required = json.loads(job.skills_required) 
         except:
            job.skills_required = []

     # Construct semantic search query
    # Prioritize Title and Requirements for better matching. Description can be noisy.
    # Prioritize Title and Skills. Description is often too generic and causes false positives.
    skills_str = ", ".join(job.skills_required) if isinstance(job.skills_required, list) else str(job.skills_required)
    query_text = f"Cargo: {job.title}. Habilidades Obrigatórias: {skills_str}. Requisitos Técnicos: {job.requirements or ''}."
    
    # Use existing query service
    # We use query_simples for now, but could switch to filtered if we wanted to enforce filters (e.g. location?)
    response = query_simples(search=query_text)
    
    # Ensure job skills are a set for intersection (handle if it's still a string or None)
    job_skills_set = set()
    
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
            # Fallback for comma or newline separated string
            return set(s.lower().strip() for s in source.replace('\n', ',').split(',') if s.strip())
        return set()

    job_skills_set = clean_skills(job.skills_required)

    # Fallback: If no explicit skills, try to extract from Requirements
    if not job_skills_set and job.requirements:
        job_skills_set = clean_skills(job.requirements)
        
    if "matches" in response:
        matches = response['matches']
        jsonResponse = []
        for match in matches:
            # Parse full_enriched_json if it exists and is a string
            # Access as dictionary
            metadata = match.get('metadata', {})
            
            if "full_enriched_json" in metadata and isinstance(metadata["full_enriched_json"], str):
                try:
                    metadata["full_enriched_json"] = json.loads(metadata["full_enriched_json"])
                except Exception as e:
                    print(f"Error parsing full_enriched_json for match {match.get('id')}: {e}")

            # Parse skills if it exists and is a string
            candidate_skills = []
            if "skills" in metadata:
                if isinstance(metadata["skills"], str):
                    try:
                        metadata["skills"] = json.loads(metadata["skills"])
                        candidate_skills = metadata["skills"]
                    except:
                        # Split by comma if simple string
                        candidate_skills = [s.strip() for s in metadata["skills"].split(',')]
                elif isinstance(metadata["skills"], list):
                    candidate_skills = metadata["skills"]
            
            # Calculate Common Skills (Explainability)
            candidate_skills_set = set(str(s).lower().strip() for s in candidate_skills)
            common = job_skills_set.intersection(candidate_skills_set)
            
            common_display = [s for s in candidate_skills if str(s).lower().strip() in common]

            jsonResponse.append({
                "id": match.get('id'),
                "score": match.get('score'),
                "metadata": metadata,
                "common_skills": common_display # EXPLAINABILITY
            })
            
        return {
            "job": JobResponse.model_validate(job),
            "matches": jsonResponse
        }
    
    return {
        "job": JobResponse.model_validate(job),
        "matches": []
    }

