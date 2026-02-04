FROM python:3.9-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Expõe a porta do Cloud Run
ENV PORT=8080
EXPOSE 8080

# Executa usando o caminho do módulo Python
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 "src.main:app"