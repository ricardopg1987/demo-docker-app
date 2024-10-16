# webapp/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias primero
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]