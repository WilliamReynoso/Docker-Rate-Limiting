import os
import psycopg2
from psycopg2 import sql
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

# Configuración de Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=os.getenv("RATELIMIT_DEFAULT", "10 per hour"),  # Límite global (ejemplo: 10 peticiones por hora)
    headers_enabled=os.getenv("RATELIMIT_HEADERS_ENABLED", "true").lower() in ["true", "1"]
)

# Configuración de la conexión a la base de datos
def get_db_connection():
    connection = psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB","none"),
        user=os.getenv("POSTGRES_USER", "none"),
        password=os.getenv("POSTGRES_PASSWORD", "none")
    )
    return connection

@app.route('/')
@limiter.limit("3 per minute")
def home():
    return "Hello world!\nAqui tienes un limite de 3 peticiones por minuto :)"

@app.route('/pagina')
def pagina():
    return "Esta es la página en el endpoint /pagina.\nSin limite especifico pero es Afectado por el limite global de 10 por hora c:"

@app.route('/usuarios')
@limiter.limit("2 per minute")  # Limitar la consulta de usuarios a 10 por hora
def usuarios():
    # Función para obtener la lista de usuarios de la base de datos
    try:
        # Establece la conexión con la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        # Consulta para obtener los usuarios
        query = sql.SQL("SELECT * FROM users")
        # Ejecuta la consulta
        cursor.execute(query)
        # Obtén todos los resultados
        users = cursor.fetchall()     
        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return {"error": str(e)}

    return users

@app.route('/usuarios/torre')
@limiter.limit("3 per minute")  # Limitar la consulta específica de usuarios a 3 por hora
def usuariostorre():
    # Función para obtener la lista de usuarios de la base de datos
    try:
        # Establece la conexión con la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        # Consulta para obtener los usuarios
        query = sql.SQL("SELECT * FROM users WHERE device = 'desktop'")
        # Ejecuta la consulta
        cursor.execute(query)
        # Obtén todos los resultados
        users = cursor.fetchall()     
        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return {"error": str(e)}

    return users

# Manejo de usuarios bloqueados por exceder el límite
@app.errorhandler(429)
def ratelimit_handler(e):
    return {"error": "Limite de peticiones excedido. Intentelo de nuevo más tarde.  " + str(e)}, 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
