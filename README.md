# 📊 Dashboard de Análisis Logístico con ETL

Proyecto completo de análisis de datos de Supply Chain que demuestra el ciclo completo de un proceso ETL: desde la extracción de datos hasta insights accionables con visualizaciones profesionales.

---

## 🎯 Descripción

Sistema de análisis de datos logísticos que procesa información de múltiples aspectos de la cadena de suministro: productos, ventas, inventario, logística, proveedores y producción. Incluye pipeline ETL automatizado, base de datos relacional y análisis exploratorio con visualizaciones impactantes.

**Dataset:** Supply Chain Data (100 registros) con 24 variables operacionales

---

## ✨ Características Principales

- ✅ **Pipeline ETL Automatizado**: Extracción desde CSV, transformación con Pandas, carga a MySQL
- ✅ **Base de Datos Normalizada**: 5 tablas relacionales con integridad referencial
- ✅ **Análisis Exploratorio Completo**: Jupyter Notebook con 15+ visualizaciones
- ✅ **KPIs de Supply Chain**: Revenue, eficiencia logística, calidad, inventario
- ✅ **Insights Accionables**: Recomendaciones basadas en datos
- ✅ **Exportación de Reportes**: CSV con análisis por categoría y alertas

---

## 🛠️ Tecnologías

**Lenguajes y Herramientas:**
- Python 3.13
- MySQL 8.0
- Jupyter Notebook

**Librerías Python:**
- `pandas` & `numpy` - Manipulación y análisis de datos
- `matplotlib` & `seaborn` - Visualizaciones
- `pymysql` & `sqlalchemy` - Conexión a bases de datos
- `python-dotenv` - Gestión de variables de entorno

---

## 📁 Estructura del Proyecto
```
proyecto-01-dashboard-logistico/
│
├── data/
│   ├── raw/                    # Datos originales (CSV)
│   └── processed/              # Datos procesados
│
├── notebooks/
│   └── analisis_supply_chain.ipynb  # Análisis completo con visualizaciones
│
├── src/
│   ├── explore_data.py         # Exploración inicial del dataset
│   ├── create_database.py      # Creación de estructura de BD
│   └── etl_pipeline.py         # Pipeline ETL completo
│
├── outputs/
│   ├── top_productos.csv       # Top 20 productos por revenue
│   ├── resumen_categorias.csv  # Análisis por categoría
│   └── productos_alerta.csv    # Productos que requieren atención
│
├── sql/                        # Scripts SQL (generados dinámicamente)
├── README.md
├── requirements.txt
└── .env                        # Configuración de BD (no incluido en repo)
```

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/GonzaloUlloaCL/analisis-datos-python-portafolio.git
cd analisis-datos-python-portafolio/proyecto-01-dashboard-logistico
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Crear archivo `.env` con:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=supply_chain_db
```

### 5. Ejecutar el proyecto
```bash
# Crear base de datos
cd src
python create_database.py

# Ejecutar ETL
python etl_pipeline.py

# Analizar en Jupyter
cd ../notebooks
jupyter notebook
```

---

## 📊 KPIs Analizados

### Financieros
- Revenue total y por categoría
- Márgenes operativos
- Costos logísticos y de manufactura

### Operacionales
- Rotación de inventario
- Tiempo promedio de entrega
- Tasa de cumplimiento de órdenes
- Niveles de stock

### Calidad
- Tasa de defectos por producto y categoría
- Resultados de inspecciones
- Correlación defectos vs costos

### Logística
- Eficiencia por carrier (costo/día)
- Análisis por modo de transporte
- Optimización de rutas

---

## 📈 Visualizaciones Incluidas

1. **Matriz de Correlación** - Relaciones entre variables clave
2. **Revenue por Categoría** - Barras + Pie Chart
3. **Top Productos** - Análisis de mejores performers
4. **Eficiencia Logística** - Costo vs Tiempo por carrier
5. **Análisis de Calidad** - Distribución y tendencias de defectos
6. **Dashboard Ejecutivo** - Vista consolidada de KPIs

---

## 💡 Insights Principales

- Identificación de categoría líder en revenue
- Detección de productos con alto stock/bajas ventas
- Análisis de eficiencia por carrier
- Productos con alta tasa de defectos (alertas)
- Oportunidades de optimización de costos

---

## 📝 Próximas Mejoras

- [ ] Agregar predicciones con Machine Learning
- [ ] Dashboard interactivo con Plotly/Dash
- [ ] Automatización de reportes periódicos
- [ ] Integración con APIs de proveedores
- [ ] Análisis de series temporales

---

## 👤 Autor

**Gonzalo Ulloa González**

Ingeniero Industrial especializado en Supply Chain y Análisis de Datos

📧 gonzalo.ulloa@usach.cl  
💼 [LinkedIn](https://www.linkedin.com/in/gonzalo-ulloa-g/)  
🐙 [GitHub](https://github.com/GonzaloUlloaCL)

---

## 📄 Licencia

Este proyecto es parte de un portafolio profesional y está disponible para fines educativos.

---

## 🙏 Agradecimientos

Dataset: [Supply Chain Analysis - Kaggle](https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis)
