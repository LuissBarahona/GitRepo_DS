# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos y el código de la aplicación
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# Expone el puerto para Flask
EXPOSE 6000

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
