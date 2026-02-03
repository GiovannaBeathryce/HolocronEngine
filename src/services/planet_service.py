from concurrent.futures import ThreadPoolExecutor
from .base_service import BaseService
from .client import Client

class PlanetService(BaseService):
    def __init__(self):
        super().__init__(resource_name="planets")

    def get_planets(self, page=1):
        cache_key = f'{self.resource}_list_page_{page}'

        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        data = Client.fetch_data(self.resource, params={"page": page})
        if not data: 
            return {"erro": "Não foi possível carregar os planetas", "status": 500}
        
        formatted_results = {
            "total_planetas": data.get("count"),
            "proxima": f"/planetas?page={page + 1}" if data.get("next") else None,
            "anterior": f"/planetas?page={page - 1}" if data.get("previous") else None,
            "planetas": [
                {
                    "id": planet["url"].split("/")[-2],
                    "nome": planet["name"],
                    "clima": planet["climate"],
                } for planet in data.get("results")
            ]
        }
        
        self._save_to_cache(cache_key, formatted_results)
        return formatted_results
    
    def search_planets(self, query):
        data = Client.fetch_data(self.resource, params={"search": query})
        
        if not data or data.get("count") == 0:
            return {"erro": f"Nenhum planeta encontrado com '{query}'", "status": 404}

        return {
            "total_encontrados": data.get("count"),
            "planetas": [
                {
                    "id": p["url"].split("/")[-2],
                    "nome": p["name"],
                } for p in data.get("results")
            ]
        }
    
    def get_planet_details(self, planet_id):
        cache_key = f"{self.resource}_detail_{planet_id}"

        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        data = Client.fetch_data(f"{self.resource}/{planet_id}")
        if not data:
            return {"erro": "Planeta não encontrado", "status": 404}
        
        residents_urls = data.get("residents", [])
        residents_list = len(residents_urls)
        
        films_urls = data.get("films", [])

        with ThreadPoolExecutor() as executor:
            fetch_filmes = list(executor.map(self._fetch_film_title, films_urls))
            filmes = list(fetch_filmes)

        
        formatted_planet = {
            "id": planet_id,
            "nome": data.get("name"),
            "periodo_rotacao": data.get("rotation_period"),
            "periodo_orbital": data.get("orbital_period"),
            "diametro": data.get("diameter"),
            "clima": data.get("climate"),
            "gravidade": data.get("gravity"),
            "terreno": data.get("terrain"),
            "agua_superficial": data.get("surface_water"),
            "populacao": data.get("population"),
            "residentes": residents_list,
            "aparece_nos_filmes": filmes
        }
        
        self._save_to_cache(cache_key, formatted_planet)
        return formatted_planet
    
    def _fetch_resident_basic_info(self, resident_url):
        resident_id = resident_url.split("/")[-2]
        data = Client.fetch_data(f"people/{resident_id}")
        if data:
            return {"id": resident_id, "nome": data.get("name")} 

    def get_planet_residents(self, planet_id):
        cache_key = f"planet_{planet_id}_residents"

        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        data = Client.fetch_data(f"{self.resource}/{planet_id}")
        if not data:
            return {"erro": "Planeta não encontrado", "status": 404}
        
        residents_urls = data.get("residents", [])

        if not residents_urls:
            return {"planeta": data.get("name"), "residentes": [], "mensagem": "Este planeta não possui residentes conhecidos."} 
        
        with ThreadPoolExecutor() as executor:
            residentes = list(executor.map(self._fetch_resident_basic_info, residents_urls))

        residents_list = [resid for resid in residentes if resid is not None]        
    
        formatted_residents = {
            "planeta_id": planet_id,
            "nome_planeta": data.get("name"),
            "total_residentes": len(residents_list),
            "residentes": residents_list
        }
        
        self._save_to_cache(cache_key, formatted_residents)
        return formatted_residents
    