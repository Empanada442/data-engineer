
"""
Dashboard de Análisis de Ventas
App creada con Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================

st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

@st.cache_data
def generar_datos_ventas(n=1000):
    """Genera datos de ventas aleatorios"""
    np.random.seed(42)

    fechas = pd.date_range(
        start='2023-01-01',
        end='2024-12-31',
        freq='h'
    )[:n]

    df = pd.DataFrame({
        'fecha': fechas,
        'producto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Webcam'], n),
        'categoria': np.random.choice(['Electrónica', 'Accesorios'], n),
        'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], n),
        'vendedor': np.random.choice(['Ana', 'Bruno', 'Carlos', 'Diana'], n),
        'cantidad': np.random.randint(1, 10, n),
        'precio_unitario': np.random.uniform(20, 1000, n)
    })

    df['total'] = df['cantidad'] * df['precio_unitario']
    df['año'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month
    df['dia_semana'] = df['fecha'].dt.day_name()

    return df

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Configuración")

# Selector de fecha
fecha_inicio = st.sidebar.date_input(
    "Fecha inicio",
    value=pd.to_datetime('2023-01-01')
)

fecha_fin = st.sidebar.date_input(
    "Fecha fin",
    value=pd.to_datetime('2024-12-31')
)

# Filtros
st.sidebar.subheader("🔍 Filtros")

# ============================================================
# CARGAR DATOS
# ============================================================

df = generar_datos_ventas()

# Aplicar filtro de fechas
df_filtrado = df[
    (df['fecha'].dt.date >= fecha_inicio) &
    (df['fecha'].dt.date <= fecha_fin)
].copy()

# Filtros de sidebar
regiones = st.sidebar.multiselect(
    "Regiones",
    options=df_filtrado['region'].unique(),
    default=df_filtrado['region'].unique()
)

productos = st.sidebar.multiselect(
    "Productos",
    options=df_filtrado['producto'].unique(),
    default=df_filtrado['producto'].unique()
)

# Aplicar filtros
df_filtrado = df_filtrado[
    (df_filtrado['region'].isin(regiones)) &
    (df_filtrado['producto'].isin(productos))
]

# ============================================================
# HEADER
# ============================================================

st.title("📊 Dashboard de Análisis de Ventas")
st.markdown("---")

# Mostrar info de filtros
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"📅 Período: {fecha_inicio} - {fecha_fin}")
with col2:
    st.info(f"📍 Regiones: {len(regiones)}")
with col3:
    st.info(f"📦 Productos: {len(productos)}")

st.markdown("---")

# ============================================================
# MÉTRICAS PRINCIPALES (KPIs)
# ============================================================

st.subheader("📈 Métricas Principales")

# Calcular métricas
total_ventas = df_filtrado['total'].sum()
total_transacciones = len(df_filtrado)
ticket_promedio = df_filtrado['total'].mean()
total_unidades = df_filtrado['cantidad'].sum()

# Calcular cambio vs mes anterior (simulado)
cambio_ventas = np.random.uniform(-10, 20)
cambio_transacciones = np.random.uniform(-5, 15)
cambio_ticket = np.random.uniform(-8, 12)
cambio_unidades = np.random.uniform(-3, 18)

# Mostrar métricas en columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Ventas",
        value=f"${total_ventas:,.0f}",
        delta=f"{cambio_ventas:+.1f}%"
    )

with col2:
    st.metric(
        label="🛒 Transacciones",
        value=f"{total_transacciones:,}",
        delta=f"{cambio_transacciones:+.1f}%"
    )

with col3:
    st.metric(
        label="🎫 Ticket Promedio",
        value=f"${ticket_promedio:,.2f}",
        delta=f"{cambio_ticket:+.1f}%"
    )

with col4:
    st.metric(
        label="📦 Unidades Vendidas",
        value=f"{total_unidades:,}",
        delta=f"{cambio_unidades:+.1f}%"
    )

st.markdown("---")

# ============================================================
# VISUALIZACIONES
# ============================================================

# Tabs para organizar visualizaciones
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tendencias", "📊 Categorías", "🗺️ Regiones", "📋 Datos"])

# --- TAB 1: TENDENCIAS ---
with tab1:
    st.subheader("Evolución de Ventas en el Tiempo")

    # Agrupar por fecha
    ventas_tiempo = df_filtrado.groupby(df_filtrado['fecha'].dt.date)['total'].sum().reset_index()
    ventas_tiempo.columns = ['fecha', 'ventas']

    fig = px.line(
        ventas_tiempo,
        x='fecha',
        y='ventas',
        title='Ventas Diarias',
        labels={'ventas': 'Ventas ($)', 'fecha': 'Fecha'}
    )
    fig.update_traces(line_color='#1f77b4', line_width=2)
    fig.update_layout(height=400, hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

    # Ventas por día de la semana
    st.subheader("Ventas por Día de la Semana")

    ventas_dia = df_filtrado.groupby('dia_semana')['total'].sum().reset_index()
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ventas_dia['dia_semana'] = pd.Categorical(ventas_dia['dia_semana'], categories=order, ordered=True)
    ventas_dia = ventas_dia.sort_values('dia_semana')

    fig = px.bar(
        ventas_dia,
        x='dia_semana',
        y='total',
        title='Distribución Semanal de Ventas',
        labels={'total': 'Ventas ($)', 'dia_semana': 'Día'},
        color='total',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: CATEGORÍAS ---
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ventas por Producto")

        ventas_producto = df_filtrado.groupby('producto')['total'].sum().reset_index()
        ventas_producto = ventas_producto.sort_values('total', ascending=False)

        fig = px.bar(
            ventas_producto,
            x='producto',
            y='total',
            color='producto',
            title='Total de Ventas por Producto'
        )
        fig.update_layout(showlegend=False, height=400)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribución por Categoría")

        ventas_categoria = df_filtrado.groupby('categoria')['total'].sum().reset_index()

        fig = px.pie(
            ventas_categoria,
            values='total',
            names='categoria',
            title='Proporción de Ventas por Categoría',
            hole=0.4
        )
        fig.update_layout(height=400)

        st.plotly_chart(fig, use_container_width=True)

    # Tabla de productos
    st.subheader("Top 10 Productos")

    top_productos = df_filtrado.groupby('producto').agg({
        'total': 'sum',
        'cantidad': 'sum',
        'fecha': 'count'
    }).round(2)
    top_productos.columns = ['Ventas Totales', 'Unidades', 'Transacciones']
    top_productos = top_productos.sort_values('Ventas Totales', ascending=False).head(10)

    st.dataframe(top_productos, use_container_width=True)

# --- TAB 3: REGIONES ---
with tab3:
    st.subheader("Análisis por Región")

    col1, col2 = st.columns(2)

    with col1:
        ventas_region = df_filtrado.groupby('region')['total'].sum().reset_index()

        fig = px.bar(
            ventas_region,
            x='region',
            y='total',
            color='region',
            title='Ventas por Región',
            labels={'total': 'Ventas ($)', 'region': 'Región'}
        )
        fig.update_layout(showlegend=False, height=400)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Vendedores por región
        ventas_vendedor = df_filtrado.groupby(['region', 'vendedor'])['total'].sum().reset_index()

        fig = px.bar(
            ventas_vendedor,
            x='region',
            y='total',
            color='vendedor',
            title='Ventas por Región y Vendedor',
            labels={'total': 'Ventas ($)', 'region': 'Región'},
            barmode='group'
        )
        fig.update_layout(height=400)

        st.plotly_chart(fig, use_container_width=True)

    # Heatmap: producto x región
    st.subheader("Mapa de Calor: Producto x Región")

    heatmap_data = df_filtrado.pivot_table(
        values='total',
        index='producto',
        columns='region',
        aggfunc='sum'
    ).fillna(0)

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues',
        text=np.round(heatmap_data.values, 0),
        texttemplate='$%{text:,.0f}',
        textfont={"size": 10},
        colorbar=dict(title="Ventas ($)")
    ))

    fig.update_layout(
        title='Ventas por Producto y Región',
        xaxis_title='Región',
        yaxis_title='Producto',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

# --- TAB 4: DATOS ---
with tab4:
    st.subheader("📋 Datos Detallados")

    # Opciones de visualización
    col1, col2, col3 = st.columns(3)

    with col1:
        mostrar_filas = st.number_input(
            "Filas a mostrar",
            min_value=10,
            max_value=len(df_filtrado),
            value=min(100, len(df_filtrado)),
            step=10
        )

    with col2:
        ordenar_por = st.selectbox(
            "Ordenar por",
            options=['fecha', 'total', 'cantidad', 'producto']
        )

    with col3:
        orden = st.radio(
            "Orden",
            options=['Descendente', 'Ascendente']
        )

    # Mostrar datos
    df_mostrar = df_filtrado.sort_values(
        by=ordenar_por,
        ascending=(orden == 'Ascendente')
    ).head(mostrar_filas)

    st.dataframe(
        df_mostrar[['fecha', 'producto', 'categoria', 'region', 
                   'vendedor', 'cantidad', 'precio_unitario', 'total']],
        use_container_width=True
    )

    # Botón de descarga
    csv = df_filtrado.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Descargar datos filtrados (CSV)",
        data=csv,
        file_name=f'ventas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv'
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Dashboard creado con Streamlit 🚀</p>
        <p>Datos generados aleatoriamente para demostración</p>
    </div>
""", unsafe_allow_html=True)
