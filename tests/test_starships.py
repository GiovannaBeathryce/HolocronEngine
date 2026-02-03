import pytest
from src.services.starships_service import StarshipsService

@pytest.fixture
def starships_service():
    return StarshipsService()

def test_starship_service_inheritance(starships_service):
    """Verifica se StarshipService herdou corretamente da BaseService"""
    assert starships_service.resource == 'starships'
    assert hasattr(starships_service, '_fetch_film_title')

def test_get_starship_details_format(starships_service, mocker):
    """Testa se o dicionário de detalhes da nave vem com os campos técnicos corretos"""
    
    mock_ship_data = {
        "name": "Millennium Falcon",
        "model": "YT-1300 light freighter",
        "manufacturer": "Corellian Engineering Corporation",
        "cost_in_credits": "100000",
        "pilots": ["https://swapi.dev/api/people/13/"], # Han Solo
        "films": ["https://swapi.dev/api/films/1/"]
    }
    
    mock_pilot_data = {"name": "Han Solo"}

    mocker.patch('src.services.client.Client.fetch_data', side_effect=[
        mock_ship_data,  # Detalhes da nave
        mock_pilot_data  # Nome do piloto (dentro do map)
    ])
    
    # Mock do método de filmes que está na Base
    mocker.patch.object(StarshipsService, '_fetch_film_title', return_value="A New Hope")

    result = starships_service.get_starship_details("10")

    # Asserts
    assert result["nome"] == "Millennium Falcon"
    assert result["modelo"] == "YT-1300 light freighter"
    assert len(result["pilotos_notaveis"]) == 1
    assert result["pilotos_notaveis"][0]["nome"] == "Han Solo"
    assert result["aparece_nos_filmes"][0] == "A New Hope"