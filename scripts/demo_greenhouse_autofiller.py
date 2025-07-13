from pathlib import Path
import json
import asyncio
from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller
from backend.utils.constants import TEST_JOB_DICT
from backend.generation.generators.essay_generator import EssayResponseGenerator

def load_user_profile():
    path = Path("scripts/data/user_profile.json")
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

profile_data = load_user_profile()

async def run():
        print("🤖 Running Greenhouse autofill (dry-run)...")
        autofiller = GreenhouseAutofiller()
        await autofiller.autofill(
            profile_data,
            resume_path="tests/data/yemi_resume.pdf",
            cover_letter_path="tests/data/cover_letter.pdf",
            job_data=TEST_JOB_DICT,
            dry_run=True
        )
if __name__ == "__main__":
    asyncio.run(run())