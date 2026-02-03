import shelve
import logging

logger = logging.getLogger(__name__)

class BaseService:
    def __init__(self, resource_name):
        self.resource = resource_name
        self.cache_file = 'holocron_cache'

    def _get_from_cache(self, key):
        with shelve.open(self.cache_file) as db:
            if key in db:
                logger.info(f"CACHE HIT: Recuperando {key}")
                return db[key]
            return None

    def _save_to_cache(self, key, data):
        with shelve.open(self.cache_file) as db:
            db[key] = data
            logger.info(f"CACHE SAVED: {key} armazenado.")