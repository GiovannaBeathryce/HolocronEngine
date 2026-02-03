import logging
from flask import Flask, jsonify, request
from src.services.character_service import CharacterService
from src.services.planet_service import PlanetService
from src.services.starships_service import StarshipsService

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