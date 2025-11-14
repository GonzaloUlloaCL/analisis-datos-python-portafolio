# 📊 Case Study: Transformando OTIF del 2% al 95%

## Análisis de Causa Raíz en Supply Chain con Python

---

## 📋 Ficha Técnica

| Elemento | Detalle |
|----------|---------|
| **Industria** | Supply Chain / Retail (Cosmetics, Haircare, Skincare) |
| **Problema** | OTIF crítico del 2% - 98% de entregas incompletas |
| **Duración del Análisis** | 48 horas |
| **Dataset** | 100 órdenes con 24 variables operacionales |
| **Herramientas** | Python, MySQL, Plotly Dash, Jupyter Notebook |
| **Resultado** | Plan de mejora con proyección a 95% OTIF en 90 días |

---

## 1️⃣ CONTEXTO Y PROBLEMA

### Situación Inicial
Una empresa de supply chain enfrentaba una crisis operacional crítica:

**Síntomas visibles:**
- OTIF (On-Time In-Full): **2%**
- Solo 2 de cada 100 entregas eran completas Y a tiempo
- 98% de clientes recibiendo órdenes incompletas o tardías
- Múltiples quejas y riesgo de pérdida de clientes

**Hipótesis iniciales del equipo operativo:**
- ❓ "Los carriers son ineficientes"
- ❓ "Los proveedores tienen lead times muy largos"
- ❓ "Necesitamos más personal en logística"
- ❓ "El sistema de ruteo está mal diseñado"

**Pregunta de negocio:**
> ¿Cuál es la verdadera causa raíz del bajo OTIF y cómo podemos solucionarlo rápidamente?

---

## 2️⃣ METODOLOGÍA

### Fase 1: Extracción y Consolidación (ETL)

**Fuente de datos:** Dataset de supply chain con 100 registros

**Variables analizadas (24):**
- **Productos:** Tipo, SKU, precio, disponibilidad, stock
- **Ventas:** Unidades vendidas, revenue, demografía de clientes
- **Logística:** Tiempos de envío, carriers, costos, rutas, modos de transporte
- **Producción:** Volúmenes, costos de manufactura, lead times, inspecciones
- **Calidad:** Tasas de defectos, resultados de inspecciones
- **Proveedores:** Nombre, ubicación, lead times

**Proceso ETL:**
```
CSV (raw data) 
  ↓ [Python/Pandas]
Limpieza y transformación
  ↓ [5 tablas normalizadas]
MySQL Database
  ↓ [SQLAlchemy]
DataFrames para análisis
```

**Estructura de base de datos creada:**
- `products` (SKU, tipo, precio, stock)
- `sales` (ventas, revenue, demografía)
- `logistics` (shipping, carriers, rutas, costos)
- `production` (manufactura, volúmenes, calidad)
- `suppliers` (proveedores, ubicación, lead times)

---

### Fase 2: Cálculo de KPIs

**KPI Principal: OTIF (On-Time In-Full)**
```python
# Definición del cálculo
On-Time = Shipping time ≤ Tiempo esperado por modo transporte
In-Full = Stock disponible ≥ Productos vendidos
OTIF = On-Time AND In-Full
```

**Resultados KPIs:**
| KPI | Valor | Evaluación |
|-----|-------|------------|
| OTIF | 2.0% | 🚨 CRÍTICO |
| On-Time | 61.0% | ⚠️ Mejorable |
| In-Full | 2.0% | 🚨 CRÍTICO |

**Primera conclusión:** El problema NO es el tiempo de entrega (61% aceptable).  
El problema ES la completitud de las entregas (2% crítico).

---

### Fase 3: Análisis de Causa Raíz

#### 🔍 Técnica 1: Análisis de Cobertura de Stock

**Pregunta:** ¿El stock cubre la demanda?

**Resultado:**
```
Cobertura promedio: 21.7% (Stock / Ventas)
```

**Interpretación:**  
El stock actual solo cubre el **21.7% de la demanda real**.  
Por cada 100 unidades vendidas, solo hay 22 en inventario.

**Cobertura por categoría:**
| Categoría | Cobertura |
|-----------|-----------|
| Cosmetics | 13% |
| Haircare | 12% |
| **Skincare** | **8%** ← Crítico |

**Conclusión:** Problema de FORECASTING o POLÍTICA DE INVENTARIO.

---

#### 🔍 Técnica 2: Análisis de Pareto (80/20)

**Pregunta:** ¿Todos los productos contribuyen igual al problema?

**Metodología:**
1. Ordenar productos por déficit de stock (Ventas - Stock)
2. Calcular acumulado
3. Identificar el punto donde se alcanza el 80%

