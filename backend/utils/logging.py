# utils/logging.py
import logging
import os
import sys

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sentence_transformers").setLevel(logging.INFO)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)  # or WARNING if too noisy
    
    if not logger.hasHandlers():
        level = logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO
        
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(levelname)s] %(name)s - %(message)s")
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        logger.setLevel(level)
    
        logger.propagate = True
    return logger
