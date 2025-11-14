import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pymysql
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv(os.path.join('..', '.env'))

# Conectar a MySQL
config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

print("📊 Cargando datos desde MySQL...")
connection = pymysql.connect(**config)

# Cargar datos
products_df = pd.read_sql("SELECT * FROM products", connection)
sales_df = pd.read_sql("SELECT * FROM sales", connection)
logistics_df = pd.read_sql("SELECT * FROM logistics", connection)
production_df = pd.read_sql("SELECT * FROM production", connection)

connection.close()

# Consolidar datos
products_clean = products_df.drop(columns=['id', 'created_at'])
logistics_clean = logistics_df.drop(columns=['id', 'created_at'])
production_clean = production_df.drop(columns=['id', 'created_at'])
sales_clean = sales_df.drop(columns=['id', 'created_at'])

df = sales_clean.merge(products_clean, on='sku', how='left') \
                .merge(logistics_clean, on='sku', how='left') \
                .merge(production_clean, on='sku', how='left')

# Calcular OTIF (lógica corregida)
expected_time = df.groupby('transportation_mode')['shipping_times'].median()
df['expected_shipping_time'] = df['transportation_mode'].map(expected_time)
df['on_time'] = (df['shipping_times'] <= df['expected_shipping_time']).astype(int)
df['in_full'] = (df['stock_levels'] >= df['products_sold']).astype(int)  # CORREGIDO
df['otif'] = (df['on_time'] & df['in_full']).astype(int)

print(f"✅ Datos cargados: {len(df)} registros")

# Crear aplicación Dash
app = dash.Dash(__name__)

# Colores
colors = {
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'primary': '#3498db',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c'
}

# Layout del dashboard
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    
    # Header
    html.Div([
        html.H1('🚚 Supply Chain Dashboard', 
                style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '10px'}),
        html.H3('Análisis en Tiempo Real con KPI OTIF', 
                style={'textAlign': 'center', 'color': colors['primary'], 'marginBottom': '30px'})
    ]),
    
    # Filtros
    html.Div([
        html.Div([
            html.Label('Categoría de Producto:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': 'Todas', 'value': 'ALL'}] + 
                        [{'label': cat, 'value': cat} for cat in df['product_type'].unique()],
                value='ALL',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),
        
        html.Div([
            html.Label('Carrier:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='carrier-filter',
                options=[{'label': 'Todos', 'value': 'ALL'}] + 
                        [{'label': car, 'value': car} for car in df['shipping_carrier'].unique()],
                value='ALL',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),
        
        html.Div([
            html.Label('Modo de Transporte:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='transport-filter',
                options=[{'label': 'Todos', 'value': 'ALL'}] + 
                        [{'label': mode, 'value': mode} for mode in df['transportation_mode'].unique()],
                value='ALL',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '30px'}),
    
    # KPI Cards
    html.Div(id='kpi-cards', style={'marginBottom': '30px'}),
    
    # Gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='revenue-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            dcc.Graph(id='otif-chart')
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='carrier-efficiency')
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            dcc.Graph(id='defects-chart')
        ], style={'width': '48%', 'display': 'inline-block'})
    ]),
    
    # Footer
    html.Div([
        html.Hr(),
        html.P('© 2025 Gonzalo Ulloa González | Análisis de Supply Chain', 
               style={'textAlign': 'center', 'color': colors['text'], 'marginTop': '30px'})
    ])
])

