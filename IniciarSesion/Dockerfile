# Usar la imagen base de Python
FROM python:3.8-slim

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Verificar variables de entorno
RUN echo "Database Host: $DATABASE_HOST" && \
    echo "Database Name: $DATABASE_NAME" && \
    echo "Database User: $DATABASE_USER" && \
    echo "Database Password: $DATABASE_PASSWORD"

# Exponer el puerto en el que Flask correrá
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python3", "app.py"]
