# Usar una imagen base de Python
FROM python:3.11-slim

# Actualizar el sistema y instalar libmagic
RUN apt-get update && apt-get install -y libmagic-dev

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app/

# Crear un entorno virtual y activar
RUN python -m venv /opt/venv
RUN . /opt/venv/bin/activate

# Instalar las dependencias
RUN /opt/venv/bin/pip install -r requirements.txt

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "dynamics.wsgi:application"]
