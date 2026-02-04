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
            filmes_future = executor.map(self._fetch_film_title, film_urls)
            
            filmes = list(filmes_future)
        
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
            "detalhes_da_especie": {
                "detalhes": f"/personagem/{char_id}/especie",
            } if especie_nome != "Desconhecida" else {},
            "filmes": filmes,
        }
            
        self._save_to_cache(cache_key, formatted_char)
        return formatted_char
        
    def get_character_species_details(self, char_id):
            """Busca os detalhes completos da espécie de um personagem específico"""
            cache_key = f"char_{char_id}_species_full"
            cached = self._get_from_cache(cache_key)
            if cached: return cached

            char_data = Client.fetch_data(f"people/{char_id}")
            if not char_data:
                return {"erro": "Personagem não encontrado", "status": 404}

            species_urls = char_data.get("species", [])
            if not species_urls:
                return {"mensagem": "Este personagem não possui uma espécie específica registrada (provavelmente Humano).", "especie": None}

            species_id = species_urls[0].split("/")[-2]
            data = Client.fetch_data(f"species/{species_id}")
            
            if not data:
                return {"erro": "Detalhes da espécie não encontrados", "status": 404}

            formatted_species = {
                "personagem": char_data.get("name"),
                "nome_especie": data.get("name"),
                "classificacao": data.get("classification"),
                "designacao": data.get("designation"),
                "altura_media": data.get("average_height"),
                "cores_pele": data.get("skin_colors"),
                "cores_cabelo": data.get("hair_colors"),
                "cores_olhos": data.get("eye_colors"),
                "expectativa_vida": data.get("average_lifespan"),
                "linguagem": data.get("language"),
                "planeta_origem": self._fetch_summary(data.get("homeworld")) if data.get("homeworld") else "Desconhecido"
            }

            self._save_to_cache(cache_key, formatted_species)
            return formatted_species