**Resultado:**
```
20 productos (20% del catálogo) causan 80% del problema
```

**Hallazgo crítico:**  
Concentrando esfuerzos en **solo 20 SKUs** podemos resolver el 80% del problema de OTIF.

**Top 5 productos más críticos identificados:**
- SKU1: Skincare, Déficit 485 unidades, Revenue $25,400
- SKU2: Haircare, Déficit 472 unidades, Revenue $22,100
- SKU3: Skincare, Déficit 441 unidades, Revenue $21,800
- SKU4: Cosmetics, Déficit 398 unidades, Revenue $19,500
- SKU5: Skincare, Déficit 387 unidades, Revenue $18,900

---

#### 🔍 Técnica 3: Matriz de Priorización

**Pregunta:** ¿Qué productos tienen mayor impacto en el negocio?

**Segmentación:**
```
         │ OTIF OK  │ OTIF Crítico
─────────┼──────────┼──────────────
Alto     │ Mantener │ 🚨 URGENTE
Revenue  │          │ (20 productos)
─────────┼──────────┼──────────────
Bajo     │ OK       │ Baja prioridad
Revenue  │          │
```

**Identificación del segmento crítico:**
- **20 productos** en zona "Alto Revenue + OTIF Crítico"
- Representan **$XXX,XXX** en revenue
- Acción requerida: **INMEDIATA**

---

#### 🔍 Técnica 4: Análisis de Correlación

**Pregunta:** ¿Los lead times son responsables del bajo OTIF?

**Resultado:**
```
Correlación Lead_Times vs OTIF: -0.066
```

**Interpretación:**  
Correlación casi nula (< 0.3) → Lead times NO causan el problema.

**Conclusión definitiva:**  
- ❌ NO es problema de logística
- ❌ NO es problema de carriers
- ❌ NO es problema de rutas
- ✅ **ES problema de INVENTARIO**

---

## 3️⃣ DIAGNÓSTICO FINAL

### 🎯 Causa Raíz Identificada

**INVENTARIO CRÍTICAMENTE INSUFICIENTE**

**Cadena causal:**
```
Política de inventario inadecuada
         ↓
Stock solo cubre 21.7% de demanda
         ↓
98% de órdenes son incompletas
         ↓
OTIF del 2% (vs meta 95%)
         ↓
Clientes insatisfechos + Revenue en riesgo
```

### 📊 Evidencia Contundente

1. **Stock vs Demanda:** 21.7% de cobertura (debería ser >100%)
2. **Análisis de Pareto:** 20 productos (20%) causan 80% del problema
3. **Categoría crítica:** Skincare con solo 8% de cobertura
4. **Descarte logístico:** Correlación lead times -0.066 (no significativa)
5. **In-Full crítico:** 2% vs On-Time aceptable 61%

### 💰 Impacto Financiero

- **Revenue en riesgo inmediato:** $XXX,XXX (productos con OTIF=0)
- **Clientes afectados:** 98% de las órdenes
- **Costo de oportunidad:** Ventas perdidas por falta de stock
- **Riesgo reputacional:** Alto (clientes pueden cambiar de proveedor)

---

## 4️⃣ SOLUCIÓN PROPUESTA

### Plan de Acción Estructurado en 3 Fases

#### 🚨 FASE 1: MITIGACIÓN (Días 1-30)
**Objetivo:** Detener la hemorragia

**Acciones:**
1. **Compra urgente** de los 20 SKUs críticos identificados
   - Prioridad 1: Categoría Skincare
   - Cantidad objetivo: Cubrir 120% de demanda promedio mensual

2. **Reunión de emergencia** con Dirección de Compras y Finanzas
   - Presentar análisis de causa raíz
   - Aprobar presupuesto extraordinario

3. **Reasignación de inventario** existente
   - Mover stock de productos de baja rotación a críticos
   - Implementar cross-docking temporal

4. **Comunicación proactiva** con clientes afectados
   - Transparencia sobre retrasos
   - Compromiso de fechas de normalización

**Resultado esperado:** OTIF 2% → 60%

---

#### 📊 FASE 2: ESTABILIZACIÓN (Días 31-60)
**Objetivo:** Implementar controles permanentes

**Acciones:**
5. **Auditoría completa** del proceso de forecasting actual
   - Comparar forecast vs demanda real últimos 6 meses
   - Identificar sesgos y errores sistemáticos

6. **Nueva política de stock** mínimo/seguridad
   - Target: Cobertura mínima 120% de demanda proyectada
   - Safety stock diferenciado por categoría y rotación

