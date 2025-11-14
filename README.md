# 📊 Dashboard de Análisis Logístico con ETL

Proyecto completo de análisis de datos de Supply Chain que demuestra el ciclo completo de un proceso ETL: desde la extracción de datos hasta insights accionables con visualizaciones profesionales.

---

## 🎯 Descripción

Sistema de análisis de datos logísticos que procesa información de múltiples aspectos de la cadena de suministro: productos, ventas, inventario, logística, proveedores y producción. Incluye pipeline ETL automatizado, base de datos relacional y análisis exploratorio con visualizaciones profesionales.

---

## 🔥 Hallazgo Clave del Proyecto

### El Problema
OTIF (On-Time In-Full) crítico del **2%** - Solo 2 de cada 100 entregas eran completas y a tiempo.

### El Análisis
Mediante **análisis de causa raíz con Python**, identifiqué:

✅ **Stock solo cubría 21.7% de la demanda** → Problema de forecasting/inventario  
✅ **20 productos específicos** causaban 80% del problema (Análisis de Pareto)  
✅ **Categoría Skincare** en situación crítica (8% de cobertura)  
✅ **Lead times NO correlacionaban** → Descartado como causa  

### El Valor
- 📊 Plan estructurado: 2% → 95% OTIF en 90 días
- 💰 Inversión focalizada en 20 SKUs críticos (no dispersa)
- 🎯 Decisiones basadas en datos, no intuición
- ⏱️ Análisis completado en 48 horas

**Técnicas:** ETL, Análisis de Pareto, Matriz de Priorización, Correlaciones, Dashboard Interactivo

---

## ✨ Características Principales

- ✅ **Pipeline ETL Automatizado**: CSV → Python → MySQL
- ✅ **Base de Datos Normalizada**: 5 tablas con integridad referencial
- ✅ **Análisis de Causa Raíz**: Identificación del problema real
- ✅ **Dashboard Interactivo**: Plotly Dash con filtros dinámicos
- ✅ **KPIs de Supply Chain**: OTIF, On-Time, In-Full, cobertura de stock
- ✅ **Visualizaciones Profesionales**: 12+ gráficos accionables

---

## 🛠️ Tecnologías

- **Python 3.13:** Pandas, NumPy, Matplotlib, Seaborn, Plotly
- **MySQL 8.0:** Base de datos relacional
- **Plotly Dash:** Dashboard web interactivo
- **Jupyter Notebook:** Análisis documentado
- **Git/GitHub:** Control de versiones

---

## 📁 Estructura del Proyecto
```
proyecto-01-dashboard-logistico/
├── data/
│   ├── raw/              # Datos originales
│   └── processed/        # Datos limpios
├── notebooks/            # Jupyter con análisis completo
├── src/                  # Scripts Python
│   ├── create_database.py
│   ├── etl_pipeline.py
│   └── dashboard_app.py
├── outputs/              # Reportes y visualizaciones
├── README.md
└── requirements.txt
```

---

## 🚀 Instalación
```bash
# 1. Clonar repositorio
git clone https://github.com/GonzaloUlloaCL/analisis-datos-python-portafolio.git
cd proyecto-01-dashboard-logistico

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env con credenciales MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=supply_chain_db

# 5. Ejecutar pipeline
cd src
python create_database.py
python etl_pipeline.py

# 6. Ver dashboard
python dashboard_app.py
# Abrir: http://localhost:8050
```

---

## 📊 Resultados del Análisis

### KPIs Identificados
- **OTIF:** 2.0% (crítico)
- **On-Time:** 61.0% (aceptable)
- **In-Full:** 2.0% (crítico)
- **Cobertura de Stock:** 21.7%

### Causa Raíz
Inventario insuficiente - política de compras inadecuada o error en forecasting.

### Productos Críticos
20 SKUs identificados con Análisis de Pareto (80/20).

---

## 🔮 Mejoras Futuras

- [ ] Modelo predictivo de demanda (Machine Learning)
- [ ] Conexión con APIs de ERP
- [ ] Bot de Telegram para alertas
- [ ] Deploy en cloud (AWS, Heroku)
- [ ] Optimización de project management con programación lineal

---

## 📊 Ver Análisis Completo

[![Open in nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/GonzaloUlloaCL/analisis-datos-python-portafolio/blob/main/proyecto-01-dashboard-logistico/notebooks/analisis_supply_chain.ipynb)

---

## 👤 Autor

**Gonzalo Ulloa González**  
Ingeniero Industrial | Analista de Datos

📧 gonzalo.ulloa@usach.cl
💼 [LinkedIn](https://www.linkedin.com/in/gonzalo-ulloa-g/)  
🐙 [GitHub](https://github.com/GonzaloUlloaCL)

---

## 📄 Licencia

Portafolio profesional - Código disponible para fines educativos
---

## 🙏 Agradecimientos

Dataset: [Supply Chain Analysis - Kaggle](https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis)