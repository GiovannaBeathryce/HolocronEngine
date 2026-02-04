import logging
import sys
import os

def setup_logging():
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if os.getenv('ENV') != 'production':
        handlers.append(logging.FileHandler("app.log"))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers
    )