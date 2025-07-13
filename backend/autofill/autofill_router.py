from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller
from backend.autofill.base_autofiller import BaseAutofiller
from backend.utils.logging import get_logger

logger = get_logger(__name__)

def get_autofill_strategy(url: str) -> str:
    if "greenhouse.io" in url:
        return "greenhouse"
    return "unsupported"

async def autofill_router(profile_data, resume_path, cover_letter_path, job_data, page=None, dry_run=True):
    url = job_data.get("url")
    if not url:
        raise ValueError("Missing job_data['url']. Cannot launch form.")
    
    strategy = get_autofill_strategy(url)
    logger.info(f"[autofill-router] 🔍 Detected ATS: {strategy} from URL: {url}")

    autofiller: BaseAutofiller

    if strategy == "greenhouse":
        autofiller = GreenhouseAutofiller()
    else:
        raise NotImplementedError(f"ATS strategy not yet implemented for URL: {url}")

    return await autofiller.autofill(profile_data, resume_path, cover_letter_path, job_data, page, dry_run)
