FROM debian:bullseye-slim

RUN apt-get update
RUN apt-get install python3 python3-pip libmariadb-dev \
    python3-dev -y

# Configuración de zona horaria.
ENV TZ=America/Mexico_City
RUN ln -snf  /etc/l/usr/share/zoneinfo/$TZocaltime && echo $TZ > /etc/timezone

# Entorno de desarrollo.
WORKDIR /app

COPY ./correspondencia/requirements.txt /app/

# Instalación de requerimientos
RUN pip3 install -r /app/requirements.txt

# Copea el código al entorno de Docker.
COPY ./correspondencia/ /app/

EXPOSE 8000

RUN python3 manage.py makemigrations usuarios
RUN python3 manage.py makemigrations ficha

# Comando ejecutado por defecto.
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
