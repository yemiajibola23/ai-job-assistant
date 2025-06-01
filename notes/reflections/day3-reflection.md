# 🪞 Day 3 Reflection – AI Job Assistant

## 🧩 What We Built
- Wrote `filter_jobs()` using cosine similarity to match job descriptions to a resume.
- Designed and initialized a normalized SQLite schema for storing filtered jobs.
- Implemented `save_jobs_to_db()` to store filtered matches while avoiding duplicates.
- Connected the full pipeline in an integration test and configured pytest pathing.

## 💬 Reflection Prompts

**1. Most challenging part:**  
Understanding Python syntax when creating the job filtering function. I knew what I wanted to do but not in the most elegant, Python-y way.

**2. Most satisfying part:**  
Writing the db logic was satisfying because I could envision its place in the overall scheme.

**3. Concept I understand better:**  
I think I understand a little bit more about Python testing using pytest.

**4. Surprising or unexpected:**  
It was surprising running into the import issues over and over.

**5. Want to revisit or go deeper:**  
I would like to convert the other test scripts to pytest eventually.
