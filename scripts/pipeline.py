from scripts.apply_to_job import apply_to_job
from scripts.auto_query import run_auto_query
from backend.resume.resume_parser import parse_resume_text,load_resume_text
from backend.db.connection import get_connection
from typing import Optional
from backend.utils.logging import get_logger
from backend.utils.constants import DEFAULT_SCORE_THRESHOLD

logger = get_logger(__name__)

async def run_full_pipeline(resume_path: str, user_query: Optional[str] = None, min_score: float = DEFAULT_SCORE_THRESHOLD) -> dict:
    conn = get_connection()
    
    resume_text = load_resume_text(resume_path)
    resume_data = parse_resume_text(resume_text)
    
    results = run_auto_query(resume_text, conn, user_query)

    applied = 0
    skipped = 0

    for job in results["matches"]:
        score = job.get("score", 0.0)
        if score >= min_score:
            try:
                await apply_to_job(job, resume_data, conn)
                applied += 1
            except Exception as e:
                logger.error(f"❌ Failed to apply to job {job.get('id')} – {job.get('title')}: {e}")
        else:
            logger.info(f"Skipping ⏭️ Score {score:.2f} < {min_score}: {job.get('title')} at {job.get('company_name')}")
            skipped += 1

    print(f"\n🚀 Finished applying:\n✅ Applied to {applied} jobs\n⏭️ Skipped {skipped} low-scoring jobs")
    print(f"💾 {results['saved_count']} new jobs saved from query: {results['query']}")

    return {
        "query": results["query"],
        "applied_count": applied,
        "skipped_count": skipped,
        "saved_count": results["saved_count"]
    }