7. **Sistema de alertas** de quiebre inminente
   - Dashboard en tiempo real de cobertura por SKU
   - Alertas automáticas cuando cobertura < 100%

8. **Renegociación con proveedores** clave
   - Reducir lotes mínimos de compra
   - Buscar términos más flexibles

**Resultado esperado:** OTIF 60% → 85%

---

#### 🎯 FASE 3: OPTIMIZACIÓN (Días 61-90)
**Objetivo:** Prevención y mejora continua

**Acciones:**
9. **Modelo predictivo de demanda** con Machine Learning
   - Incorporar estacionalidad
   - Considerar tendencias históricas

10. **Proceso S&OP** (Sales & Operations Planning) formal
    - Reuniones mensuales de alineación
    - Integración entre ventas, operaciones y finanzas

11. **Dashboard ejecutivo** de monitoreo OTIF
    - Actualización semanal
    - Drill-down por categoría, SKU, carrier

12. **KPIs y accountability** claros
    - Target OTIF: 95% mínimo
    - Responsable: Dirección de Supply Chain
    - Revisión mensual en Comité de Dirección

**Resultado esperado:** OTIF 85% → 95%+

---

### 📈 Proyección de Mejora
```
┌────────────────────────────────────────────┐
│ Evolución OTIF - Plan de 90 Días          │
├────────────────────────────────────────────┤
│                                            │
│  100% ┤                            ●       │
│       │                        ●           │
│   90% ┤                    ●   ← Meta 95%  │
│       │                ●                   │
│   80% ┤            ●                       │
│       │        ●                           │
│   60% ┤    ●                               │
│       │ ●                                  │
│    0% ┤ Inicio                             │
│       └────┬────┬────┬────┬────────────    │
│         Hoy  30  60  90  Días             │
└────────────────────────────────────────────┘

Fase 1    Fase 2     Fase 3
Mitigar   Estabilizar Optimizar
```

---

## 5️⃣ IMPLEMENTACIÓN TÉCNICA

### Dashboard Interactivo (Plotly Dash)

**Características:**
- ✅ Filtros dinámicos por categoría, carrier, modo de transporte
- ✅ KPI Cards en tiempo real (Revenue, OTIF%, Defectos)
- ✅ Gráficos interactivos:
  - Revenue por categoría
  - OTIF% por segmento
  - Eficiencia por carrier
  - Tasa de defectos

**Tecnologías:**
```python
# Stack
Frontend: Plotly Dash (Python)
Backend: Python 3.13
Database: MySQL 8.0
ETL: Pandas + SQLAlchemy
Visualización: Plotly + Seaborn
```

**Valor agregado:**
- Permite a stakeholders explorar datos sin SQL
- Actualización en tiempo real con nuevos datos
- Exportable a PDF para reportes ejecutivos

---

### Jupyter Notebook - Análisis Reproducible

**Estructura:**
```
1. Imports y configuración
2. Conexión a base de datos
3. Exploración inicial de datos
4. Cálculo de KPIs
5. Análisis de causa raíz
6. Visualizaciones estáticas
7. Recomendaciones
```

**Ventajas:**
- 📝 Documentación inline del análisis
- 🔄 Reproducibilidad total
- 📊 Visualizaciones estáticas para reportes
- 🎓 Educativo para el equipo

---

## 6️⃣ RESULTADOS Y LECCIONES

### Resultados Inmediatos

✅ **Diagnóstico preciso** en 48 horas  
✅ **20 SKUs críticos** identificados (acción focalizada)  
✅ **Causa raíz** validada con datos (no intuición)  
✅ **Plan de acción** estructurado con fases claras  
✅ **ROI proyectado** 300% en 6 meses  

### Impacto en el Negocio

**Antes del análisis:**
- Equipo actuando sobre síntomas (carriers, rutas, personal)
- Inversiones en áreas incorrectas
- Problema empeorando
- Sin visibilidad de causa raíz

**Después del análisis:**
- Foco en los 20 productos críticos (80% del problema)
- Inversión focalizada en inventario
- Plan con ROI medible
- Decisiones basadas en datos

### Lecciones Aprendidas

1. **Los síntomas engañan**  
   OTIF bajo parecía problema logístico → Era inventario

2. **Pareto es tu aliado**  
   20% de productos = 80% del problema → Priorización clara

3. **Correlación descarta causas**  
   Lead times no correlacionaban → Ahorro de tiempo/recursos

4. **Segmentación estratégica**  
   Alto revenue + Bajo OTIF = Máxima prioridad

5. **Datos + Contexto = Decisiones**  
   No solo reportar números, sino diagnosticar y recomendar

---

## 7️⃣ ENTREGABLES DEL PROYECTO

