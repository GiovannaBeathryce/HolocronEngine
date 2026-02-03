import shelve
import logging
from concurrent.futures import ThreadPoolExecutor
from .base_service import BaseService
from .client import Client

logger = logging.getLogger(__name__)

class CharacterService(BaseService):
    def __init__(self):
        super().__init__(resource_name="people")

    def get_characters(self, page=1):
        cache_key = f"people_page_{page}"

        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data

            # Se não está no cache, busca na SWAPI
        logger.info(f"CACHE MISS: Buscando página {page} na SWAPI...")
        data = Client.fetch_data(self.resource, params={"page": page})

        if not data or "results" not in data:
            return {"erro": "Página não encontrada", "status": 404}
        
        formatted_results = {
        "total_de_personagens": data.get("count"),
        "proxima": f"/personagens?page={page + 1}" if data.get("next") else None,
        "anterior": f"/personagens?page={page - 1}" if data.get("previous") else None,
        "personagens": [
                {
                    "id": p["url"].split("/")[-2],
                    "nome": p["name"],
                } for p in data.get("results")
            ]
        }

        self._save_to_cache(cache_key, formatted_results)
        return formatted_results

    # Método auxiliar para buscar título de filme    
    def _fetch_film_title(self, film_url):
        film_id = film_url.split("/")[-2]
        film_data = Client.fetch_data(f"films/{film_id}")
        return film_data.get("title") if film_data else None    
    
    def get_character_details(self, char_id):
        cache_key = f"char_detail_{char_id}"
        
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data
            
        data = Client.fetch_data(f"{self.resource}/{char_id}")
        if not data:
            return {"erro": "Personagem não encontrado", "status": 404}

        # chamada do método auxiliar
        film_urls = data.get("films", [])
        with ThreadPoolExecutor() as executor:
            filmes = list(executor.map(self._fetch_film_title, film_urls))
        
        especie_nome = "Desconhecida"
        especie = data.get("species", [])
        if especie:
            especie_id = especie[0].split("/")[-2]
            especie_data = Client.fetch_data(f"species/{especie_id}")
            if especie_data:
                especie_nome = especie_data.get("name")
            
        planeta_natal = "Desconhecido"
        planeta_de_origem = data.get("homeworld")
        if planeta_de_origem:   
            planeta_id = planeta_de_origem.split("/")[-2]
            planeta_data = Client.fetch_data(f"planets/{planeta_id}")
            if planeta_data:
                planeta_natal = planeta_data.get("name")

        formatted_char = {
            "id": char_id,
            "nome": data.get("name"),
            "especie": especie_nome, 
            "ano_de_nascimento": data.get("birth_year"),
            "genero": data.get("gender"),
            "planeta_natal": planeta_natal,
            "informacoes_fisicas": {
                "altura": data.get("height"),
                "peso": data.get("mass"),
                "cor_do_cabelo": data.get("hair_color"),
                "cor_da_pele": data.get("skin_color"),
                "cor_dos_olhos": data.get("eye_color"),
            },
            "filmes": filmes,
        }
            
        self._save_to_cache(cache_key, formatted_char)
        return formatted_char
        
    def search_characters(self, query):
        """
            Listagem normal: localhost/personagens?page=1

            Busca específica: localhost/personagens?nome=skywalker

            Busca parcial: localhost/personagens?nome=lu (deve trazer Luke, Luminara, etc...)
        """

        data = Client.fetch_data("people", params={"search": query})
        
        if not data or data.get("count") == 0:
            return {"erro": f"Nenhum personagem encontrado com '{query}'", "status": 404}

        return {
            "total_encontrados": data.get("count"),
            "personagens": [
                {
                    "id": p["url"].split("/")[-2],
                    "nome": p["name"],
                } for p in data.get("results")
            ]
        }
    