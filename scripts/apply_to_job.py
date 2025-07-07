
from backend.generation.export.tailored_resume_exporter import generate_and_render_tailored_resume
from backend.generation.export.tailored_cover_letter_exporter import generate_and_render_tailored_cover_letter
from backend.db.application_dao import add_application
from backend.db.connection import get_connection
from backend.generation.generators.cover_letter_generator import CoverLetterGenerator
from backend.generation.generators.resume_generator import ResumeGenerator
from backend.autofill.playwright_autofiller import PlaywrightAutofiller
from backend.generation.client.openai_client import client
from backend.generation.templates.jinja_env import get_jinja_env
import json
from pathlib import Path
import sqlite3



def load_user_profile():
    path = Path("scripts/data/user_profile.json")
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def apply_to_job(job: dict, resume_data: dict, conn: sqlite3.Connection):
    job_id = job.get("id")
    if not job_id:
        raise ValueError("Missing job ID")
    job_url = job["url"]
    job_description = job["description"]
    
    
    # Step 1: Generate assets
    jinja_env = get_jinja_env()
    resume_generator = ResumeGenerator(jinja_env, client)
    cover_letter_generator = CoverLetterGenerator(jinja_env, client)
    tailored_data = resume_generator.tailor_resume_data(resume_data, job_description)
    
    resume_path = generate_and_render_tailored_resume(job_id, resume_data, job_description, resume_generator, tailored_data)
    cover_letter_path = generate_and_render_tailored_cover_letter(job_id, resume_data, job_description, tailored_data, cover_letter_generator)
    
    # Step 2: Run the autofiller
    profile_data = load_user_profile()
    application_data = {
        **profile_data,
        "first_name": profile_data.get("name", "").split()[0],
        "last_name": profile_data.get("name", "").split()[-1],
        "email": profile_data.get("email"),
        "phone": profile_data.get("phone"),
        "resume": str(resume_path),
        "cover_letter": str(cover_letter_path)
    }
    autofiller = PlaywrightAutofiller(job_url)
    autofill_result = autofiller.fill_form(application_data)
    
    app_dict = {
        "job_id": job_id,
        "job_title": job.get("title", "Unknown Title"),
        "company_name": job.get("company", "Unknown Company"),
        "location": job.get("location", ""),
        "tailored_resume_path": str(resume_path),
        "tailored_cover_letter_path": str(cover_letter_path),
        "status": "Applied"
    }
    
    add_application(conn, app_dict)
    
    
    print(f"✅ Applied to {job['title']} at {job['company']}")
    print(f"📝 Resume: {resume_path}")
    print(f"💌 Cover Letter: {cover_letter_path}")
    print(f"🔗 Job URL: {job_url}")
    
    print("\n📋 Autofill Summary:")
    print(f"🧠 Filled fields: {len(autofill_result['filled_fields'])} → {autofill_result['filled_fields']}")
    print(f"📁 Uploaded files: {autofill_result['uploaded_files']}")
    print(f"⏭️ Skipped fields: {len(autofill_result['skipped_fields'])} → {autofill_result['skipped_fields']}")
    print(f"⚠️ Errors: {len(autofill_result['errors'])} → {autofill_result['errors']}")
    print(f"✅ Clicked Submit: {autofill_result['clicked_submit']}")
    print(f"🎯 Confirmation Found: {autofill_result['confirmation_found']}")
