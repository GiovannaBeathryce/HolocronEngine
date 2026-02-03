import pytest
from src.services.planet_service import PlanetService

@pytest.fixture
def planet_service():
    return PlanetService()

def test_planet_service_resource_name(planet_service):
    """Verifica se o recurso foi definido corretamente como 'planets'"""
    assert planet_service.resource == 'planets'

def test_planet_service_has_base_methods(planet_service):
    """Verifica se herdou os métodos da BaseService"""
    assert hasattr(planet_service, '_fetch_film_title')
    assert hasattr(planet_service, '_get_from_cache')

def test_get_planet_details_structure(planet_service, mocker):
    """Testa se a estrutura de retorno do planeta está correta (usando Mock)"""
    
    mock_planet_data = {
        "name": "Tatooine",
        "climate": "arid",
        "terrain": "desert",
        "population": "200000",
        "residents": ["https://swapi.dev/api/people/1/"],
        "films": ["https://swapi.dev/api/films/1/"]
    }
    
    mocker.patch('src.services.client.Client.fetch_data', return_value=mock_planet_data)
    mocker.patch.object(PlanetService, '_fetch_film_title', return_value="A New Hope")
    mocker.patch.object(PlanetService, '_fetch_resident_basic_info', return_value={"id": "1", "nome": "Luke Skywalker"})

    result = planet_service.get_planet_details("1")

    assert result["nome"] == "Tatooine"
    assert "residentes" in result
    assert result["aparece_nos_filmes"][0] == "A New Hope"
    assert result["residentes"] > 0