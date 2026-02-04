from flask import Flask
from src.logger_config import setup_logging

setup_logging()

from src.routes.global_routes import global_bp
from src.routes.character_routes import character_bp
from src.routes.movie_routes import movie_bp
from src.routes.starship_routes import starship_bp
from src.routes.planet_routes import planet_bp
from src.routes.vehicle_routes import vehicle_bp

app = Flask(__name__)

app.register_blueprint(global_bp)
app.register_blueprint(character_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(starship_bp)
app.register_blueprint(planet_bp)
app.register_blueprint(vehicle_bp)
