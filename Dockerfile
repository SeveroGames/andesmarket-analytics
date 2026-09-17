# 1. Usar una imagen oficial de Python ligera como base
FROM python:3.12.4-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar solo el archivo de requerimientos primero (para optimizar caché)
COPY requirements.txt .

# 4. Instalar las dependencias del sistema y de Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código de la API al contenedor
COPY api/ ./api/

# 6. Exponer el puerto por donde escuchará FastAPI
EXPOSE 8000

# 7. Comando para arrancar el servidor cuando el contenedor inicie
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]