from .base_service import BaseService
from .client import Client  
from concurrent.futures import ThreadPoolExecutor

class MovieService(BaseService):
    def __init__(self):
        super().__init__(resource_name='films')  
    
    def get_movies(self, page=1):
        """Lista paginada de filmes"""
        cache_key = f"{self.resource}_list_page_{page}"
        cached = self._get_from_cache(cache_key)
        if cached: return cached

        data = Client.fetch_data(f"films/?page={page}")
        if not data:
            return {"erro": "Nenhum filme encontrado", "status": 404}

        results = data.get("results", [])
        formatted_results = []
        for movie in results:
            formatted_results.append({
                "id": movie.get("url").split("/")[-2],
                "titulo": movie.get("title"),
                "episodio": movie.get("episode_id"),
            })

        result = {
        "total_de_personagens": data.get("count"),
        "proxima": f"/filmes?page={page + 1}" if data.get("next") else 'Não disponivel',
        "anterior": f"/filmes?page={page - 1}" if data.get("previous") else None,
            "total_filmes": data.get("count", 0),
            "filmes": formatted_results
        }
        self._save_to_cache(cache_key, result)
        return result

    def get_movie_basic_info(self, movie_id):
        """Apenas dados básicos do filme (Sinopse, Diretor, etc)"""
        cache_key = f"movie_basic_{movie_id}"
        cached = self._get_from_cache(cache_key)
        if cached: return cached

        data = Client.fetch_data(f"films/{movie_id}")
        if not data: return {"erro": "Filme não encontrado", "status": 404}

        formatted = {
            "titulo": data.get("title"),
            "episodio": data.get("episode_id"),
            "diretor": data.get("director"),
            "produtor": data.get("producer"),
            "sinopse": {
                "detalhes": data.get("opening_crawl"),
            },
            "lancamento": data.get("release_date"),
            "links_detalhes": {
                "personagens": f"/filme/{movie_id}/personagens",
                "planetas": f"/filme/{movie_id}/planetas",
                "naves": f"/filme/{movie_id}/naves",
                "veiculos": f"/filme/{movie_id}/veiculos",            }
        }
        self._save_to_cache(cache_key, formatted)
        return formatted

    def get_movie_related_resource(self, movie_id, resource_key):
        """
        Método genérico para buscar sub-recursos de um filme.
        resource_key pode ser 'characters', 'planets', 'starships', etc.
        """
        cache_key = f"movie_{movie_id}_{resource_key}"
        cached = self._get_from_cache(cache_key)
        if cached: return cached

        data = Client.fetch_data(f"films/{movie_id}")
        if not data or resource_key not in data:
            return {"erro": "Recurso não encontrado", "status": 404}

        urls = data.get(resource_key, [])
        with ThreadPoolExecutor() as executor:
            # Usamos o nosso novo _fetch_summary da BaseService!
            list_results = list(executor.map(self._fetch_summary, urls))

        result = {
            "filme": data.get("title"),
            "total": len(list_results),
            "dados": list_results
        }
        
        self._save_to_cache(cache_key, result)
        return result