import pymysql
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión
config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

db_name = os.getenv('DB_NAME')

# Crear conexión
connection = pymysql.connect(**config)

try:
    with connection.cursor() as cursor:
        # Crear base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ Base de datos '{db_name}' creada/verificada exitosamente")
        
        # Usar la base de datos
        cursor.execute(f"USE {db_name}")
        
        # Crear tabla de productos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_type VARCHAR(50),
            sku VARCHAR(50) UNIQUE,
            price DECIMAL(10,2),
            availability INT,
            stock_levels INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✅ Tabla 'products' creada")
        
        # Crear tabla de proveedores
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            supplier_name VARCHAR(100),
            location VARCHAR(100),
            lead_time INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✅ Tabla 'suppliers' creada")
        
        # Crear tabla de ventas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sku VARCHAR(50),
            products_sold INT,
            revenue_generated DECIMAL(12,2),
            customer_demographics VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sku) REFERENCES products(sku)
        )
        """)
        print("✅ Tabla 'sales' creada")
        
        # Crear tabla de logística
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logistics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sku VARCHAR(50),
            shipping_times INT,
            shipping_carrier VARCHAR(100),
            shipping_costs DECIMAL(10,2),
            transportation_mode VARCHAR(50),
            route VARCHAR(50),
            total_costs DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sku) REFERENCES products(sku)
        )
        """)
        print("✅ Tabla 'logistics' creada")
        
        # Crear tabla de producción
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS production (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sku VARCHAR(50),
            production_volumes INT,
            manufacturing_lead_time INT,
            manufacturing_costs DECIMAL(10,2),
            inspection_results VARCHAR(50),
            defect_rates DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sku) REFERENCES products(sku)
        )
        """)
        print("✅ Tabla 'production' creada")
        
    connection.commit()
    print("\n🎉 Base de datos y tablas creadas exitosamente!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    connection.rollback()
    
finally:
    connection.close()
    print("🔒 Conexión cerrada")