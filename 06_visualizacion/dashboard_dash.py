
"""
Dashboard Empresarial con Dash
Dashboard profesional para análisis de ventas
"""

from dash import Dash, dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================================
# GENERAR DATOS
# ============================================================

def generar_datos():
    np.random.seed(42)
    fechas = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')

    df = pd.DataFrame({
        'fecha': fechas,
        'ventas': np.random.randint(1000, 5000, len(fechas)) + 
                 np.cumsum(np.random.randn(len(fechas)) * 50),
        'categoria': np.random.choice(['Electrónica', 'Ropa', 'Alimentos'], len(fechas)),
        'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], len(fechas))
    })

    return df

df = generar_datos()

# ============================================================
# INICIALIZAR APP
# ============================================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.title = "Dashboard de Ventas"

# ============================================================
# LAYOUT
# ============================================================

# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("📊 Dashboard de Ventas", className="text-white mb-0"))
        ]),
    ]),
    color="primary",
    dark=True,
    className="mb-4"
)

# Controles
controles = dbc.Card([
    dbc.CardBody([
        html.H5("Filtros", className="card-title"),
        html.Hr(),

        # Selector de fecha
        html.Label("Rango de Fechas:"),
        dcc.DatePickerRange(
            id='date-picker',
            start_date=df['fecha'].min(),
            end_date=df['fecha'].max(),
            display_format='DD/MM/YYYY',
            className="mb-3"
        ),

        html.Br(),
        html.Br(),

        # Selector de región
        html.Label("Región:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': 'Todas', 'value': 'ALL'}] +
                   [{'label': r, 'value': r} for r in df['region'].unique()],
            value='ALL',
            className="mb-3"
        ),

        # Selector de categoría
        html.Label("Categoría:"),
        dcc.Dropdown(
            id='categoria-dropdown',
            options=[{'label': 'Todas', 'value': 'ALL'}] +
                   [{'label': c, 'value': c} for c in df['categoria'].unique()],
            value='ALL',
            className="mb-3"
        ),

        html.Hr(),

        # Botón de actualizar
        dbc.Button(
            "🔄 Actualizar Dashboard",
            id='actualizar-btn',
            color="primary",
            className="w-100"
        )
    ])
])

# Métricas (KPIs)
metricas = dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("💰", className="text-center"),
                html.H5("Total Ventas", className="text-center text-muted"),
                html.H3(id="kpi-ventas", className="text-center")
            ])
        ])
    ], width=3),

    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("📈", className="text-center"),
                html.H5("Promedio Diario", className="text-center text-muted"),
                html.H3(id="kpi-promedio", className="text-center")
            ])
        ])
    ], width=3),

    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("📊", className="text-center"),
                html.H5("Mejor Día", className="text-center text-muted"),
                html.H3(id="kpi-mejor", className="text-center")
            ])
        ])
    ], width=3),

    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("🎯", className="text-center"),
                html.H5("Total Días", className="text-center text-muted"),
                html.H3(id="kpi-dias", className="text-center")
            ])
        ])
    ], width=3),
], className="mb-4")

# Gráficos
graficos = dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H5("Evolución de Ventas", className="card-title"),
                dcc.Graph(id='grafico-tiempo')
            ])
        ])
    ], width=8),

    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H5("Distribución por Categoría", className="card-title"),
                dcc.Graph(id='grafico-categoria')
            ])
        ])
    ], width=4),
], className="mb-4")

# Tabla
tabla = dbc.Card([
    dbc.CardBody([
        html.H5("Datos Detallados", className="card-title"),
        html.Div(id='tabla-datos')
    ])
])

# Layout principal
app.layout = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col(controles, width=3),
            dbc.Col([
                metricas,
                graficos,
                tabla
            ], width=9)
        ])
    ], fluid=True)
])

# ============================================================
# CALLBACKS
# ============================================================

@callback(
    [Output('kpi-ventas', 'children'),
     Output('kpi-promedio', 'children'),
     Output('kpi-mejor', 'children'),
     Output('kpi-dias', 'children'),
     Output('grafico-tiempo', 'figure'),
     Output('grafico-categoria', 'figure'),
     Output('tabla-datos', 'children')],
    [Input('actualizar-btn', 'n_clicks')],
    [State('date-picker', 'start_date'),
     State('date-picker', 'end_date'),
     State('region-dropdown', 'value'),
     State('categoria-dropdown', 'value')]
)
def update_dashboard(n_clicks, start_date, end_date, region, categoria):
    """Actualiza todo el dashboard según filtros"""

    # Filtrar datos
    df_filtrado = df.copy()

    if start_date and end_date:
        df_filtrado = df_filtrado[
            (df_filtrado['fecha'] >= start_date) &
            (df_filtrado['fecha'] <= end_date)
        ]

    if region != 'ALL':
        df_filtrado = df_filtrado[df_filtrado['region'] == region]

    if categoria != 'ALL':
        df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria]

    # Calcular KPIs
    total_ventas = df_filtrado['ventas'].sum()
    promedio_diario = df_filtrado['ventas'].mean()
    mejor_dia = df_filtrado['ventas'].max()
    total_dias = len(df_filtrado)

    # Gráfico de tiempo
    fig_tiempo = px.line(
        df_filtrado,
        x='fecha',
        y='ventas',
        title='Evolución Temporal de Ventas'
    )
    fig_tiempo.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Ventas ($)",
        height=300
    )

    # Gráfico de categoría
    ventas_cat = df_filtrado.groupby('categoria')['ventas'].sum().reset_index()
    fig_categoria = px.pie(
        ventas_cat,
        values='ventas',
        names='categoria',
        title='Distribución por Categoría',
        hole=0.4
    )
    fig_categoria.update_layout(height=300)

    # Tabla
    df_tabla = df_filtrado.tail(10)[['fecha', 'categoria', 'region', 'ventas']]
    df_tabla['fecha'] = df_tabla['fecha'].dt.strftime('%Y-%m-%d')
    df_tabla['ventas'] = df_tabla['ventas'].apply(lambda x: f"${x:,.2f}")

    tabla_component = dbc.Table.from_dataframe(
        df_tabla,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size='sm'
    )

    return (
        f"${total_ventas:,.0f}",
        f"${promedio_diario:,.0f}",
        f"${mejor_dia:,.0f}",
        f"{total_dias}",
        fig_tiempo,
        fig_categoria,
        tabla_component
    )

# ============================================================
# RUN SERVER
# ============================================================

if __name__ == '__main__':
    app.run(debug=True, port=8050)
