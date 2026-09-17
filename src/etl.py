import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

print("🚀 Iniciando proceso ETL...")

def load_table(csv_name, table_name, column_mapping, date_columns=None, custom_transform=None):
    file_path = f"data/raw/{csv_name}"
    print(f"📥 Extrayendo datos de {csv_name}...")
    df = pd.read_csv(file_path)
    
    # Limpieza básica de nombres de columnas
    df.columns = df.columns.str.strip().str.lower()
    
    print(f"⚙️ Transformando {table_name}...")
    df = df.rename(columns=column_mapping)
    
    # Formateo de fechas (agregamos dayfirst=True para formato DD/MM/YYYY)
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                
    # Aplicar transformaciones específicas si existen
    if custom_transform:
        df = custom_transform(df)
        
    print(f"📤 Cargando {len(df)} filas en la tabla '{table_name}'...")
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"✅ {table_name} cargada exitosamente.\n")
    except Exception as e:
        print(f"❌ Error al cargar {table_name}: {e}\n")


# --- FUNCIONES DE TRANSFORMACIÓN ESPECÍFICAS ---
def transform_productos(df):
    # 1. Reemplazar comas por puntos en el precio y convertir a decimal (float)
    if df['precio_unitario'].dtype == 'object':
        df['precio_unitario'] = df['precio_unitario'].str.replace(',', '.').astype(float)
        
    # 2. Mapear los nombres de categorías a sus IDs numéricos
    cat_map = {
        'lácteos': 1, 'carnicería': 2, 'panadería': 3, 
        'frutas y verduras': 4, 'congelados': 5, 
        'bebidas': 6, 'galletitas y snacks': 7, 'conservas': 8
    }
    # Buscar el texto, pasarlo a minúsculas, y reemplazarlo por su ID
    df['id_categoria'] = df['id_categoria'].astype(str).str.strip().str.lower().map(cat_map)
    return df

def transform_ventas(df):
    # Eliminar filas donde el 'id_venta' esté duplicado, quedándonos con la primera aparición
    cantidad_original = len(df)
    df = df.drop_duplicates(subset=['id_venta'])
    cantidad_nueva = len(df)
    
    if cantidad_original != cantidad_nueva:
        print(f"🧹 Se eliminaron {cantidad_original - cantidad_nueva} ventas duplicadas del CSV.")
        
    return df


if __name__ == "__main__":
    
    load_table("categorias.csv", "categorias", {
        "id_categoría": "id_categoria", "id_categoria": "id_categoria",
        "categoría": "categoria", "categoria": "categoria",
        "descripción": "descripcion", "descripcion": "descripcion"
    })

    load_table("metodos_pago.csv", "metodos_pago", {
        "id_método": "id_metodo", "id_metodo": "id_metodo",
        "método": "metodo", "metodo": "metodo",
        "descripción": "descripcion", "descripcion": "descripcion"
    })

    load_table("clientes.csv", "clientes", {
        "id_cliente": "id_cliente", "nombre": "nombre",
        "apellido": "apellido", "email": "email",
        "fecha_registro": "fecha_registro", "fecha_resgistro": "fecha_registro", 
        "región": "region", "region": "region"
    }, date_columns=["fecha_registro"])

    load_table("productos.csv", "productos", {
        "id_producto": "id_producto", "nombre_producto": "nombre_producto",
        "categoría": "id_categoria", "categoria": "id_categoria",
        "precio_unitario": "precio_unitario", "stock": "stock"
    }, custom_transform=transform_productos)

    load_table("ventas.csv", "ventas", {
        "id_venta": "id_venta", "fecha": "fecha",
        "id_cliente": "id_cliente", "id_producto": "id_producto",
        "cantidad": "cantidad", "método_pago": "id_metodo",
        "metodo_pago": "id_metodo", "estado": "estado"
    }, date_columns=["fecha"], custom_transform=transform_ventas)

    print("🎉 ¡Proceso ETL completado!")