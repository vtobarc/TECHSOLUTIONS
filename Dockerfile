# Usar una imagen base de Python
FROM python:3.11-slim

# Actualizar el sistema e instalar libmagic
RUN apt-get update && apt-get install -y libmagic-dev

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app/

# Crear un entorno virtual y activarlo
RUN python -m venv /opt/venv

# Instalar las dependencias
RUN /opt/venv/bin/pip install -r requirements.txt

# Establecer el PATH del entorno virtual para que gunicorn pueda ser encontrado
ENV PATH="/opt/venv/bin:$PATH"

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "dynamics.wsgi:application"]

