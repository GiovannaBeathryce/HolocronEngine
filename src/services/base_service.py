import shelve
import logging
from src.services.client import Client

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

    def _fetch_film_title(self, film_url):
        film_id = film_url.split("/")[-2]
        film_data = Client.fetch_data(f"films/{film_id}")
        return film_data.get("title") if film_data else "Filme Desconhecido"