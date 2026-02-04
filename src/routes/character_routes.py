from flask import Blueprint, jsonify, request
from src.auth import require_api_key
from src.services.character_service import CharacterService

character_bp = Blueprint('character_bp', __name__)
character_service = CharacterService()

@character_bp.route('/personagens', methods=['GET'])
def list_or_search_characters():
    nome = request.args.get('nome')
    if nome:
        return jsonify(character_service.search_characters(nome))
        
    page = request.args.get('page', 1, type=int)
    return jsonify(character_service.get_characters(page))

@character_bp.route('/personagem/<int:id>', methods=['GET'])
def character_details(id):
    return jsonify(character_service.get_character_details(id))

@character_bp.route('/personagem/<int:id>/especie', methods=['GET'])
@require_api_key
def get_species_details(id):
    return jsonify(character_service.get_character_species_details(id))
