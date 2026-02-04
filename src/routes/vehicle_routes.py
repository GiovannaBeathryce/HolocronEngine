from flask import Blueprint, jsonify, request
from src.services.vehicles_service import VehiclesService

vehicle_bp = Blueprint('vehicle_bp', __name__)
vehicles_service = VehiclesService()

@vehicle_bp.route('/veiculos', methods=['GET'])
def list_vehicles():
    page = request.args.get('page', 1, type=int)
    return jsonify(vehicles_service.get_vehicles(page))

@vehicle_bp.route('/veiculo/<int:id>', methods=['GET'])
def vehicle_details(id):
    return jsonify(vehicles_service.get_vehicle_details(id))
