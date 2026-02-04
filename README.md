# 🌌 Holocron Engine - Star Wars API Wrapper

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

O **Holocron Engine** é uma API middleware de alta performance construída em Python/Flask para consumir e otimizar dados da [SWAPI (Star Wars API)](https://swapi.dev/). O projeto demonstra padrões avançados de arquitetura, incluindo paralelismo, cache persistente e segurança via API Gateway.

## 🚀 Funcionalidades Principais

-   **Busca Global Paralela:** Utiliza `ThreadPoolExecutor` para realizar varreduras simultâneas em múltiplas categorias (Personagens, Naves, Planetas, etc).
-   **Sistema de Cache:** Implementação de cache persistente via `shelve` para reduzir a latência e o consumo da API de origem.
-   **Segurança:** Proteção de endpoints sensíveis através de autenticação por Header (`X-API-KEY`).
-   **Logs Estruturados:** Sistema de logging configurado para rastreabilidade de erros e monitoramento de performance.
-   **Cloud Ready:** Totalmente containerizado e pronto para deploy no Google Cloud Run.

## 🛠️ Arquitetura do Projeto

```text
src/
├── routes/          # Blueprints (Personagens, Filmes, Busca, etc)
├── services/        # Lógica de negócio e integração com SWAPI
├── auth.py          # Middleware de segurança
└── logger_config.py # Configuração central de monitoramento
docs/                # Guia de API e Postman Collection
tests/               # Testes unitários e de integração
``` 
## ⚙️ Instalação e Execução Local
**Pré-requisitos**
- Python 3.9 ou superior

- Docker (opcional)

**Passo a Passo**
1. **Clone o repositório:**
```
Bash
git clone [https://github.com/GiovannaBeathryce/HolocronEngine.git](https://github.com/GiovannaBeathryce/HolocronEngine.git)
cd HolocronEngine
```
2. **Configure o ambiente virtual e instale as dependências:**
```
Bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. **Configure as variáveis de ambiente:** Crie um arquivo `.env` na raiz com:
```
Snippet de código
API_KEY=sua_chave_secreta_aqui
ENV=development
```
4. **Execute a aplicação:**
``` 
Bash
python -m src.main
```
## 🧪 Testes
**Para rodar os testes unitários (garantindo que o pytest-env esteja instalado):**
```
Bash
pytest
```
## 🐳 Docker
**Para buildar e rodar o container localmente:**
```
Bash
docker build -t holocron-engine .
docker run -p 8080:8080 -e API_KEY=sua_chave_secreta_aqui holocron-engine
```
## 📖 Documentação da API
A documentação detalhada das rotas e a **Postman Collection** podem ser encontradas na pasta `/docs.`

**Exemplo de Uso (Busca Global)**
- Endpoint: `GET /busca?q=luke`
- Header: `X-API-KEY: sua_chave_secreta`

##      
Desenvolvido com ❤️ por [Giobanna Beathryce](https://github.com/GiovannaBeathryce).
