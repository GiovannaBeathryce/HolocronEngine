import os
import tempfile
import shelve
import logging
from src.services.client import Client

logger = logging.getLogger(__name__)

class BaseService:
    def __init__(self, resource_name):
        self.resource = resource_name
        temp_dir = tempfile.gettempdir()
        self.cache_file = os.path.join(temp_dir, 'holocron_cache')
        self.logger = logging.getLogger(self.__class__.__name__)

    def _get_from_cache(self, key):
        with shelve.open(self.cache_file) as db:
            if key in db:
                self.logger.info(f"CACHE HIT: Recuperando {key}")
                return db[key]
            self.logger.info(f"CACHE MISS: {key} não encontrado. Chamando API...")
            return None
        
    def _save_to_cache(self, key, data):
        with shelve.open(self.cache_file) as db:
            db[key] = data
            self.logger.info(f"CACHE SAVED: {key} armazenado.")

    def _fetch_film_title(self, film_url):
        film_id = film_url.split("/")[-2]
        film_data = Client.fetch_data(f"films/{film_id}")
        return film_data.get("title") if film_data else "Filme Desconhecido"
    
    def _fetch_summary(self, url):
        """
        Busca ID e Nome/Título de qualquer URL da SWAPI.
        """
        if not url: return None
        
        parts = url.strip("/").split("/")
        resource_type = parts[-2] 
        resource_id = parts[-1]   
        
        data = Client.fetch_data(f"{resource_type}/{resource_id}")
        if not data: return None

        return {
            "id": resource_id,
            "nome": data.get("name") or data.get("title")
        }
    