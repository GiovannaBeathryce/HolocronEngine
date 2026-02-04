from flask import Blueprint, jsonify, request
from src.auth import require_api_key
from src.services.planet_service import PlanetService

planet_bp = Blueprint('planet_bp', __name__)
planet_service = PlanetService()

@planet_bp.route('/planetas', methods=['GET'])
def list_or_search_planets():
    nome = request.args.get('nome')
    if nome:
        return jsonify(planet_service.search_planets(nome))
    page = request.args.get('page', 1, type=int)
    return jsonify(planet_service.get_planets(page))

@planet_bp.route('/planeta/<int:id>', methods=['GET'])
def planet_details(id):
    return jsonify(planet_service.get_planet_details(id))

@planet_bp.route('/planeta/<int:id>/residentes', methods=['GET'])
@require_api_key
def list_residents(id):
    return jsonify(planet_service.get_planet_residents(id))
