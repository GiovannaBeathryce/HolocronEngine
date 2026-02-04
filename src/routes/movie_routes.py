from flask import Blueprint, jsonify, request
from src.services.movie_service import MovieService

movie_bp = Blueprint('movie_bp', __name__)
movie_service = MovieService()

@movie_bp.route('/filmes', methods=['GET'])
def list_movises():
    page = request.args.get('page', 1, type=int)
    return jsonify(movie_service.get_movies(page))

@movie_bp.route('/filme/<int:id>', methods=['GET'])
def basic_details_movies(id):
    return jsonify(movie_service.get_movie_basic_info(id))

@movie_bp.route('/filme/<int:id>/personagens', methods=['GET'])
def characters_of_movie(id):
    return jsonify(movie_service.get_movie_related_resource(id, 'characters'))

@movie_bp.route('/filme/<int:id>/planetas', methods=['GET'])
def planets_of_movie(id):
    return jsonify(movie_service.get_movie_related_resource(id, 'planets'))

@movie_bp.route('/filme/<int:id>/naves', methods=['GET'])
def starships_of_movie(id):
    return jsonify(movie_service.get_movie_related_resource(id, 'starships'))

@movie_bp.route('/filme/<int:id>/veiculos', methods=['GET'])
def vehicles_of_movie(id):
    return jsonify(movie_service.get_movie_related_resource(id, 'vehicles'))
