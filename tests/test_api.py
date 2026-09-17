from fastapi.testclient import TestClient
from api.main import app

# Creamos un cliente de pruebas basado en nuestra app FastAPI
client = TestClient(app)

def test_health_check():
    """Prueba que el servidor esté vivo y respondiendo."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mensaje": "🚀 AndesMarket API está en línea"}

def test_get_segments_summary():
    """Prueba el endpoint de los segmentos de Machine Learning."""
    response = client.get("/api/v1/analytics/segments")
    
    # Verificamos que responda con éxito (HTTP 200 OK)
    assert response.status_code == 200
    
    # Verificamos que la respuesta contenga la llave "data"
    data = response.json()
    assert "data" in data
    
    # Verificamos que sea una lista
    assert isinstance(data["data"], list)

def test_get_churn_risk_valid_client():
    """Prueba el riesgo de fuga con un cliente que SÍ existe (ej. ID 15)."""
    # Usamos un ID de cliente que sabemos que existe en la base de datos
    response = client.get("/api/v1/analytics/churn/15")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "id_cliente" in data
    assert "riesgo_fuga_porcentaje" in data
    assert "alerta" in data
    assert data["id_cliente"] == 15

def test_get_churn_risk_invalid_client():
    """Prueba cómo reacciona la API ante un cliente que NO existe."""
    # Usamos un ID absurdamente alto para forzar un error 404
    response = client.get("/api/v1/analytics/churn/9999999")
    
    # Verificamos que la API maneje el error correctamente y no colapse
    assert response.status_code == 404
    assert response.json() == {"detail": "Cliente no encontrado"}