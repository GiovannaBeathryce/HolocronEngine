import os
from functools import wraps
from flask import request, jsonify

API_KEY = os.getenv('API_KEY')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not API_KEY:
            return jsonify({"erro": "Configuração de segurança pendente no servidor."}), 500

        user_key = request.headers.get('SW-API-KEY')
        
        if not user_key or user_key != API_KEY:
            return jsonify({
                "erro": "Não autorizado", 
                "mensagem": "Chave de API inválida ou ausente."
            }), 401
            
        return f(*args, **kwargs)
    return decorated_function