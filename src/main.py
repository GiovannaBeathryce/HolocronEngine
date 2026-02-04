import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from src.logger_config import setup_logging

load_dotenv()
setup_logging()

from src.routes.global_routes import global_bp
from src.routes.character_routes import character_bp
from src.routes.movie_routes import movie_bp
from src.routes.starship_routes import starship_bp
from src.routes.planet_routes import planet_bp
from src.routes.vehicle_routes import vehicle_bp

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"erro": "Rota não encontrada", "status": 404}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"erro": "Erro interno no servidor", "status": 500}), 500

app.register_blueprint(global_bp)
app.register_blueprint(character_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(starship_bp)
app.register_blueprint(planet_bp)
app.register_blueprint(vehicle_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
