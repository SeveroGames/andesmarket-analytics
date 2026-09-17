import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Construir la URL de conexión
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def test_connection():
    try:
        # Crear el motor de conexión
        engine = create_engine(DATABASE_URL)
        
        # Probar la conexión ejecutando una consulta simple
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            
            print("✅ ¡Conexión exitosa a PostgreSQL!")
            print(f"📦 Versión de la Base de Datos: {version}")
            
    except Exception as e:
        print("❌ Error al conectar a la base de datos:")
        print(e)

if __name__ == "__main__":
    test_connection()