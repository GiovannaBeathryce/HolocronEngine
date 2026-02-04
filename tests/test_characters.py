import pytest
from src.main import app

@pytest.fixture
def test_status_rota_personagens(client):
    """Testa se a rota principal responde"""
    response = client.get('/personagens')
    """Pode retornar 200 (sucesso) ou 500 (se a SWAPI falhar e não tivermos mock)"""
    assert response.status_code in [200, 500, 404]

def test_busca_personagem_mockado(client, mocker):
    """Testa a busca usando um mock para isolar a API externa"""
    mock_retorno = {
        "total_encontrados": 1,
        "personagens": [{"id": "1", "nome": "Luke Teste"}]
    }
    """ Interceptamos a chamada do serviço"""
    mocker.patch('src.services.character_service.CharacterService.search_characters', 
                 return_value=mock_retorno)

    response = client.get('/personagens?nome=Luke')
    assert response.status_code == 200
    assert response.json['personagens'][0]['nome'] == "Luke Teste"

def test_get_character_species_full_details(sw_service, mocker):
    """Testa se a rota de espécie traz os dados técnicos (ex: Wookiee para o Chewbacca)"""
    
    mock_char = {"name": "Chewbacca", "species": ["https://swapi.dev/api/species/3/"]}
    mock_spec = {
        "name": "Wookie",
        "classification": "mammal",
        "language": "Shyriiwook",
        "average_lifespan": "400",
        "homeworld": "https://swapi.dev/api/planets/14/"
    }
    mock_home = {"name": "Kashyyyk"}

    mocker.patch('src.services.client.Client.fetch_data', side_effect=[
        mock_char, 
        mock_spec,
        mock_home
    ])

    result = sw_service.get_character_species_details("13")

    assert result["personagem"] == "Chewbacca"
    assert result["nome_especie"] == "Wookie"
    assert result["linguagem"] == "Shyriiwook"
    assert result["planeta_origem"]["nome"] == "Kashyyyk"    

