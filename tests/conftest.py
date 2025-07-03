# tests/conftest.py
import logging

def pytest_configure(config):
    # Force suppression of noisy external loggers
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    logging.getLogger("httpx").setLevel(logging.CRITICAL)
    logging.getLogger("sentence_transformers").setLevel(logging.CRITICAL)
    logging.getLogger("transformers").setLevel(logging.CRITICAL)
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
