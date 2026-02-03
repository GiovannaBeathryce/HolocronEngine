from .base_service import BaseService
from .client import Client
from concurrent.futures import ThreadPoolExecutor

class SearchService(BaseService):
    def __init__(self):
        super().__init__(resource_name='search')

    def global_search(self, query):
        if not query:
            return {"erro": "Termo de busca vazio", "status": 400}

        resources = {
            "personagens": "people",
            "planetas": "planets",
            "naves": "starships",
            "veiculos": "vehicles",
            "filmes": "films"
        }

        def fetch_category(category_name, swapi_resource):
            # A SWAPI suporta busca via parâmetro ?search=
            data = Client.fetch_data(swapi_resource, params={"search": query})
            results = data.get("results", []) if data else []
            
            return category_name, [
                {
                    "id": item["url"].strip("/").split("/")[-1],
                    "nome": item.get("name") or item.get("title"),
                    "tipo": category_name
                } for item in results
            ]

        with ThreadPoolExecutor() as executor:
            # Dispara as buscas em paralelo para todas as categorias
            futures = [executor.submit(fetch_category, name, res) for name, res in resources.items()]
            
            search_results = {}
            for future in futures:
                category, items = future.result()
                if items: # Só adiciona ao JSON se houver resultados
                    search_results[category] = items

        return {
            "termo_buscado": query,
            "total_categorias_com_sucesso": len(search_results),
            "resultados": search_results
        }