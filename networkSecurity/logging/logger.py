import logging
import os
from datetime import datetime

# Corrected log file naming with double quotes
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Logs directory path
logs_path = os.path.join(os.getcwd(), 'logs', LOG_FILE)
os.makedirs(os.path.dirname(logs_path), exist_ok=True)

# Full log file path
LOG_FILE_PATH = os.path.join(logs_path)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

# Example log
logging.info("Logging setup is complete.")
