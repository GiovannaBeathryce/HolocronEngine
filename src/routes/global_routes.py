from flask import Blueprint, jsonify, request
from src.auth import require_api_key
from src.services.search_service import SearchService

global_bp = Blueprint('global_bp', __name__)
search_service = SearchService()

@global_bp.route('/busca', methods=['GET'])
@require_api_key
def search_global():
    termo = request.args.get('q', '')
    return jsonify(search_service.global_search(termo))

@global_bp.route('/', methods=['GET'])
def index():
    return jsonify({
            "projeto": "Holocron SWAPI Engine",
            "versao": "1.0.0",
            "mensagem": "Bem-vindo à central de dados da galáxia. Use as rotas abaixo para explorar.",
            "guia_rapido": {
                "autenticacao": "Algumas rotas requerem o header 'SW-API-KEY'",
                "dica": "Adicione '?page=2' para navegar nos resultados."
            },
            "endpoints": {
                "publicos": [
                    {
                        "rota": "/personagens",
                        "metodo": "GET",
                        "descricao": "Lista todos os personagens (paginado)."
                    },
                    {
                        "rota": "/personagem/<id>",
                        "metodo": "GET",
                        "descricao": "Detalhes biográficos e técnicos de um personagem."
                    },

                    {
                        "rota": "/planetas",
                        "metodo": "GET",
                        "descricao": "Lista todos os planetas (paginado)."
                    },
                    {
                        "rota": "/planeta/<id>",
                        "metodo": "GET",
                        "descricao": "Detalhes geográficos e populacionais de um planeta."
                    }, 
                    {
                        "rota": "/naves",
                        "metodo": "GET",
                        "descricao": "Lista todas as naves espaciais (paginado)."
                    },
                    {
                        "rota": "/nave/<id>",
                        "metodo": "GET",
                        "descricao": "Detalhes técnicos de uma nave espacial."
                    },
                    {
                        "rota": "/veiculos",
                        "metodo": "GET",
                        "descricao": "Lista todos os veículos (paginado)."
                    },
                    {
                        "rota": "/veiculo/<id>",
                        "metodo": "GET",
                        "descricao": "Detalhes técnicos de um veículo."
                    },
                    {
                        "rota": "/filmes",
                        "metodo": "GET",
                        "descricao": "Lista todos os filmes da saga."
                    },
                    {
                        "rota": "/filme/<id>",
                        "metodo": "GET",
                        "descricao": "Detalhes e elenco de um filme específico."
                    }
                ],
                "protegidos": [
                    {
                        "rota": "/busca?q=<termo>",
                        "metodo": "GET",
                        "descricao": "Busca global paralela em todos os recursos.",
                        "recurso_extra": "Alta performance via Threading."
                    },
                    {
                        "rota": "/personagem/<id>/especie",
                        "metodo": "GET",
                        "descricao": "Detalhes biológicos da espécie de um personagem."
                    },
                    {
                        "rota": "/planeta/<id>/residents",
                        "metodo": "GET",
                        "descricao": "Lista residentes de um planeta específico."
                    },
                    {
                        "rota": "/filme/<id>/personagens",
                        "metodo": "GET",
                        "descricao": "Lista personagens que aparecem em um filme específico."
                    },
                    {
                        "rota": "/filme/<id>/planetas",
                        "metodo": "GET",
                        "descricao": "Lista planetas que aparecem em um filme específico."
                    },
                    {
                        "rota": "/filme/<id>/naves",
                        "metodo": "GET",
                        "descricao": "Lista naves espaciais que aparecem em um filme específico."
                    },
                    {
                        "rota": "/filme/<id>/veiculos",
                        "metodo": "GET",
                        "descricao": "Lista veículos que aparecem em um filme específico."
                    }
                ]
            },
            "documentacao_tecnica": {
                "linguagem": "Python 3.9",
                "cache": "Habilitado via Shelve (Persistente)",
                "logs": "Habilitados via Python Logging"
            }
        })

    # return jsonify({
    #     "projeto": "Holocrom SWAPI Wrapper",
    #     "versao": "1.0.0",
    #     "descricao": "Interface otimizada para consulta de dados do universo Star Wars",
    #     "menu_de_rotas": {
    #         "personagens": {
    #             "lista": "/personagens?page=1",
    #             "detalhes": "/personagem/<id>",
    #             "biologia": "/personagem/<id>/especie"
    #         },
    #         "planetas": {
    #             "lista": "/planetas?page=1",
    #             "detalhes": "/planeta/<id>"
    #         },
    #         "naves": {
    #             "lista": "/naves?page=1",
    #             "detalhes": "/nave/<id>"
    #         },
    #         "veiculos": {
    #             "lista": "/veiculos?page=1",
    #             "detalhes": "/veiculo/<id>"
    #         },
    #         "filmes": {
    #             "lista": "/filmes",
    #             "detalhes": "/filme/<id>",
    #             "sub_recursos": {
    #                 "personagens": "/filme/<id>/personagens",
    #                 "naves": "/filme/<id>/naves",
    #                 "planetas": "/filme/<id>/planetas"
    #             }
    #         },
    #         "busca_global": "/busca?q=<termo>"
    #     },
    #     "dica": "Use o parâmetro 'q' na rota de busca para pesquisar em tudo ao mesmo tempo!"
    # })