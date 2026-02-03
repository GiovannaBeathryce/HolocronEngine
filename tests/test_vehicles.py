import pytest
from src.services.vehicles_service import VehiclesService

@pytest.fixture
def vehicles_service():
    return VehiclesService()

def test_vehicle_service_inheritance(vehicles_service):
    assert vehicles_service.resource == 'vehicles'
    assert hasattr(vehicles_service, '_fetch_film_title')
    
def test_get_vehicle_details_format(vehicles_service, mocker):
    """Testa se os detalhes do veículo (ex: Sandcrawler) são processados corretamente"""
    
    # Mock da resposta da SWAPI para um Sandcrawler
    mock_vehicle_data = {
        "name": "Sandcrawler",
        "model": "Digger Crawler",
        "vehicle_class": "wheeled",
        "manufacturer": "Corellia Mining Corporation",
        "cost_in_credits": "150000",
        "pilots": [], # Geralmente vazio para veículos simples
        "films": ["https://swapi.dev/api/films/1/"]
    }
    
    # Mock do fetch_data
    mocker.patch('src.services.client.Client.fetch_data', return_value=mock_vehicle_data)
    
    # Mock do método de filmes da Base
    mocker.patch.object(VehiclesService, '_fetch_film_title', return_value="A New Hope")

    result = vehicles_service.get_vehicle_details("4")

    # Asserts
    assert result["nome"] == "Sandcrawler"
    assert result["classe_do_veiculo"] == "wheeled"
    assert "pilotos" in result
    assert result["aparece_nos_filmes"][0] == "A New Hope"