# Callbacks para interactividad
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('revenue-chart', 'figure'),
     Output('otif-chart', 'figure'),
     Output('carrier-efficiency', 'figure'),
     Output('defects-chart', 'figure')],
    [Input('category-filter', 'value'),
     Input('carrier-filter', 'value'),
     Input('transport-filter', 'value')]
)
def update_dashboard(category, carrier, transport):
    # Filtrar datos
    filtered_df = df.copy()
    
    if category != 'ALL':
        filtered_df = filtered_df[filtered_df['product_type'] == category]
    if carrier != 'ALL':
        filtered_df = filtered_df[filtered_df['shipping_carrier'] == carrier]
    if transport != 'ALL':
        filtered_df = filtered_df[filtered_df['transportation_mode'] == transport]
    
    # Calcular KPIs
    total_revenue = filtered_df['revenue_generated'].sum()
    total_products = filtered_df['products_sold'].sum()
    otif_pct = (filtered_df['otif'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    avg_defects = filtered_df['defect_rates'].mean()
    
    # KPI Cards
    kpi_cards = html.Div([
        html.Div([
            html.H4('💰 Revenue Total'),
            html.H2(f'${total_revenue:,.0f}', style={'color': colors['success']})
        ], style={'width': '23%', 'display': 'inline-block', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'marginRight': '2%', 'textAlign': 'center'}),
        
        html.Div([
            html.H4('📦 Productos Vendidos'),
            html.H2(f'{total_products:,}', style={'color': colors['primary']})
        ], style={'width': '23%', 'display': 'inline-block', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'marginRight': '2%', 'textAlign': 'center'}),
        
        html.Div([
            html.H4('✅ OTIF %'),
            html.H2(f'{otif_pct:.1f}%', style={'color': colors['success'] if otif_pct >= 95 else colors['danger']})
        ], style={'width': '23%', 'display': 'inline-block', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'marginRight': '2%', 'textAlign': 'center'}),
        
        html.Div([
            html.H4('⚠️ Defectos Prom'),
            html.H2(f'{avg_defects:.2f}%', style={'color': colors['warning']})
        ], style={'width': '23%', 'display': 'inline-block', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center'})
    ])
    
    # Gráfico 1: Revenue por categoría
    revenue_by_cat = filtered_df.groupby('product_type')['revenue_generated'].sum().reset_index()
    fig_revenue = px.bar(revenue_by_cat, x='product_type', y='revenue_generated',
                        title='Revenue por Categoría',
                        labels={'product_type': 'Categoría', 'revenue_generated': 'Revenue ($)'},
                        color='revenue_generated',
                        color_continuous_scale='Blues')
    fig_revenue.update_layout(showlegend=False)
    
    # Gráfico 2: OTIF por categoría
    otif_by_cat = filtered_df.groupby('product_type')['otif'].mean().reset_index()
    otif_by_cat['otif'] = otif_by_cat['otif'] * 100
    fig_otif = px.bar(otif_by_cat, x='product_type', y='otif',
                     title='OTIF % por Categoría',
                     labels={'product_type': 'Categoría', 'otif': 'OTIF (%)'},
                     color='otif',
                     color_continuous_scale='Greens')
    fig_otif.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="Meta 95%")
    fig_otif.update_layout(showlegend=False)
    
    # Gráfico 3: Eficiencia por carrier
    carrier_eff = filtered_df.groupby('shipping_carrier')['shipping_costs'].mean().reset_index()
    fig_carrier = px.bar(carrier_eff, x='shipping_carrier', y='shipping_costs',
                        title='Costo Promedio por Carrier',
                        labels={'shipping_carrier': 'Carrier', 'shipping_costs': 'Costo ($)'},
                        color='shipping_costs',
                        color_continuous_scale='Reds')
    fig_carrier.update_layout(showlegend=False)
    
    # Gráfico 4: Defectos
    defects_by_cat = filtered_df.groupby('product_type')['defect_rates'].mean().reset_index()
    fig_defects = px.bar(defects_by_cat, x='product_type', y='defect_rates',
                        title='Tasa de Defectos por Categoría',
                        labels={'product_type': 'Categoría', 'defect_rates': 'Defectos (%)'},
                        color='defect_rates',
                        color_continuous_scale='Oranges')
    fig_defects.update_layout(showlegend=False)
    
    return kpi_cards, fig_revenue, fig_otif, fig_carrier, fig_defects

# Ejecutar app
if __name__ == '__main__':
    print("\n🚀 Iniciando dashboard...")
    print("📱 Abre tu navegador en: http://127.0.0.1:8050")
    app.run(debug=True)