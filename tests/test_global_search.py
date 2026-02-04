import pytest
from src.services.search_service import SearchService

@pytest.fixture
def search_service():
    return SearchService()

def test_global_search_structure(search_service, mocker):
    
    # Simula retorno apenas para personagens e naves
    mock_people = {"results": [{"name": "Luke Skywalker", "url": ".../people/1/"}]}
    mock_ships = {"results": []} # Vazio para os outros
    
    # Mock do fetch_data retornando valores diferentes para cada chamada
    mocker.patch('src.services.client.Client.fetch_data', side_effect=[
        mock_people, # people
        mock_ships,  # planets
        mock_ships,  # starships
        mock_ships,  # vehicles
        mock_ships   # films
    ])

    result = search_service.global_search("Skywalker")

    assert result["termo_buscado"] == "Skywalker"
    assert "personagens" in result["resultados"]
    assert result["resultados"]["personagens"][0]["nome"] == "Luke Skywalker"

def test_global_search_success(client):
    headers = {'SW-API-KEY': 'test-secret-key'}
    response = client.get('/busca?q=luke', headers=headers)
    
    assert response.status_code == 200
    assert "personagens" in response.json['resultados']

def test_global_search_unauthorized(client):
    response = client.get('/busca?q=luke')
    
    assert response.status_code == 401
    assert response.json['erro'] == "Não autorizado"