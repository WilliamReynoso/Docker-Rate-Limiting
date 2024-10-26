FROM python:3

# Exponer puerto 5432
EXPOSE 5432

# Crear directorio para los scripts SQL
RUN mkdir -p /docker-entrypoint-initdb.d

# Copiar los scripts SQL al entrypoint del contenedor
COPY ./scripts/query_base.sql /docker-entrypoint-initdb.d/

# Instalar dependencias de Python
RUN pip install flask psycopg2 Flask-Limiter

WORKDIR /code 

COPY ./code /code

CMD ["flask","run","--host=0.0.0.0"]

