import logging 
import logging.config
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DIR="logs"
LOG_FILE=os.getenv("LOG_FILE", "orchestrator.log")

Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'stream': sys.stdout,
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, LOG_FILE),
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

def setup_logging():
    """Setup logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)