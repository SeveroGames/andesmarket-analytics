from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# 1. Configuración y Conexión a Base de Datos
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# 2. Inicializar FastAPI
app = FastAPI(
    title="AndesMarket Analytics API",
    description="API REST para consumir modelos de ML y KPIs de la base de datos",
    version="1.0.0"
)

# --- ENDPOINTS (RUTAS) ---

@app.get("/", tags=["Health"])
def health_check():
    """Verifica que la API esté funcionando correctamente."""
    return {"status": "ok", "mensaje": "🚀 AndesMarket API está en línea"}

@app.get("/api/v1/analytics/segments", tags=["Machine Learning"])
def get_segments_summary():
    """Obtiene un resumen de cuántos clientes hay en cada segmento K-Means."""
    try:
        with engine.connect() as conn:
            query = text("SELECT segmento_negocio, COUNT(*) as cantidad FROM segmentos_clientes GROUP BY segmento_negocio")
            result = conn.execute(query).fetchall()
            return {"data": [{"segmento": row[0], "clientes": row[1]} for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/churn/{id_cliente}", tags=["Machine Learning"])
def get_churn_risk(id_cliente: int):
    """Devuelve la probabilidad de abandono (Churn) de un cliente específico."""
    # 1. Hacemos la consulta a la BD dentro del try
    try:
        with engine.connect() as conn:
            query = text("SELECT probabilidad_abandono FROM predicciones_churn WHERE id_cliente = :id")
            result = conn.execute(query, {"id": id_cliente}).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # 2. Evaluamos el resultado FUERA del try
    if result:
        return {
            "id_cliente": id_cliente, 
            "riesgo_fuga_porcentaje": float(result[0]),
            "alerta": "ALTA" if result[0] > 50 else "BAJA"
        }
        
    # Si no hay resultado, lanzamos el 404 sin que el 'except' lo atrape
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.get("/api/v1/sales/anomalies", tags=["Ventas & Fraude"])
def get_recent_anomalies():
    """Devuelve las últimas 5 ventas detectadas como anomalías por Isolation Forest."""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT a.id_venta, a.score_anomalia, v.fecha 
                FROM anomalias_ventas a
                JOIN ventas v ON a.id_venta = v.id_venta
                WHERE a.es_anomalia = 1
                ORDER BY v.fecha DESC
                LIMIT 5
            """)
            result = conn.execute(query).fetchall()
            return {"ultimas_anomalias": [{"id_venta": row[0], "score": float(row[1]), "fecha": str(row[2])} for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))