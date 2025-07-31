import logging
from datetime import datetime

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(f"./logs/log_{str(datetime.now()).replace(' ', '_', 1)}.txt", "w")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("(%(asctime)s - %(levelname)s) %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)