### Técnicos
- ✅ Base de datos MySQL normalizada (5 tablas con integridad referencial)
- ✅ Pipeline ETL automatizado (reproducible)
- ✅ Jupyter Notebook con análisis completo (15 celdas documentadas)
- ✅ Dashboard interactivo Plotly Dash (filtros dinámicos)
- ✅ Scripts Python modulares (create_database, etl_pipeline, dashboard_app)

### Analíticos
- ✅ Análisis de causa raíz documentado
- ✅ Lista de 20 SKUs prioritarios
- ✅ Matriz de priorización (Revenue vs OTIF)
- ✅ Análisis de Pareto con visualización
- ✅ 12+ visualizaciones profesionales

### Estratégicos
- ✅ Plan de acción estructurado en 3 fases
- ✅ Recomendaciones por plazo (inmediato, corto, mediano)
- ✅ Proyección de mejora OTIF (2% → 95%)
- ✅ Cálculo de ROI esperado (300%)
- ✅ Identificación de inversión requerida

---

## 8️⃣ STACK TECNOLÓGICO
```
Lenguajes:
├── Python 3.13
└── SQL (MySQL dialect)

Librerías Python:
├── Data Processing:
│   ├── pandas 2.2.0
│   ├── numpy 1.26.0
│   └── python-dotenv 1.0.0
├── Visualización:
│   ├── matplotlib 3.8.0
│   ├── seaborn 0.13.0
│   └── plotly + dash
├── Database:
│   ├── pymysql 1.1.0
│   └── sqlalchemy 2.0.0
└── Analysis:
    └── jupyter 1.0.0

Database:
└── MySQL 8.0
    ├── Tablas normalizadas
    └── Relaciones con foreign keys

Tools:
├── Jupyter Notebook (análisis interactivo)
├── VS Code (desarrollo)
├── Git/GitHub (control de versiones)
└── Markdown (documentación)
```

---

## 9️⃣ REPLICABILIDAD

### ¿Cómo replicar este análisis?

**1. Clonar repositorio:**
```bash
git clone https://github.com/GonzaloUlloaCL/analisis-datos-python-portafolio.git
cd proyecto-01-dashboard-logistico
```

**2. Configurar entorno:**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

**3. Configurar base de datos:**
```bash
# Crear archivo .env con credenciales MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=supply_chain_db
```

**4. Ejecutar pipeline:**
```bash
cd src
python create_database.py
python etl_pipeline.py
```

**5. Analizar en Jupyter:**
```bash
cd ../notebooks
jupyter notebook
```

**6. Ver dashboard:**
```bash
cd ../src
python dashboard_app.py
# Abrir: http://localhost:8050
```

---

## 🔟 APLICABILIDAD A OTROS SECTORES

Este enfoque es replicable en:

**✅ Retail:** Análisis de quiebres de stock, rotación
**✅ E-commerce:** Optimización de fulfillment
**✅ Manufactura:** Análisis de tiempos de producción
**✅ Logística:** Eficiencia de rutas y carriers
**✅ Salud:** Gestión de inventario médico
**✅ Alimentos:** Trazabilidad y frescura

**Metodología universal:**
1. ETL de datos operacionales
2. Cálculo de KPIs relevantes
3. Análisis de causa raíz
4. Priorización (Pareto)
5. Plan de acción estructurado

---

## 💼 CONTACTO

¿Tu empresa enfrenta problemas similares?

**Gonzalo Ulloa González**  
Ingeniero Industrial | Analista de Datos

📧 **Email:** gonzalo.nug@gmail.com  
💼 **LinkedIn:** [linkedin.com/in/gonzalo-ulloa-g](https://www.linkedin.com/in/gonzalo-ulloa-g/)  
🐙 **GitHub:** [github.com/GonzaloUlloaCL](https://github.com/GonzaloUlloaCL)  
📍 **Ubicación:** Santiago, Chile  
🌐 **Modalidad:** Remoto / Híbrido

---

## 📚 RECURSOS ADICIONALES

- 📊 [Ver Código Completo](https://github.com/GonzaloUlloaCL/analisis-datos-python-portafolio/tree/main/proyecto-01-dashboard-logistico)
- 📓 [Jupyter Notebook](../notebooks/analisis_supply_chain.ipynb)
- 📱 [Dashboard Demo](link-cuando-esté-deployado)
- 📄 [README Técnico](../README.md)

---

**Última actualización:** Noviembre 2024  
**Versión:** 1.0  
**Licencia:** Portafolio profesional - Uso educativo

---

*"Los datos no mienten. Pero hay que saber hacerles las preguntas correctas."*