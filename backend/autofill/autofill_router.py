from backend.autofill.greenhouse_autofiller import GreenhouseAutofiller

from backend.autofill.base_autofiller import BaseAutofiller
from backend.utils.logging import get_logger

logger = get_logger(__name__)

def get_autofill_strategy(url: str) -> str:
    if "greenhouse.io" in url:
        return "greenhouse"
    else:
        return "unsupported"

def autofill_router(page, application_data, dry_run=True) -> None:
    url = page.url
    strategy = get_autofill_strategy(url)
    logger.info(f"[autofill-router] 🔍 Detected ATS: {strategy} from URL: {url}")

    autofiller: BaseAutofiller
    
    if strategy == "greenhouse":
        autofiller = GreenhouseAutofiller(page, application_data, dry_run)
    else:
        raise NotImplementedError(f"ATS strategy not yet implemented for URL: {url}")
    
    result = autofiller.fill()
    print("=== Result Log ===")
    for key, val in result.items():
        print(f"{key}: {val}")
    