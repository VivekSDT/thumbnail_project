import os
from dotenv import load_dotenv
from logger_config import get_logger

log = get_logger("config")

def load_config():
    """Loads .env file as base config"""
    load_dotenv()

    config = {
        "producer_dir": os.getenv("PRODUCER_DIR", "producer"),
        "consumer_dir": os.getenv("CONSUMER_DIR", "consumer"),
        "thumbnail_size": (
            int(os.getenv("THUMBNAIL_WIDTH", 128)),
            int(os.getenv("THUMBNAIL_HEIGHT", 128))
        ),
        "check_interval": int(os.getenv("CHECK_INTERVAL", 3)),
        "idle_timeout": int(os.getenv("IDLE_TIMEOUT", 20)),
        "batch_size": int(os.getenv("BATCH_SIZE", 1)),
        "num_consumers": int(os.getenv("NUM_CONSUMERS", 1))
    }

    log.info("Loaded configuration from environment variables")
    return config
