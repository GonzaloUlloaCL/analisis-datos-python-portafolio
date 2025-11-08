import pymysql
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión MySQL
config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

print("=" * 60)
print("     INICIANDO ETL PIPELINE")
print("=" * 60)

# ========================================
# PASO 1: EXTRACCIÓN (Extract)
# ========================================
print("\n PASO 1: EXTRAYENDO DATOS DEL CSV...")

# Leer CSV desde data/raw/
data_path = os.path.join('..', 'data', 'raw', 'supply_chain_data.csv')
df = pd.read_csv(data_path)

print(f"✅ Datos extraídos: {df.shape[0]} registros, {df.shape[1]} columnas")

# ========================================
# PASO 2: TRANSFORMACIÓN (Transform)
# ========================================
print("\n PASO 2: TRANSFORMANDO DATOS...")

# 2.1 - Limpiar nombres de columnas (quitar espacios)
df.columns = df.columns.str.strip()

# 2.2 - Crear dataframes separados por tabla
products_df = df[['Product type', 'SKU', 'Price', 'Availability', 'Stock levels']].copy()
products_df.columns = ['product_type', 'sku', 'price', 'availability', 'stock_levels']

# Eliminar duplicados por SKU
products_df = products_df.drop_duplicates(subset=['sku'])

# 2.3 - Tabla de proveedores (Suppliers)
suppliers_df = df[['Supplier name', 'Location', 'Lead time']].copy()
suppliers_df.columns = ['supplier_name', 'location', 'lead_time']
suppliers_df = suppliers_df.drop_duplicates(subset=['supplier_name'])

# 2.4 - Tabla de ventas (Sales)
sales_df = df[['SKU', 'Number of products sold', 'Revenue generated', 'Customer demographics']].copy()
sales_df.columns = ['sku', 'products_sold', 'revenue_generated', 'customer_demographics']

# 2.5 - Tabla de logística (Logistics)
logistics_df = df[['SKU', 'Shipping times', 'Shipping carriers', 'Shipping costs', 
                    'Transportation modes', 'Routes', 'Costs']].copy()
logistics_df.columns = ['sku', 'shipping_times', 'shipping_carrier', 'shipping_costs',
                        'transportation_mode', 'route', 'total_costs']

# 2.6 - Tabla de producción (Production)
production_df = df[['SKU', 'Production volumes', 'Manufacturing lead time', 
                     'Manufacturing costs', 'Inspection results', 'Defect rates']].copy()
production_df.columns = ['sku', 'production_volumes', 'manufacturing_lead_time',
                         'manufacturing_costs', 'inspection_results', 'defect_rates']

print(f"✅ Datos transformados:")
print(f"   - Productos: {len(products_df)} registros únicos")
print(f"   - Proveedores: {len(suppliers_df)} registros únicos")
print(f"   - Ventas: {len(sales_df)} registros")
print(f"   - Logística: {len(logistics_df)} registros")
print(f"   - Producción: {len(production_df)} registros")

# ========================================
# PASO 3: CARGA (Load)
# ========================================
print("\n PASO 3: CARGANDO DATOS A MYSQL...")

try:
    # Conectar a MySQL
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    
    # 3.1 - Cargar productos (primero porque otras tablas tienen FK)
    print("\n   Cargando productos...")
    for _, row in products_df.iterrows():
        cursor.execute("""
            INSERT INTO products (product_type, sku, price, availability, stock_levels)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            price = VALUES(price),
            availability = VALUES(availability),
            stock_levels = VALUES(stock_levels)
        """, tuple(row))
    print(f"   ✅ {len(products_df)} productos cargados")
    
    # 3.2 - Cargar proveedores
    print("\n   Cargando proveedores...")
    for _, row in suppliers_df.iterrows():
        cursor.execute("""
            INSERT INTO suppliers (supplier_name, location, lead_time)
            VALUES (%s, %s, %s)
        """, tuple(row))
    print(f"   ✅ {len(suppliers_df)} proveedores cargados")
    
    # 3.3 - Cargar ventas
    print("\n   Cargando ventas...")
    for _, row in sales_df.iterrows():
        cursor.execute("""
            INSERT INTO sales (sku, products_sold, revenue_generated, customer_demographics)
            VALUES (%s, %s, %s, %s)
        """, tuple(row))
    print(f"   ✅ {len(sales_df)} registros de ventas cargados")
    
    # 3.4 - Cargar logística
    print("\n   Cargando logística...")
    for _, row in logistics_df.iterrows():
        cursor.execute("""
            INSERT INTO logistics (sku, shipping_times, shipping_carrier, shipping_costs,
                                 transportation_mode, route, total_costs)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
    print(f"   ✅ {len(logistics_df)} registros de logística cargados")
    
    # 3.5 - Cargar producción
    print("\n   Cargando producción...")
    for _, row in production_df.iterrows():
        cursor.execute("""
            INSERT INTO production (sku, production_volumes, manufacturing_lead_time,
                                  manufacturing_costs, inspection_results, defect_rates)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(row))
    print(f"   ✅ {len(production_df)} registros de producción cargados")
    
    # Commit de todas las transacciones
    connection.commit()
    
    print("\n" + "=" * 60)
    print(" ETL PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    
    # Verificar datos cargados
    cursor.execute("SELECT COUNT(*) FROM products")
    print(f"\n📊 Resumen final:")
    print(f"   Productos en BD: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    print(f"   Proveedores en BD: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM sales")
    print(f"   Ventas en BD: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM logistics")
    print(f"   Logística en BD: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM production")
    print(f"   Producción en BD: {cursor.fetchone()[0]}")
    
except Exception as e:
    print(f"\n❌ Error durante el ETL: {e}")
    connection.rollback()
    
finally:
    cursor.close()
    connection.close()
    print("\n🔒 Conexión cerrada")