import logging
from flask import Flask, jsonify, request
from src.services.character_service import CharacterService

app = Flask(__name__)

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

character_service = CharacterService()

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
        
