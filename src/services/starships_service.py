from .base_service import BaseService
from .client import Client
from concurrent.futures import ThreadPoolExecutor

class StarshipsService(BaseService):
    def __init__(self):
        super().__init__(resource_name='starships')

    def get_starships(self, page=1):
        cache_key = f"{self.resource}_list_page_{page}"
        cached_data = self._get_from_cache(cache_key)    
        if cached_data:
            return cached_data
        
        data = Client.fetch_data(self.resource, params={'page': page})
        if not data:
            return {"erro": "Não foi possível carregar as naves estelares.", "status":500}
        
        formatted_results = {
            "total_naves": data.get("count"),
            "proxima": f"/naves?page={page + 1}" if data.get("next") else None,
            "anterior": f"/naves?page={page - 1}" if data.get("previous") else None,
            "naves": [
                {
                    "id": s["url"].split("/")[-2],
                    "nome": s["name"],
                    "modelo": s["model"]
                } for s in data.get("results")
            ]
        }

        self._save_to_cache(cache_key, formatted_results)
        return formatted_results
    
    def get_starship_details(self, starship_id):
        cache_key = f"{self.resource}_detail_{starship_id}"
        cached = self._get_from_cache(cache_key)
        if cached: return cached

        data = Client.fetch_data(f"{self.resource}/{starship_id}")
        if not data:
            return {"erro": "Nave não encontrada", "status": 404}

        pilot_urls = data.get("pilots", [])
        film_urls = data.get("films", [])

        with ThreadPoolExecutor() as executor:
            filmes_future = executor.map(self._fetch_film_title, film_urls)
            # um pequeno helper lambda para buscar nomes de pilotos
            pilotos_future = executor.map(
                lambda url: {"id": url.split("/")[-2], "nome": Client.fetch_data(f"people/{url.split('/')[-2]}").get("name")}, 
                pilot_urls
            )
            
            filmes = list(filmes_future)
            pilotos = list(pilotos_future)

        formatted_ship = {
            "id": starship_id,
            "nome": data.get("name"),
            "numero_de_passageiros": data.get("passengers"),
            "modelo": data.get("model"),
            "fabricante": data.get("manufacturer"),
            "custo_em_creditos": data.get("cost_in_credits"),
            "comprimento": data.get("length"),
            "velocidade_maxima_atmosfera": data.get("max_atmosphering_speed"),
            "equipe_tecnica": data.get("crew"),
            "classe_de_nave_estelar": data.get("starship_class"),
            "capacidade_carga": data.get("cargo_capacity"),
            "classe_hiperdrive": data.get("hyperdrive_rating"),
            "pilotos_notaveis": pilotos,
            "aparece_nos_filmes": filmes
        }
        
        self._save_to_cache(cache_key, formatted_ship)
        return formatted_ship