from .base_service import BaseService
from .client import Client
from concurrent.futures import ThreadPoolExecutor

class VehiclesService(BaseService):
    def __init__(self):
        super().__init__(resource_name="vehicles")

    def get_vehicles(self, page=1):
        cache_key = f"{self.resource}_list_page_{page}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        data = Client.fetch_data(self.resource, params={"page": page})
        if not data:
            return {"erro": "Não foi possível carregar a lista de veículos.", "status": 500}
        
        formatted_results = {
            "total_veiculos": data.get("count"),
            "proxima": f"/veiculos?page={page + 1}" if data.get("next") else None,
            "anterior": f"/veiculos?page={page - 1}" if data.get("previous") else None,
            "veiculos": [
                {
                    "id": veiculo["url"].split("/")[-2],
                    "nome": veiculo["name"],
                    "modelo": veiculo["model"],
                    "classe_do_veiculo": veiculo["vehicle_class"],
                } for veiculo in data.get("results")
            ]
        }

        self._save_to_cache(cache_key, formatted_results)
        return formatted_results
    
    def get_vehicle_details(self, vehicle_id):
        cache_key = f"{self.resource}_detail_{vehicle_id}"
        cached = self._get_from_cache(cache_key)
        if cached: return cached

        data = Client.fetch_data(f"{self.resource}/{vehicle_id}")
        if not data:
            return {"erro": "Veiculo não encontrado", "status": 404}

        # Buscas paralelas para Filmes e Pilotos
        pilot_urls = data.get("pilots", [])
        film_urls = data.get("films", [])

        with ThreadPoolExecutor() as executor:
            filmes_future = executor.map(self._fetch_film_title, film_urls)
            pilotos_future = executor.map(
                lambda url: {"id": url.split("/")[-2], "nome": Client.fetch_data(f"people/{url.split('/')[-2]}").get("name")}, 
                pilot_urls
            )
            
            filmes = list(filmes_future)
            pilotos = list(pilotos_future)

        formatted_vehicle = {
            "id": vehicle_id,
            "nome": data.get("name"),
            "modelo": data.get("model"),
            "fabricante": data.get("manufacturer"),
            "custo_em_creditos": data.get("cost_in_credits"),
            "comprimento": data.get("length"),
            "velocidade_maxima_atmosfera": data.get("max_atmosphering_speed"),
            "equipe_tecnica": data.get("crew"),
            "passageiros": data.get("passengers"),
            "capacidade_carga": data.get("cargo_capacity"),
            "suprimentos": data.get("consumables"),
            "classe_do_veiculo": data.get("vehicle_class"),
            "pilotos": pilotos,
            "aparece_nos_filmes": filmes
        }
        
        self._save_to_cache(cache_key, formatted_vehicle)
        return formatted_vehicle