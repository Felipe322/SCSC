FROM debian:bullseye-slim

RUN apt-get update
RUN apt-get install python3 python3-pip libmariadb-dev \
    python3-dev -y

# Configuración de zona horaria.
ENV TZ=America/Mexico_City
RUN ln -snf  /etc/l/usr/share/zoneinfo/$TZocaltime && echo $TZ > /etc/timezone

# Entorno de desarrollo.
WORKDIR /app

# Agrega archivo de requerimientos.
COPY ./correspondencia/requirements.txt /app/

# Instalación de requerimientos.
RUN pip3 install -r /app/requirements.txt

# Copea el código al entorno de Docker.
COPY ./correspondencia/ /app/

# Puerto expuesto del contenedor al host.
EXPOSE 8000

# Realiza migraciones de la base de datos.
RUN python3 manage.py makemigrations usuarios
RUN python3 manage.py makemigrations ficha

RUN python3 manage.py createsuperuser
# Crea un alias llamado run para correr Django.
RUN echo 'alias mig="python3 manage.py migrate"' >> ~/.bashrc

# Crea un alias llamado cs para crear super usuario en Django.
RUN echo 'alias cs="python3 manage.py createsuperuser"' >> ~/.bashrc

# Crea un alias llamado run para correr Django.
RUN echo 'alias run="python3 manage.py runserver 0.0.0.0:8001"' >> ~/.bashrc

# Comando ejecutado por defecto.
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
