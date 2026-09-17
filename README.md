# 🛒 AndesMarket Analytics: End-to-End Data & ML Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.0-336791?logo=postgresql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-F7931E?logo=scikit-learn&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?logo=powerbi&logoColor=black)

Este repositorio contiene un proyecto completo de datos (End-to-End) que simula la infraestructura tecnológica de un negocio de retail de tamaño medio (**AndesMarket**). 

El proyecto abarca todo el ciclo de vida de los datos: desde la ingesta de archivos crudos, normalización en bases de datos relacionales, análisis estadístico, entrenamiento de modelos de Machine Learning, visualización ejecutiva, hasta su puesta en producción a través de una API empaquetada con Docker.

---

## 🏗️ Arquitectura y Stack Tecnológico

El proyecto se divide en 4 grandes pilares:

1. **Ingeniería de Datos (Data Engineering):**
   * **PostgreSQL:** Base de datos relacional para almacenamiento robusto.
   * **SQL Avanzado:** Uso de CTEs y Window Functions (`RANK`, `LAG`, `PARTITION BY`) para la creación de Vistas analíticas y KPIs pre-calculados (MoM Growth).
   * **Python (Pandas, SQLAlchemy):** Creación de un script ETL para extraer datos CSV, limpiarlos y cargarlos a la BD.

2. **Ciencia de Datos (Data Science & ML):**
   * **Análisis Estadístico:** Pruebas de hipótesis (T-Test) para evaluar significancia estadística entre diferentes regiones de ventas.
   * **Scikit-Learn & XGBoost:** Modelos entrenados localmente y guardados en base de datos.

3. **Business Intelligence (Visualización):**
   * **Power BI:** Conexión directa a PostgreSQL mediante un esquema de estrella (Star Schema) y uso de medidas DAX para seguimiento en tiempo real.

4. **Despliegue y Backend (MLOps):**
   * **FastAPI & Uvicorn:** Creación de una API RESTful para servir las predicciones de los modelos a otros sistemas.
   * **Pytest:** Pruebas unitarias (Unit Testing) para garantizar la estabilidad de los endpoints.
   * **Docker & Docker Compose:** Empaquetado de la API para garantizar un entorno agnóstico (funciona igual en cualquier servidor).

---

## 📈 Casos de Uso de Negocio (El "Por Qué")

Los modelos de Machine Learning implementados resuelven problemas reales de negocio:

* 👥 **Segmentación de Clientes (K-Means + RFM):** Clasificación automática de clientes en *VIPs, Frecuentes, Ocasionales y En Riesgo* según su Recencia, Frecuencia y Valor Monetario, permitiendo campañas de marketing dirigidas.
* 🚪 **Predicción de Abandono (Churn Prediction - Random Forest):** Algoritmo de clasificación que detecta con anticipación la probabilidad (%) de que un cliente deje de comprar, ayudando a la retención proactiva.
* 🔮 **Forecasting de Ventas (XGBoost):** Predicción de los ingresos diarios futuros utilizando variables temporales (Lags y Medias Móviles de 7 días).
* 🚨 **Detección de Fraude/Anomalías (Isolation Forest):** Identificación automatizada del 1% de las transacciones más atípicas (compras masivas institucionales o posibles errores del sistema).

---

## 📂 Estructura del Proyecto

```text
andesmarket-analytics/
├── api/
│   ├── main.py                  # Código fuente de FastAPI (Endpoints)
├── data/
│   └── raw/                     # Archivos CSV originales (fuente de datos)
├── notebooks/
│   ├── 01_eda.ipynb                     # Exploratory Data Analysis
│   ├── 02_statistical_analysis.ipynb    # Pruebas de Hipótesis (T-Test)
│   ├── 03_customer_segmentation.ipynb   # K-Means (Segmentación)
│   ├── 04_sales_forecasting.ipynb       # XGBoost (Series de Tiempo)
│   ├── 05_anomaly_detection.ipynb       # Isolation Forest
│   └── 06_churn_prediction.ipynb        # Random Forest Classifier
├── sql/
│   ├── schema.sql               # DDL para creación de tablas
│   └── advanced_views.sql       # Vistas con Window Functions y CTEs
├── tests/
│   └── test_api.py              # Pruebas unitarias de los endpoints (Pytest)
├── .env.example                 # Plantilla de variables de entorno
├── docker-compose.yml           # Orquestación del contenedor
├── Dockerfile                   # Configuración de la imagen de la API
├── requirements.txt             # Dependencias de Python
└── src/
    └── etl.py                   # Script de extracción, limpieza y carga


🚀 Guía de Instalación y Uso (Local)
Sigue estos pasos para replicar el proyecto en tu máquina local.

1. Clonar el repositorio e instalar dependencias
git clone [https://github.com/](https://github.com/)<TU_USUARIO_DE_GITHUB>/andesmarket-analytics.git
cd andesmarket-analytics

# Crear y activar entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt


2. Configurar la Base de Datos
Debes tener PostgreSQL instalado.

Crea un archivo .env en la raíz del proyecto basándote en .env.example.

Incluye tus credenciales (Usuario, Contraseña, Host, Puerto, Nombre de BD).

Ejecuta los scripts de la carpeta /sql en tu motor PostgreSQL para crear el esquema y las vistas.

Corre el ETL para poblar la base de datos: python src/etl.py


3. Ejecutar las Pruebas Unitarias (Testing)
Para verificar que el sistema funciona correctamente antes de levantar la API:

python -m pytest tests/test_api.py -v


4. Desplegar la API con Docker (Producción)
Si tienes Docker Desktop instalado, puedes levantar la aplicación completa con un solo comando:

docker-compose up -d --build

Nota: Si estás ejecutando Docker localmente, asegúrate de cambiar DB_HOST=host.docker.internal en tu archivo .env para que el contenedor pueda leer tu base de datos de PostgreSQL.


👨‍💻 Autor
Andres Stevn Chichande

Data Analyst / Data Scientist

https://www.linkedin.com/in/andres-chichande-rodriguez/