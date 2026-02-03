import pytest
from src.services.movie_service import MovieService

@pytest.fixture
def movie_service():
    return MovieService()

def test_movie_basic_info_format(movie_service, mocker):
    """Garante que as informações básicas e os links de detalhes estão presentes"""
    mock_movie = {
        "title": "A New Hope",
        "episode_id": 4,
        "director": "George Lucas",
        "release_date": "1977-05-25"
    }
    mocker.patch('src.services.client.Client.fetch_data', return_value=mock_movie)

    result = movie_service.get_movie_basic_info("1")

    assert result["titulo"] == "A New Hope"
    assert "links_detalhes" in result
    assert result["links_detalhes"]["personagens"] == "/filme/1/personagens"

def test_get_movie_characters_list(movie_service, mocker):
    """Testa a busca paralela de personagens de um filme específico"""
    
    # 1. Dados do filme com lista de URLs de personagens
    mock_movie_data = {
        "title": "A New Hope",
        "characters": [
            "https://swapi.dev/api/people/1/", # Luke
            "https://swapi.dev/api/people/2/"  # C-3PO
        ]
    }

    # 2. Respostas individuais para cada chamada do _fetch_summary
    mocker.patch('src.services.client.Client.fetch_data', side_effect=[
        mock_movie_data,
        {"name": "Luke Skywalker"},
        {"name": "C-3PO"}
    ])

    result = movie_service.get_movie_related_resource("1", "characters")

    assert result["filme"] == "A New Hope"
    assert result["total"] == 2
    assert result["dados"][0]["nome"] == "Luke Skywalker"
    assert result["dados"][1]["id"] == "2"