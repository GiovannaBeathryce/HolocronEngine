from flask import Blueprint, jsonify, request
from src.services.starships_service import StarshipsService

starship_bp = Blueprint('starship_bp', __name__)
starships_service = StarshipsService()

@starship_bp.route('/naves', methods=['GET'])
def list_starships():
    page = request.args.get('page', 1, type=int)
    return jsonify(starships_service.get_starships(page))

@starship_bp.route('/nave/<int:id>', methods=['GET'])
def starship_details(id):
    return jsonify(starships_service.get_starship_details(id))