from flask import Blueprint, jsonify, request
from src.services.search_service import SearchService

global_bp = Blueprint('global_bp', __name__)
search_service = SearchService()

@global_bp.route('/busca', methods=['GET'])
def search_global():
    termo = request.args.get('q', '')
    return jsonify(search_service.global_search(termo))

@global_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        "projeto": "Holocrom SWAPI Wrapper",
        "versao": "1.0.0",
        "descricao": "Interface otimizada para consulta de dados do universo Star Wars",
        "menu_de_rotas": {
            "personagens": {
                "lista": "/personagens?page=1",
                "detalhes": "/personagem/<id>",
                "biologia": "/personagem/<id>/especie"
            },
            "planetas": {
                "lista": "/planetas?page=1",
                "detalhes": "/planeta/<id>"
            },
            "naves": {
                "lista": "/naves?page=1",
                "detalhes": "/nave/<id>"
            },
            "veiculos": {
                "lista": "/veiculos?page=1",
                "detalhes": "/veiculo/<id>"
            },
            "filmes": {
                "lista": "/filmes",
                "detalhes": "/filme/<id>",
                "sub_recursos": {
                    "personagens": "/filme/<id>/personagens",
                    "naves": "/filme/<id>/naves",
                    "planetas": "/filme/<id>/planetas"
                }
            },
            "busca_global": "/busca?q=<termo>"
        },
        "dica": "Use o parâmetro 'q' na rota de busca para pesquisar em tudo ao mesmo tempo!"
    })