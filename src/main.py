import logging
from flask import Flask, jsonify, request
from src.services.character_service import CharacterService
from src.services.planet_service import PlanetService
from src.services.starships_service import StarshipsService
from src.services.vehicles_service import VehiclesService
from src.services.movie_service import MovieService
from src.services.search_service import SearchService

app = Flask(__name__)

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

character_service = CharacterService()
planet_service = PlanetService()
starshipsService = StarshipsService()
vehicles_service = VehiclesService()
movie_service = MovieService()
search_service = SearchService()

@app.route('/personagens', methods=['GET'])
def list_or_search_characters():
    nome = request.args.get('nome')
    if nome:
        return jsonify(character_service.search_characters(nome))
        
    page = request.args.get('page', 1, type=int)
    return jsonify(character_service.get_characters(page))

@app.route('/personagem/<int:id>', methods=['GET'])
def detalhes(id):
    return jsonify(character_service.get_character_details(id))

@app.route('/personagem/<int:id>/especie', methods=['GET'])
def detalhes_especie_personagem(id):
    return jsonify(character_service.get_character_species_details(id))
        
@app.route('/planetas', methods=['GET'])
def list_or_search_planets():
    nome = request.args.get('nome')
    if nome:
        return jsonify(planet_service.search_planets(nome))
    page = request.args.get('page', 1, type=int)
    return jsonify(planet_service.get_planets(page))

@app.route('/planeta/<int:id>', methods=['GET'])
def planet_details(id):
    return jsonify(planet_service.get_planet_details(id))

@app.route('/planeta/<int:planet_id>/residentes', methods=['GET'])
def list_residents(planet_id):
    return jsonify(planet_service.get_planet_residents(planet_id))

@app.route("/naves", methods=['GET'])
def list_starships():
    page = request.args.get('page', 1, type=int)
    return jsonify(starshipsService.get_starships(page))

@app.route('/nave/<int:id>', methods=['GET'])
def starship_details(id):
    return jsonify(starshipsService.get_starship_details(id))

@app.route('/veiculos', methods=['GET'])
def list_vehicles():
    page = request.args.get('page', 1, type=int)
    return jsonify(vehicles_service.get_vehicles(page))

@app.route('/veiculo/<int:id>', methods=['GET'])
def vehicle_details(id):
    return jsonify(vehicles_service.get_vehicle_details(id))

@app.route("/filmes", methods=['GET'])
def list_movises():
    page = request.args.get('page', 1, type=int)
    return jsonify(movie_service.get_movies(page))

@app.route('/filme/<int:id>', methods=['GET'])
def basic_details_movies(id):
    return jsonify(movie_service.get_movie_basic_info(id))

@app.route('/filme/<int:id>/personagens', methods=['GET'])
def characters_of_movie(id):
    return jsonify(movie_service.get_movie_related_resource(id, 'characters'))

@app.route('/filme/<int:id>/planetas', methods=['GET'])
def planets_of_movie(id):
    return jsonify(movie_service.get_movie_related_resource(id, 'planets'))

@app.route('/filme/<int:id>/naves', methods=['GET'])
def starships_of_movie(id):
    return jsonify(movie_service.get_movie_related_resource(id, 'starships'))

@app.route('/filme/<int:id>/veiculos', methods=['GET'])
def vehicles_of_movie(id):
    return jsonify(movie_service.get_movie_related_resource(id, 'vehicles'))

@app.route('/busca', methods=['GET'])
def search_global():
    termo = request.args.get('q', '')
    return jsonify(search_service.global_search(termo))