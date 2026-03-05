# ================= LIBRERÍAS =================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar
from datetime import datetime, timedelta
import numpy as np
import random
from streamlit_option_menu import option_menu

# ================= CONFIGURACIÓN INICIAL =================
st.set_page_config(
    page_title="Planifica360 | Finanzas Inteligentes",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= ESTILOS CSS PREMIUM =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&family=Space+Mono:wght@400;700&display=swap');
    
    :root {
        --bg-primary: #0A0E1A;
        --bg-secondary: #111827;
        --bg-card: #151D2E;
        --bg-card-hover: #1C2640;
        --accent-gold: #F5C842;
        --accent-emerald: #10D9A0;
        --accent-rose: #F56565;
        --accent-blue: #4A90E2;
        --accent-purple: #9B59B6;
        --text-primary: #F0F4FF;
        --text-secondary: #8896B3;
        --text-muted: #4A5568;
        --border: rgba(255,255,255,0.06);
        --border-accent: rgba(245,200,66,0.3);
        --glow-gold: 0 0 30px rgba(245,200,66,0.15);
        --glow-emerald: 0 0 30px rgba(16,217,160,0.15);
    }

    * { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }
    
    /* ===== FONDO DARK PREMIUM ===== */
    .stApp {
        background: var(--bg-primary) !important;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: 
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(74,144,226,0.08) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(245,200,66,0.05) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }
    
    /* ===== LABELS & TEXT ===== */
    .stTextInput label, .stNumberInput label, .stSelectbox label,
    .stSlider label, .stExpander label {
        color: var(--text-secondary) !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }
    
    /* ===== INPUTS ===== */
    .stNumberInput input, .stTextInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-size: 14px !important;
        transition: all 0.2s !important;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 2px rgba(245,200,66,0.15) !important;
        background: rgba(245,200,66,0.04) !important;
    }
    
    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    /* ===== BOTONES ===== */
    .stButton > button {
        background: linear-gradient(135deg, #F5C842, #E8A020) !important;
        color: #0A0E1A !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 20px rgba(245,200,66,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(245,200,66,0.4) !important;
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* ===== METRIC ===== */
    [data-testid="stMetricValue"] {
        font-family: 'Space Mono', monospace !important;
        color: var(--text-primary) !important;
        font-size: 20px !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 12px !important;
    }
    
    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #F5C842, #10D9A0) !important;
        border-radius: 10px !important;
    }
    
    .stProgress > div {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
    }
    
    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 50px !important;
        padding: 6px !important;
        gap: 4px !important;
        border: 1px solid var(--border) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 50px !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 8px 20px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #F5C842, #E8A020) !important;
        color: #0A0E1A !important;
        font-weight: 700 !important;
    }
    
    /* ===== SLIDER ===== */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #F5C842, #10D9A0) !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(245,200,66,0.5); }
    
    /* ===== CARDS CUSTOM ===== */
    .card-dark {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .card-dark:hover {
        border-color: rgba(245,200,66,0.2);
        box-shadow: var(--glow-gold);
    }
    
    .card-metric {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .card-metric::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
    }
    
    .card-metric.gold::before { background: linear-gradient(90deg, #F5C842, #E8A020); }
    .card-metric.emerald::before { background: linear-gradient(90deg, #10D9A0, #06B6D4); }
    .card-metric.rose::before { background: linear-gradient(90deg, #F56565, #E53E3E); }
    .card-metric.blue::before { background: linear-gradient(90deg, #4A90E2, #7C3AED); }
    
    .metric-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-family: 'Space Mono', monospace;
        font-size: 22px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
    }
    
    .metric-sub {
        font-size: 12px;
        color: var(--text-secondary);
    }
    
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 50px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-success { background: rgba(16,217,160,0.15); color: #10D9A0; }
    .badge-warning { background: rgba(245,200,66,0.15); color: #F5C842; }
    .badge-danger { background: rgba(245,101,101,0.15); color: #F56565; }
    
    .income-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 28px;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
    
    .section-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin-bottom: 24px;
    }
    
    .divider {
        height: 1px;
        background: var(--border);
        margin: 20px 0;
    }
    
    .sidebar-section-title {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--text-muted);
        padding: 16px 0 8px 0;
    }
    
    .tag-income {
        background: rgba(16,217,160,0.1);
        border: 1px solid rgba(16,217,160,0.2);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 11px;
        color: #10D9A0;
        font-weight: 600;
    }
    
    /* Override default streamlit backgrounds */
    .main > div { background: transparent !important; }
    .block-container { padding-top: 2rem !important; }
    
    /* Markdown text */
    .stMarkdown p, .stMarkdown li { color: var(--text-secondary) !important; }
    
    /* Alerts */
    .stAlert { border-radius: 12px !important; border: none !important; }
    
    /* Number input arrows */
    .stNumberInput button {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: none !important;
        box-shadow: none !important;
        padding: 4px !important;
        transform: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE PARA INGRESOS DINÁMICOS =================
if 'ingresos_lista' not in st.session_state:
    st.session_state.ingresos_lista = [
        {"nombre": "Salario Principal", "monto": 3500.0, "tipo": "Fijo", "frecuencia": "Mensual"},
        {"nombre": "Freelance", "monto": 500.0, "tipo": "Variable", "frecuencia": "Mensual"},
        {"nombre": "Dividendos", "monto": 200.0, "tipo": "Pasivo", "frecuencia": "Mensual"},
    ]

if 'gastos_extra' not in st.session_state:
    st.session_state.gastos_extra = []

if 'metas_lista' not in st.session_state:
    st.session_state.metas_lista = [
        {"nombre": "Fondo de Emergencia", "meta": 20000.0, "actual": 15000.0, "color": "#F5C842"},
        {"nombre": "Vacaciones", "meta": 5000.0, "actual": 2000.0, "color": "#10D9A0"},
        {"nombre": "Auto Nuevo", "meta": 50000.0, "actual": 5000.0, "color": "#4A90E2"},
    ]

# ================= FUNCIONES =================
def format_currency(amount):
    return f"S/ {amount:,.2f}"

def format_currency_short(amount):
    if amount >= 1_000_000:
        return f"S/ {amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"S/ {amount/1_000:.1f}K"
    return f"S/ {amount:,.0f}"

def calculate_financial_health(income, expenses, savings):
    if income <= 0: return 0
    savings_rate = (income - expenses) / income * 100
    expense_rate = expenses / income * 100
    score = 0
    if savings_rate >= 20: score += 40
    elif savings_rate >= 10: score += 30
    elif savings_rate >= 0: score += 20
    if expense_rate <= 50: score += 30
    elif expense_rate <= 70: score += 20
    elif expense_rate <= 90: score += 10
    if savings > income * 3: score += 30
    elif savings > income * 1: score += 20
    elif savings > 0: score += 10
    return min(score, 100)

def plotly_dark_layout(fig, height=400):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#8896B3'),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            bgcolor='rgba(21,29,46,0.8)',
            bordercolor='rgba(255,255,255,0.06)',
            borderwidth=1,
            font=dict(color='#8896B3')
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.06)',
            tickfont=dict(color='#8896B3')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.06)',
            tickfont=dict(color='#8896B3')
        )
    )
    return fig

# ================= SIDEBAR =================
with st.sidebar:
    # Logo & Header
    st.markdown("""
    <div style="padding: 12px 0 20px 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:42px; height:42px; background:linear-gradient(135deg,#F5C842,#E8A020); 
                        border-radius:12px; display:flex; align-items:center; justify-content:center;
                        font-size:20px;">💎</div>
            <div>
                <div style="font-family:'DM Serif Display',serif; font-size:18px; color:#F0F4FF; font-weight:700;">Planifica360</div>
                <div style="font-size:11px; color:#4A5568; text-transform:uppercase; letter-spacing:0.1em;">Finanzas Inteligentes</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nombre
    st.markdown('<div class="sidebar-section-title">👤 Tu Perfil</div>', unsafe_allow_html=True)
    nombre = st.text_input("Nombre", value="Usuario", label_visibility="collapsed", placeholder="Tu nombre")
    
    # ===== INGRESOS DINÁMICOS =====
    st.markdown('<div class="sidebar-section-title">💰 Fuentes de Ingreso</div>', unsafe_allow_html=True)
    
    # Mostrar ingresos actuales
    for i, ingreso in enumerate(st.session_state.ingresos_lista):
        col_a, col_b = st.columns([3,1])
        with col_a:
            tipo_icons = {"Fijo": "🔵", "Variable": "🟡", "Pasivo": "🟢"}
            icon = tipo_icons.get(ingreso["tipo"], "⚪")
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);
                        border-radius:10px; padding:8px 12px; margin-bottom:6px;">
                <div style="font-size:11px; color:#8896B3;">{icon} {ingreso['tipo']}</div>
                <div style="font-size:13px; color:#F0F4FF; font-weight:600;">{ingreso['nombre']}</div>
                <div style="font-family:'Space Mono',monospace; font-size:14px; color:#F5C842;">{format_currency(ingreso['monto'])}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            if st.button("✕", key=f"del_ing_{i}", help="Eliminar"):
                st.session_state.ingresos_lista.pop(i)
                st.rerun()
    
    # Agregar nuevo ingreso
    with st.expander("➕ Agregar Ingreso", expanded=False):
        nuevo_nombre = st.text_input("Nombre del ingreso", key="new_ing_name", placeholder="Ej: Consultoría")
        nuevo_monto = st.number_input("Monto mensual (S/)", min_value=0.0, value=0.0, step=100.0, key="new_ing_monto")
        nuevo_tipo = st.selectbox("Tipo", ["Fijo", "Variable", "Pasivo", "Bono"], key="new_ing_tipo")
        nuevo_freq = st.selectbox("Frecuencia", ["Mensual", "Quincenal", "Semanal", "Anual"], key="new_ing_freq")
        
        if st.button("Agregar Ingreso", key="add_ingreso"):
            if nuevo_nombre and nuevo_monto > 0:
                # Normalizar a mensual
                monto_mensual = nuevo_monto
                if nuevo_freq == "Quincenal": monto_mensual = nuevo_monto * 2
                elif nuevo_freq == "Semanal": monto_mensual = nuevo_monto * 4.33
                elif nuevo_freq == "Anual": monto_mensual = nuevo_monto / 12
                
                st.session_state.ingresos_lista.append({
                    "nombre": nuevo_nombre,
                    "monto": monto_mensual,
                    "tipo": nuevo_tipo,
                    "frecuencia": nuevo_freq
                })
                st.rerun()
    
    # Ahorros
    st.markdown('<div class="sidebar-section-title">🏦 Patrimonio</div>', unsafe_allow_html=True)
    ahorro_actual = st.number_input("Ahorro Acumulado (S/)", min_value=0.0, value=15000.0, step=1000.0)
    inversiones = st.number_input("Inversiones (S/)", min_value=0.0, value=5000.0, step=500.0)
    deudas = st.number_input("Deudas Totales (S/)", min_value=0.0, value=3000.0, step=500.0)
    
    # Gastos
    st.markdown('<div class="sidebar-section-title">📊 Gastos Mensuales</div>', unsafe_allow_html=True)
    
    with st.expander("🏠 Vivienda"):
        alquiler = st.number_input("Alquiler/Hipoteca", min_value=0.0, value=1200.0, step=50.0)
        servicios = st.number_input("Servicios básicos", min_value=0.0, value=200.0, step=10.0)
        internet = st.number_input("Internet/Telefonía", min_value=0.0, value=80.0, step=5.0)
        mantenimiento = st.number_input("Mantenimiento", min_value=0.0, value=50.0, step=10.0)
    
    with st.expander("🚗 Transporte"):
        transporte_pub = st.number_input("Transporte Público", min_value=0.0, value=150.0, step=10.0)
        gasolina = st.number_input("Gasolina", min_value=0.0, value=200.0, step=10.0)
        mantenimiento_auto = st.number_input("Mant. Vehículo", min_value=0.0, value=100.0, step=10.0)
        estacionamiento = st.number_input("Estacionamiento", min_value=0.0, value=50.0, step=5.0)
    
    with st.expander("🍽️ Alimentación"):
        supermercado = st.number_input("Supermercado", min_value=0.0, value=600.0, step=50.0)
        restaurantes = st.number_input("Restaurantes", min_value=0.0, value=300.0, step=20.0)
        delivery = st.number_input("Delivery", min_value=0.0, value=150.0, step=10.0)
        cafes = st.number_input("Cafés/Snacks", min_value=0.0, value=100.0, step=5.0)
    
    with st.expander("🎮 Ocio & Bienestar"):
        streaming = st.number_input("Streaming", min_value=0.0, value=50.0, step=5.0)
        salidas = st.number_input("Salidas", min_value=0.0, value=200.0, step=20.0)
        deportes = st.number_input("Deportes/Gym", min_value=0.0, value=100.0, step=10.0)
        hobbies = st.number_input("Hobbies", min_value=0.0, value=150.0, step=10.0)
    
    with st.expander("📚 Educación & Salud"):
        educacion = st.number_input("Educación", min_value=0.0, value=200.0, step=20.0)
        salud = st.number_input("Salud/Medicamentos", min_value=0.0, value=150.0, step=10.0)
        suscripciones = st.number_input("Suscripciones", min_value=0.0, value=30.0, step=5.0)
        otros = st.number_input("Otros", min_value=0.0, value=100.0, step=10.0)
    
    # Gastos extra
    with st.expander("➕ Gastos Extraordinarios"):
        g_nombre = st.text_input("Nombre del gasto", key="gasto_nombre", placeholder="Ej: Viaje")
        g_monto = st.number_input("Monto (S/)", min_value=0.0, value=0.0, step=50.0, key="gasto_monto")
        if st.button("Agregar Gasto", key="add_gasto"):
            if g_nombre and g_monto > 0:
                st.session_state.gastos_extra.append({"nombre": g_nombre, "monto": g_monto})
                st.rerun()
        
        for idx, ge in enumerate(st.session_state.gastos_extra):
            st.write(f"• {ge['nombre']}: {format_currency(ge['monto'])}")

# ================= CÁLCULOS =================
ingreso_total = sum(i["monto"] for i in st.session_state.ingresos_lista)
ingresos_fijos = sum(i["monto"] for i in st.session_state.ingresos_lista if i["tipo"] == "Fijo")
ingresos_variables = sum(i["monto"] for i in st.session_state.ingresos_lista if i["tipo"] == "Variable")
ingresos_pasivos_total = sum(i["monto"] for i in st.session_state.ingresos_lista if i["tipo"] == "Pasivo")

total_vivienda = alquiler + servicios + internet + mantenimiento
total_transporte = transporte_pub + gasolina + mantenimiento_auto + estacionamiento
total_alimentacion = supermercado + restaurantes + delivery + cafes
total_entretenimiento = streaming + salidas + deportes + hobbies
total_otros = educacion + salud + suscripciones + otros
total_extras_gastos = sum(g["monto"] for g in st.session_state.gastos_extra)

total_gastos = (total_vivienda + total_transporte + total_alimentacion + 
                total_entretenimiento + total_otros + total_extras_gastos)

saldo = ingreso_total - total_gastos
patrimonio_neto = ahorro_actual + inversiones - deudas
patrimonio_total = ahorro_actual + inversiones
ahorro_mensual = max(saldo * 0.7, 0)
tasa_ahorro = (saldo / ingreso_total * 100) if ingreso_total > 0 else 0
salud_financiera = calculate_financial_health(ingreso_total, total_gastos, ahorro_actual)

# ================= NAVEGACIÓN =================
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Ingresos", "Gastos", "Proyecciones", "Metas", "Consejos"],
    icons=["grid", "cash-coin", "credit-card", "graph-up-arrow", "trophy", "lightbulb"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "6px", 
            "background-color": "rgba(255,255,255,0.04)", 
            "border-radius": "50px",
            "margin-bottom": "24px",
            "border": "1px solid rgba(255,255,255,0.06)"
        },
        "icon": {"color": "#8896B3", "font-size": "14px"},
        "nav-link": {
            "font-size": "13px", "font-weight": "600",
            "text-align": "center", "margin": "0px",
            "color": "#8896B3", "border-radius": "50px",
            "padding": "10px 20px"
        },
        "nav-link-selected": {
            "background": "linear-gradient(135deg, #F5C842, #E8A020)",
            "color": "#0A0E1A",
            "font-weight": "700"
        },
    }
)

# ============================================================
# DASHBOARD
# ============================================================
if selected == "Dashboard":
    # Header
    hora = datetime.now().hour
    saludo = "Buenos días" if hora < 12 else "Buenas tardes" if hora < 18 else "Buenas noches"
    
    col_h1, col_h2 = st.columns([3,1])
    with col_h1:
        st.markdown(f"""
        <div style="margin-bottom: 28px;">
            <div style="font-size:13px; color:#8896B3; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px;">
                {saludo} 👋
            </div>
            <div style="font-family:'DM Serif Display',serif; font-size:36px; color:#F0F4FF; line-height:1.1; margin-bottom:6px;">
                {nombre}, aquí está tu<br>resumen financiero
            </div>
            <div style="font-size:14px; color:#4A5568;">
                {datetime.now().strftime("%A, %d de %B de %Y")}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        # Health Score circular
        color_score = "#10D9A0" if salud_financiera >= 70 else "#F5C842" if salud_financiera >= 40 else "#F56565"
        estado = "Excelente" if salud_financiera >= 70 else "Regular" if salud_financiera >= 40 else "Crítico"
        st.markdown(f"""
        <div style="background: rgba(21,29,46,0.8); border: 1px solid rgba(255,255,255,0.06); 
                    border-radius:20px; padding:20px; text-align:center; margin-top:10px;">
            <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:#8896B3; margin-bottom:8px;">Health Score</div>
            <div style="font-family:'Space Mono',monospace; font-size:48px; font-weight:700; color:{color_score}; line-height:1;">{salud_financiera:.0f}</div>
            <div style="font-size:12px; color:{color_score}; margin-top:4px; font-weight:600;">◉ {estado}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    
    cards_data = [
        ("gold", "💵 Ingreso Total", ingreso_total, f"{len(st.session_state.ingresos_lista)} fuentes activas"),
        ("rose", "💳 Gastos Totales", total_gastos, f"{total_gastos/ingreso_total*100:.1f}% del ingreso" if ingreso_total > 0 else "—"),
        ("emerald", "📈 Saldo Libre", saldo, f"Tasa ahorro: {tasa_ahorro:.1f}%"),
        ("blue", "🏛️ Patrimonio Neto", patrimonio_neto, f"Inversiones: {format_currency_short(inversiones)}"),
    ]
    
    for col, (color, label, value, sub) in zip([c1, c2, c3, c4], cards_data):
        with col:
            badge_class = "badge-success" if (value >= 0 or color in ["gold","blue"]) else "badge-danger"
            badge_text = "▲ positivo" if value >= 0 else "▼ negativo"
            st.markdown(f"""
            <div class="card-metric {color}">
                <div class="metric-label" style="color:#8896B3;">{label}</div>
                <div class="metric-value">{format_currency(value)}</div>
                <div class="metric-sub">{sub}</div>
                <div style="margin-top:10px;">
                    <span class="badge {badge_class}">{badge_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    # Gráficos principales
    col_g1, col_g2 = st.columns([5,4])
    
    with col_g1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:16px; font-weight:600; color:#F0F4FF; margin-bottom:16px;">📊 Ingresos vs Gastos — Últimos 6 meses</div>', unsafe_allow_html=True)
        
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        np.random.seed(42)
        ingresos_hist = [ingreso_total * (0.9 + np.random.random() * 0.2) for _ in range(6)]
        gastos_hist = [total_gastos * (0.85 + np.random.random() * 0.3) for _ in range(6)]
        ahorros_hist = [max(i - g, 0) for i, g in zip(ingresos_hist, gastos_hist)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Ingresos', x=meses, y=ingresos_hist,
                            marker_color='rgba(16,217,160,0.8)', marker_line_width=0, 
                            width=0.3, offset=-0.17))
        fig.add_trace(go.Bar(name='Gastos', x=meses, y=gastos_hist,
                            marker_color='rgba(245,101,101,0.8)', marker_line_width=0,
                            width=0.3, offset=0.17))
        fig.add_trace(go.Scatter(name='Ahorro', x=meses, y=ahorros_hist,
                                mode='lines+markers',
                                line=dict(color='#F5C842', width=2.5),
                                marker=dict(size=8, color='#F5C842', symbol='circle')))
        
        fig = plotly_dark_layout(fig, 320)
        fig.update_layout(barmode='overlay', bargap=0.4, showlegend=True,
                         legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_g2:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:16px; font-weight:600; color:#F0F4FF; margin-bottom:16px;">🍩 Distribución de Gastos</div>', unsafe_allow_html=True)
        
        cats = ['Vivienda', 'Transporte', 'Alimentación', 'Ocio', 'Otros']
        montos = [total_vivienda, total_transporte, total_alimentacion, total_entretenimiento, total_otros + total_extras_gastos]
        colors_pie = ['#4A90E2', '#F5C842', '#10D9A0', '#9B59B6', '#F56565']
        
        fig2 = go.Figure(data=[go.Pie(
            labels=cats, values=montos, hole=0.65,
            marker=dict(colors=colors_pie, line=dict(color='#0A0E1A', width=2)),
            textinfo='percent',
            textfont=dict(size=12, color='white'),
            hovertemplate="<b>%{label}</b><br>%{value:,.2f} S/<br>%{percent}<extra></extra>"
        )])
        
        fig2.add_annotation(
            text=f"<b>{format_currency_short(total_gastos)}</b>",
            x=0.5, y=0.55, font_size=16, showarrow=False,
            font=dict(color='#F0F4FF', family='Space Mono')
        )
        fig2.add_annotation(
            text="Total Gastos",
            x=0.5, y=0.42, font_size=11, showarrow=False,
            font=dict(color='#8896B3', family='DM Sans')
        )
        
        fig2 = plotly_dark_layout(fig2, 320)
        fig2.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1, x=0.1, font=dict(size=11)))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights Row
    st.markdown('<div style="font-size:16px; font-weight:600; color:#F0F4FF; margin:20px 0 12px 0;">⚡ Alertas & Insights</div>', unsafe_allow_html=True)
    
    icol1, icol2, icol3, icol4 = st.columns(4)
    
    with icol1:
        meses_emerg = ahorro_actual / total_gastos if total_gastos > 0 else 0
        color_e = "#10D9A0" if meses_emerg >= 6 else "#F5C842" if meses_emerg >= 3 else "#F56565"
        icon_e = "✅" if meses_emerg >= 6 else "⚠️" if meses_emerg >= 3 else "🔴"
        st.markdown(f"""
        <div style="background:rgba(21,29,46,0.6); border:1px solid rgba(255,255,255,0.06); 
                    border-left: 3px solid {color_e}; border-radius:12px; padding:16px;">
            <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:#8896B3; margin-bottom:6px;">Fondo Emergencia</div>
            <div style="font-family:'Space Mono',monospace; font-size:22px; font-weight:700; color:{color_e};">{meses_emerg:.1f}m</div>
            <div style="font-size:12px; color:#4A5568;">{icon_e} Meta: 6 meses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with icol2:
        ratio_vivienda = total_vivienda / ingreso_total * 100 if ingreso_total > 0 else 0
        color_v = "#10D9A0" if ratio_vivienda <= 30 else "#F5C842" if ratio_vivienda <= 50 else "#F56565"
        st.markdown(f"""
        <div style="background:rgba(21,29,46,0.6); border:1px solid rgba(255,255,255,0.06); 
                    border-left: 3px solid {color_v}; border-radius:12px; padding:16px;">
            <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:#8896B3; margin-bottom:6px;">% en Vivienda</div>
            <div style="font-family:'Space Mono',monospace; font-size:22px; font-weight:700; color:{color_v};">{ratio_vivienda:.1f}%</div>
            <div style="font-size:12px; color:#4A5568;">Ideal: ≤ 30%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with icol3:
        color_a = "#10D9A0" if tasa_ahorro >= 20 else "#F5C842" if tasa_ahorro >= 10 else "#F56565"
        st.markdown(f"""
        <div style="background:rgba(21,29,46,0.6); border:1px solid rgba(255,255,255,0.06); 
                    border-left: 3px solid {color_a}; border-radius:12px; padding:16px;">
            <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:#8896B3; margin-bottom:6px;">Tasa de Ahorro</div>
            <div style="font-family:'Space Mono',monospace; font-size:22px; font-weight:700; color:{color_a};">{tasa_ahorro:.1f}%</div>
            <div style="font-size:12px; color:#4A5568;">Ideal: ≥ 20%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with icol4:
        ratio_deuda = deudas / ingreso_total * 100 if ingreso_total > 0 else 0
        color_d = "#10D9A0" if ratio_deuda <= 20 else "#F5C842" if ratio_deuda <= 40 else "#F56565"
        st.markdown(f"""
        <div style="background:rgba(21,29,46,0.6); border:1px solid rgba(255,255,255,0.06); 
                    border-left: 3px solid {color_d}; border-radius:12px; padding:16px;">
            <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:#8896B3; margin-bottom:6px;">Ratio de Deuda</div>
            <div style="font-family:'Space Mono',monospace; font-size:22px; font-weight:700; color:{color_d};">{ratio_deuda:.1f}%</div>
            <div style="font-size:12px; color:#4A5568;">Ideal: ≤ 20%</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# INGRESOS
# ============================================================
elif selected == "Ingresos":
    st.markdown('<div class="section-title">💰 Gestión de Ingresos</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Administra y analiza todas tus fuentes de ingreso</div>', unsafe_allow_html=True)
    
    col_i1, col_i2 = st.columns([3,2])
    
    with col_i1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:15px; font-weight:600; color:#F0F4FF; margin-bottom:16px;">Todas tus fuentes de ingreso</div>', unsafe_allow_html=True)
        
        if not st.session_state.ingresos_lista:
            st.markdown('<div style="text-align:center; color:#4A5568; padding:40px;">No tienes ingresos registrados</div>', unsafe_allow_html=True)
        
        for i, ingreso in enumerate(st.session_state.ingresos_lista):
            pct = ingreso["monto"] / ingreso_total * 100 if ingreso_total > 0 else 0
            tipo_color = {"Fijo": "#4A90E2", "Variable": "#F5C842", "Pasivo": "#10D9A0", "Bono": "#9B59B6"}
            color = tipo_color.get(ingreso["tipo"], "#8896B3")
            
            c_a, c_b, c_c = st.columns([4,2,1])
            with c_a:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);
                            border-left: 3px solid {color}; border-radius:12px; padding:14px 16px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-size:14px; font-weight:600; color:#F0F4FF;">{ingreso['nombre']}</div>
                            <div style="font-size:11px; color:#4A5568; margin-top:2px;">{ingreso['tipo']} · {ingreso['frecuencia']} · {pct:.1f}% del total</div>
                        </div>
                        <div style="font-family:'Space Mono',monospace; font-size:16px; color:{color}; font-weight:700;">
                            {format_currency(ingreso['monto'])}
                        </div>
                    </div>
                    <div style="margin-top:10px; background:rgba(255,255,255,0.06); border-radius:10px; height:4px; overflow:hidden;">
                        <div style="width:{pct}%; height:100%; background:{color}; border-radius:10px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c_b:
                nuevo_monto_edit = st.number_input("", value=ingreso["monto"], step=100.0, 
                                                   key=f"edit_monto_{i}", label_visibility="collapsed")
                if nuevo_monto_edit != ingreso["monto"]:
                    st.session_state.ingresos_lista[i]["monto"] = nuevo_monto_edit
                    st.rerun()
            with c_c:
                if st.button("🗑️", key=f"del2_ing_{i}"):
                    st.session_state.ingresos_lista.pop(i)
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_i2:
        # Resumen de ingresos
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:15px; font-weight:600; color:#F0F4FF; margin-bottom:16px;">Resumen por tipo</div>', unsafe_allow_html=True)
        
        tipos = {}
        for ing in st.session_state.ingresos_lista:
            tipos[ing["tipo"]] = tipos.get(ing["tipo"], 0) + ing["monto"]
        
        tipo_colors = {"Fijo": "#4A90E2", "Variable": "#F5C842", "Pasivo": "#10D9A0", "Bono": "#9B59B6"}
        
        for tipo, monto in tipos.items():
            pct = monto / ingreso_total * 100 if ingreso_total > 0 else 0
            color = tipo_colors.get(tipo, "#8896B3")
            st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="font-size:13px; color:#8896B3; font-weight:500;">{tipo}</span>
                    <span style="font-family:'Space Mono',monospace; font-size:13px; color:{color};">{format_currency(monto)}</span>
                </div>
                <div style="background:rgba(255,255,255,0.06); border-radius:10px; height:6px; overflow:hidden;">
                    <div style="width:{pct}%; height:100%; background:{color}; border-radius:10px;"></div>
                </div>
                <div style="text-align:right; font-size:11px; color:#4A5568; margin-top:3px;">{pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="border-top:1px solid rgba(255,255,255,0.06); margin-top:10px; padding-top:14px;
                    display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:13px; font-weight:600; color:#F0F4FF;">TOTAL MENSUAL</span>
            <span style="font-family:'Space Mono',monospace; font-size:20px; color:#F5C842; font-weight:700;">{format_currency(ingreso_total)}</span>
        </div>
        <div style="text-align:right; font-size:11px; color:#4A5568; margin-top:2px;">
            Anual: {format_currency(ingreso_total * 12)}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráfico de pie de ingresos
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:15px; font-weight:600; color:#F0F4FF; margin-bottom:12px;">Composición de ingresos</div>', unsafe_allow_html=True)
        
        nombres = [i["nombre"] for i in st.session_state.ingresos_lista]
        montos_ing = [i["monto"] for i in st.session_state.ingresos_lista]
        
        if sum(montos_ing) > 0:
            fig_ing = go.Figure(data=[go.Pie(
                labels=nombres, values=montos_ing, hole=0.6,
                marker=dict(colors=['#4A90E2','#F5C842','#10D9A0','#9B59B6','#F56565','#F97316'],
                           line=dict(color='#0A0E1A', width=2)),
                textinfo='percent',
                textfont=dict(size=11, color='white'),
            )])
            fig_ing = plotly_dark_layout(fig_ing, 240)
            fig_ing.update_layout(showlegend=True, legend=dict(font=dict(size=10), y=0.5))
            st.plotly_chart(fig_ing, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# GASTOS
# ============================================================
elif selected == "Gastos":
    st.markdown('<div class="section-title">💳 Análisis de Gastos</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Radiografía completa de tus egresos mensuales</div>', unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns([3,2])
    
    with col_g1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        
        categorias = ['Vivienda', 'Transporte', 'Alimentación', 'Ocio & Bienestar', 'Educación & Salud']
        montos_cat = [total_vivienda, total_transporte, total_alimentacion, total_entretenimiento, total_otros]
        ideal_pct = [30, 15, 15, 10, 10]
        colors_cat = ['#4A90E2', '#F5C842', '#10D9A0', '#9B59B6', '#F56565']
        
        detalles = {
            'Vivienda': {'Alquiler': alquiler, 'Servicios': servicios, 'Internet': internet, 'Mantenimiento': mantenimiento},
            'Transporte': {'Trans. Público': transporte_pub, 'Gasolina': gasolina, 'Mant. Auto': mantenimiento_auto, 'Estacionamiento': estacionamiento},
            'Alimentación': {'Supermercado': supermercado, 'Restaurantes': restaurantes, 'Delivery': delivery, 'Cafés': cafes},
            'Ocio & Bienestar': {'Streaming': streaming, 'Salidas': salidas, 'Deportes': deportes, 'Hobbies': hobbies},
            'Educación & Salud': {'Educación': educacion, 'Salud': salud, 'Suscripciones': suscripciones, 'Otros': otros},
        }
        
        for cat, monto, ideal, color in zip(categorias, montos_cat, ideal_pct, colors_cat):
            pct_real = monto / ingreso_total * 100 if ingreso_total > 0 else 0
            estado = "✅" if pct_real <= ideal else "⚠️"
            
            with st.expander(f"{estado}  {cat}  —  {format_currency(monto)}  ({pct_real:.1f}%)", expanded=False):
                for sub, val in detalles[cat].items():
                    sub_pct = val / monto * 100 if monto > 0 else 0
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; padding:6px 0; 
                                border-bottom:1px solid rgba(255,255,255,0.04);">
                        <span style="font-size:13px; color:#8896B3;">{sub}</span>
                        <div style="text-align:right;">
                            <span style="font-family:'Space Mono',monospace; font-size:13px; color:#F0F4FF;">{format_currency(val)}</span>
                            <span style="font-size:11px; color:#4A5568; margin-left:8px;">{sub_pct:.0f}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Gastos extra
        if st.session_state.gastos_extra:
            st.markdown('<div style="font-size:13px; font-weight:600; color:#F5C842; margin-top:16px;">📌 Gastos Extraordinarios</div>', unsafe_allow_html=True)
            for idx, ge in enumerate(st.session_state.gastos_extra):
                c1, c2 = st.columns([4,1])
                with c1:
                    st.markdown(f'<div style="font-size:13px; color:#8896B3; padding:4px 0;">{ge["nombre"]}: <span style="color:#F0F4FF; font-family:\'Space Mono\',monospace">{format_currency(ge["monto"])}</span></div>', unsafe_allow_html=True)
                with c2:
                    if st.button("✕", key=f"del_ge_{idx}"):
                        st.session_state.gastos_extra.pop(idx)
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_g2:
        # Regla 50/30/20
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:15px; font-weight:600; color:#F0F4FF; margin-bottom:6px;">⚖️ Regla 50/30/20</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px; color:#4A5568; margin-bottom:16px;">Distribución ideal de tu ingreso</div>', unsafe_allow_html=True)
        
        necesidades = total_vivienda + total_transporte + total_alimentacion
        deseos = total_entretenimiento
        ahorro_real = max(saldo, 0)
        
        items_5030 = [
            ("Necesidades", necesidades, 50, "#4A90E2"),
            ("Deseos", deseos, 30, "#9B59B6"),
            ("Ahorro/Deuda", ahorro_real, 20, "#10D9A0"),
        ]
        
        for label, monto_item, ideal_item, color_item in items_5030:
            pct_actual = monto_item / ingreso_total * 100 if ingreso_total > 0 else 0
            diferencia = pct_actual - ideal_item
            status = "✅" if abs(diferencia) <= 5 else ("🟡" if abs(diferencia) <= 15 else "🔴")
            
            st.markdown(f"""
            <div style="margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="font-size:13px; color:#8896B3;">{status} {label}</span>
                    <span style="font-size:12px; color:#4A5568;">Actual {pct_actual:.0f}% / Ideal {ideal_item}%</span>
                </div>
                <div style="background:rgba(255,255,255,0.06); border-radius:10px; height:8px; overflow:hidden; position:relative;">
                    <div style="width:{min(pct_actual, 100)}%; height:100%; background:{color_item}; border-radius:10px; transition: width 0.5s;"></div>
                    <div style="position:absolute; top:0; left:{ideal_item}%; height:100%; width:2px; background:rgba(255,255,255,0.3);"></div>
                </div>
                <div style="text-align:right; font-family:'Space Mono',monospace; font-size:12px; color:{color_item}; margin-top:3px;">{format_currency(monto_item)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Radar comparativo
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:15px; font-weight:600; color:#F0F4FF; margin-bottom:12px;">🎯 vs Benchmark</div>', unsafe_allow_html=True)
        
        radar_cats = ['Vivienda', 'Transporte', 'Alimentación', 'Ocio', 'Ahorro']
        radar_vals = [
            total_vivienda/ingreso_total*100 if ingreso_total > 0 else 0,
            total_transporte/ingreso_total*100 if ingreso_total > 0 else 0,
            total_alimentacion/ingreso_total*100 if ingreso_total > 0 else 0,
            total_entretenimiento/ingreso_total*100 if ingreso_total > 0 else 0,
            tasa_ahorro
        ]
        radar_ideal = [30, 15, 15, 10, 30]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_vals + [radar_vals[0]], theta=radar_cats + [radar_cats[0]],
            fill='toself', name='Tu situación',
            line=dict(color='#F5C842', width=2),
            fillcolor='rgba(245,200,66,0.1)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_ideal + [radar_ideal[0]], theta=radar_cats + [radar_cats[0]],
            fill='toself', name='Ideal',
            line=dict(color='#10D9A0', width=2, dash='dash'),
            fillcolor='rgba(16,217,160,0.05)'
        ))
        
        fig_radar = plotly_dark_layout(fig_radar, 280)
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 45], gridcolor='rgba(255,255,255,0.05)',
                               tickfont=dict(color='#4A5568', size=10)),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#8896B3'))
            )
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PROYECCIONES
# ============================================================
elif selected == "Proyecciones":
    st.markdown('<div class="section-title">📈 Proyecciones Financieras</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Simula tu futuro financiero con distintos escenarios</div>', unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns([2,3])
    
    with col_p1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:15px; font-weight:600; color:#F0F4FF; margin-bottom:16px;">⚙️ Parámetros</div>', unsafe_allow_html=True)
        
        edad_actual = st.number_input("Edad actual", min_value=18, max_value=80, value=30)
        edad_jubilacion = st.number_input("Edad de jubilación", min_value=edad_actual+1, max_value=100, value=65)
        meta_patrimonio = st.number_input("Meta de patrimonio (S/)", min_value=0.0, value=500000.0, step=10000.0)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        tasa_crecimiento = st.slider("Rendimiento anual (%)", 0.0, 20.0, 8.0) / 100
        tasa_inflacion = st.slider("Inflación anual (%)", 0.0, 10.0, 3.0) / 100
        incremento_ahorro = st.slider("Incremento anual del ahorro (%)", 0.0, 20.0, 5.0) / 100
        
        escenario = st.selectbox("Escenario", ["Base", "Optimista", "Conservador"])
        
        if escenario == "Optimista":
            tasa_crecimiento *= 1.3
        elif escenario == "Conservador":
            tasa_crecimiento *= 0.7
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_p2:
        años_total = edad_jubilacion - edad_actual
        patrimonios = [patrimonio_total]
        ingresos_pasivos_proj = [ingresos_pasivos_total]
        ahorro_anual = ahorro_mensual * 12
        
        for año in range(años_total):
            ahorro_anual_adj = ahorro_anual * (1 + incremento_ahorro) ** año
            nuevo_patrim = (patrimonios[-1] + ahorro_anual_adj) * (1 + tasa_crecimiento)
            patrimonios.append(nuevo_patrim)
            ingresos_pasivos_proj.append(nuevo_patrim * 0.04 / 12)  # Regla del 4% mensual
        
        edades = list(range(edad_actual, edad_jubilacion + 1))
        
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        
        fig_proj = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_proj.add_trace(go.Scatter(
            x=edades, y=patrimonios, name="Patrimonio",
            line=dict(color='#F5C842', width=3),
            fill='tozeroy', fillcolor='rgba(245,200,66,0.05)'
        ), secondary_y=False)
        
        fig_proj.add_trace(go.Scatter(
            x=edades, y=ingresos_pasivos_proj, name="Ingreso Pasivo/mes",
            line=dict(color='#10D9A0', width=2.5, dash='dot')
        ), secondary_y=True)
        
        # Línea de meta
        fig_proj.add_hline(y=meta_patrimonio, line_dash="dash", line_color="#F56565",
                          annotation_text=f"Meta: {format_currency_short(meta_patrimonio)}",
                          annotation_font_color="#F56565")
        
        fig_proj = plotly_dark_layout(fig_proj, 380)
        fig_proj.update_xaxes(title_text="Edad")
        fig_proj.update_yaxes(title_text="Patrimonio (S/)", secondary_y=False, tickfont=dict(color='#8896B3'))
        fig_proj.update_yaxes(title_text="Ingreso Pasivo/mes (S/)", secondary_y=True, tickfont=dict(color='#10D9A0'))
        
        st.plotly_chart(fig_proj, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # KPIs de proyección
        c1, c2, c3 = st.columns(3)
        meta_alcanzada = next((i for i, p in enumerate(patrimonios) if p >= meta_patrimonio), None)
        
        with c1:
            st.markdown(f"""
            <div class="card-metric gold">
                <div class="metric-label" style="color:#8896B3;">Patrimonio a los {edad_jubilacion}</div>
                <div class="metric-value">{format_currency_short(patrimonios[-1])}</div>
                <div class="metric-sub">+{((patrimonios[-1]/patrimonio_total-1)*100):.0f}% de crecimiento</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="card-metric emerald">
                <div class="metric-label" style="color:#8896B3;">Ingreso Pasivo Mensual</div>
                <div class="metric-value">{format_currency_short(ingresos_pasivos_proj[-1])}</div>
                <div class="metric-sub">Al momento de jubilarte</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            if meta_alcanzada is not None:
                edad_meta = edad_actual + meta_alcanzada
                st.markdown(f"""
                <div class="card-metric blue">
                    <div class="metric-label" style="color:#8896B3;">Alcanzas la Meta a los</div>
                    <div class="metric-value">{edad_meta} años</div>
                    <div class="metric-sub">En {meta_alcanzada} años</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                cumplimiento = patrimonios[-1] / meta_patrimonio * 100
                st.markdown(f"""
                <div class="card-metric rose">
                    <div class="metric-label" style="color:#8896B3;">Cumplimiento de Meta</div>
                    <div class="metric-value">{cumplimiento:.0f}%</div>
                    <div class="metric-sub">Aumenta tu ahorro mensual</div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# METAS
# ============================================================
elif selected == "Metas":
    st.markdown('<div class="section-title">🏆 Mis Metas Financieras</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Define y monitorea tus objetivos financieros</div>', unsafe_allow_html=True)
    
    # Agregar nueva meta
    with st.expander("➕ Nueva Meta", expanded=False):
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1: m_nombre = st.text_input("Nombre de la meta", key="m_nombre")
        with mc2: m_meta = st.number_input("Monto objetivo (S/)", min_value=0.0, value=10000.0, step=1000.0, key="m_meta")
        with mc3: m_actual = st.number_input("Progreso actual (S/)", min_value=0.0, value=0.0, step=500.0, key="m_actual")
        with mc4: m_color = st.selectbox("Color", ["#F5C842", "#10D9A0", "#4A90E2", "#9B59B6", "#F56565"], key="m_color")
        
        if st.button("Agregar Meta", key="add_meta"):
            if m_nombre and m_meta > 0:
                st.session_state.metas_lista.append({
                    "nombre": m_nombre, "meta": m_meta, "actual": m_actual, "color": m_color
                })
                st.rerun()
    
    # Metas actuales
    cols_meta = st.columns(min(len(st.session_state.metas_lista), 3))
    
    for idx, meta in enumerate(st.session_state.metas_lista):
        col_idx = idx % 3
        with cols_meta[col_idx] if len(cols_meta) > 1 else st.container():
            progreso = min(meta["actual"] / meta["meta"] * 100, 100) if meta["meta"] > 0 else 0
            faltante = max(meta["meta"] - meta["actual"], 0)
            meses_falta = faltante / ahorro_mensual if ahorro_mensual > 0 else float('inf')
            
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid rgba(255,255,255,0.06);
                        border-top: 4px solid {meta['color']}; border-radius:16px; padding:20px; margin-bottom:16px;">
                <div style="font-size:14px; font-weight:600; color:#F0F4FF; margin-bottom:4px;">{meta['nombre']}</div>
                <div style="font-family:'Space Mono',monospace; font-size:22px; color:{meta['color']}; font-weight:700; margin-bottom:2px;">{progreso:.0f}%</div>
                <div style="font-size:12px; color:#4A5568; margin-bottom:12px;">{format_currency(meta['actual'])} de {format_currency(meta['meta'])}</div>
                <div style="background:rgba(255,255,255,0.06); border-radius:10px; height:8px; overflow:hidden; margin-bottom:10px;">
                    <div style="width:{progreso}%; height:100%; background:{meta['color']}; border-radius:10px;"></div>
                </div>
                <div style="font-size:12px; color:#4A5568;">
                    Faltan: <span style="color:#8896B3;">{format_currency(faltante)}</span>
                    {'· ~' + f'{meses_falta:.0f} meses' if meses_falta != float("inf") and meses_falta > 0 else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c_edit, c_del = st.columns(2)
            with c_edit:
                nuevo_actual = st.number_input("Actualizar", value=meta["actual"], step=500.0,
                                               key=f"meta_edit_{idx}", label_visibility="collapsed")
                if nuevo_actual != meta["actual"]:
                    st.session_state.metas_lista[idx]["actual"] = nuevo_actual
                    st.rerun()
            with c_del:
                if st.button("Eliminar", key=f"del_meta_{idx}"):
                    st.session_state.metas_lista.pop(idx)
                    st.rerun()
    
    # Gráfico de progreso conjunto
    if st.session_state.metas_lista:
        st.markdown('<div class="card-dark" style="margin-top:10px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:15px; font-weight:600; color:#F0F4FF; margin-bottom:16px;">📊 Progreso General de Metas</div>', unsafe_allow_html=True)
        
        nombres_m = [m["nombre"] for m in st.session_state.metas_lista]
        progresos_m = [min(m["actual"]/m["meta"]*100, 100) if m["meta"] > 0 else 0 for m in st.session_state.metas_lista]
        colores_m = [m["color"] for m in st.session_state.metas_lista]
        
        fig_metas = go.Figure(go.Bar(
            x=progresos_m, y=nombres_m, orientation='h',
            marker=dict(color=colores_m, line=dict(width=0)),
            text=[f"{p:.0f}%" for p in progresos_m], textposition='outside',
            textfont=dict(color='#8896B3', size=12)
        ))
        
        fig_metas = plotly_dark_layout(fig_metas, 250)
        fig_metas.update_xaxes(range=[0, 110])
        fig_metas.update_layout(showlegend=False)
        st.plotly_chart(fig_metas, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# CONSEJOS
# ============================================================
elif selected == "Consejos":
    st.markdown('<div class="section-title">💡 Consejos Personalizados</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Recomendaciones basadas en tu situación financiera actual</div>', unsafe_allow_html=True)
    
    # Consejos dinámicos
    consejos = []
    
    if tasa_ahorro < 10:
        consejos.append({"icon":"📉","color":"#F56565","nivel":"Urgente","titulo":"Mejora tu tasa de ahorro",
                        "desc":f"Solo estás ahorrando el {tasa_ahorro:.1f}% de tus ingresos. La meta es 20%. Identifica los 3 gastos que más puedes recortar.",
                        "accion":"Regla 50/30/20: necesidades/deseos/ahorro"})
    
    if total_vivienda > ingreso_total * 0.35:
        consejos.append({"icon":"🏠","color":"#F5C842","nivel":"Importante","titulo":"Gastos de vivienda elevados",
                        "desc":f"Destinas el {total_vivienda/ingreso_total*100:.1f}% a vivienda. El ideal es ≤30%. Considera refinanciar o buscar opciones más económicas.",
                        "accion":"Explora opciones de refinanciamiento"})
    
    if ahorro_actual < total_gastos * 3:
        meses_fondo = ahorro_actual/total_gastos if total_gastos > 0 else 0
        consejos.append({"icon":"🛡️","color":"#F5C842","nivel":"Importante","titulo":"Fondo de emergencia insuficiente",
                        "desc":f"Tienes fondo para {meses_fondo:.1f} meses. Necesitas al menos 6 meses ({format_currency(total_gastos*6)}) antes de invertir agresivamente.",
                        "accion":"Prioriza construir tu colchón financiero"})
    
    if inversiones < patrimonio_total * 0.3:
        consejos.append({"icon":"📈","color":"#4A90E2","nivel":"Oportunidad","titulo":"Aumenta tus inversiones",
                        "desc":f"Solo el {inversiones/patrimonio_total*100:.0f}% de tu patrimonio está invertido. Considera ETFs, fondos indexados o bienes raíces.",
                        "accion":"Diversifica con bajo riesgo primero"})
    
    if ingresos_pasivos_total < ingreso_total * 0.1:
        consejos.append({"icon":"💡","color":"#10D9A0","nivel":"Oportunidad","titulo":"Desarrolla ingresos pasivos",
                        "desc":f"Tus ingresos pasivos son el {ingresos_pasivos_total/ingreso_total*100:.1f}% del total. Busca crear fuentes que generen dinero mientras duermes.",
                        "accion":"Dividendos, alquileres, contenido digital"})
    
    if deudas > 0:
        consejos.append({"icon":"💳","color":"#9B59B6","nivel":"Acción","titulo":"Acelera el pago de deudas",
                        "desc":f"Tienes {format_currency(deudas)} en deudas. Usa el método avalancha (mayor interés primero) para liberarte antes.",
                        "accion":"Destina el 20% extra del ingreso a deudas"})
    
    if not consejos:
        st.markdown("""
        <div style="background:rgba(16,217,160,0.1); border:1px solid rgba(16,217,160,0.3); 
                    border-radius:16px; padding:30px; text-align:center;">
            <div style="font-size:40px; margin-bottom:10px;">🎉</div>
            <div style="font-size:20px; font-weight:600; color:#10D9A0; margin-bottom:8px;">¡Situación financiera excelente!</div>
            <div style="font-size:14px; color:#8896B3;">Tu gestión financiera es ejemplar. Considera estrategias avanzadas de inversión.</div>
        </div>
        """, unsafe_allow_html=True)
    
    for consejo in consejos:
        nivel_colors = {"Urgente": "#F56565", "Importante": "#F5C842", "Oportunidad": "#10D9A0", "Acción": "#9B59B6"}
        nc = nivel_colors.get(consejo["nivel"], "#8896B3")
        
        st.markdown(f"""
        <div style="background:var(--bg-card); border:1px solid rgba(255,255,255,0.06);
                    border-left: 4px solid {nc}; border-radius:16px; padding:20px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:24px;">{consejo['icon']}</span>
                    <div>
                        <span class="badge" style="background:rgba({','.join(str(int(nc.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.15); color:{nc}; margin-bottom:4px; display:inline-block;">
                            {consejo['nivel']}
                        </span>
                        <div style="font-size:15px; font-weight:600; color:#F0F4FF;">{consejo['titulo']}</div>
                    </div>
                </div>
            </div>
            <div style="font-size:13px; color:#8896B3; margin-bottom:10px; line-height:1.6;">{consejo['desc']}</div>
            <div style="background:rgba(255,255,255,0.04); border-radius:10px; padding:10px 14px;">
                <span style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; color:{nc};">→ </span>
                <span style="font-size:12px; color:#8896B3;">{consejo['accion']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Calculadora de interés compuesto
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-dark">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:16px; font-weight:600; color:#F0F4FF; margin-bottom:16px;">🧮 Calculadora de Interés Compuesto</div>', unsafe_allow_html=True)
    
    cc1, cc2, cc3, cc4 = st.columns(4)
    with cc1: monto_ini = st.number_input("Capital inicial (S/)", value=10000.0, step=1000.0)
    with cc2: aporte_m = st.number_input("Aporte mensual (S/)", value=500.0, step=100.0)
    with cc3: años_c = st.number_input("Años", min_value=1, max_value=50, value=10)
    with cc4: tasa_c = st.slider("Tasa anual (%)", 1.0, 20.0, 8.0) / 100
    
    meses_c = años_c * 12
    tasa_m = tasa_c / 12
    valores_c, sin_interes = [monto_ini], [monto_ini]
    mc = monto_ini
    mc_si = monto_ini
    
    for mes in range(meses_c):
        mc = (mc + aporte_m) * (1 + tasa_m)
        mc_si = mc_si + aporte_m
        if (mes + 1) % 12 == 0:
            valores_c.append(mc)
            sin_interes.append(mc_si)
    
    fig_comp = go.Figure()
    years_axis = list(range(años_c + 1))
    
    fig_comp.add_trace(go.Scatter(x=years_axis, y=valores_c, name='Con Interés Compuesto',
                                 line=dict(color='#F5C842', width=3),
                                 fill='tozeroy', fillcolor='rgba(245,200,66,0.05)'))
    fig_comp.add_trace(go.Scatter(x=years_axis, y=sin_interes, name='Solo Aportes',
                                 line=dict(color='#4A90E2', width=2, dash='dot'),
                                 fill='tozeroy', fillcolor='rgba(74,144,226,0.03)'))
    
    fig_comp = plotly_dark_layout(fig_comp, 300)
    fig_comp.update_xaxes(title_text="Años")
    fig_comp.update_yaxes(title_text="Monto (S/)")
    st.plotly_chart(fig_comp, use_container_width=True)
    
    ganancia = valores_c[-1] - sin_interes[-1]
    c_r1, c_r2, c_r3 = st.columns(3)
    with c_r1:
        st.markdown(f"""<div style="text-align:center; padding:16px; background:rgba(245,200,66,0.08); border-radius:12px; border:1px solid rgba(245,200,66,0.2);">
            <div style="font-size:11px; color:#8896B3; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">Valor Final</div>
            <div style="font-family:'Space Mono',monospace; font-size:20px; color:#F5C842; font-weight:700;">{format_currency(valores_c[-1])}</div>
        </div>""", unsafe_allow_html=True)
    with c_r2:
        st.markdown(f"""<div style="text-align:center; padding:16px; background:rgba(16,217,160,0.08); border-radius:12px; border:1px solid rgba(16,217,160,0.2);">
            <div style="font-size:11px; color:#8896B3; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">Ganancia por interés</div>
            <div style="font-family:'Space Mono',monospace; font-size:20px; color:#10D9A0; font-weight:700;">{format_currency(ganancia)}</div>
        </div>""", unsafe_allow_html=True)
    with c_r3:
        multiplicador = valores_c[-1] / monto_ini if monto_ini > 0 else 0
        st.markdown(f"""<div style="text-align:center; padding:16px; background:rgba(74,144,226,0.08); border-radius:12px; border:1px solid rgba(74,144,226,0.2);">
            <div style="font-size:11px; color:#8896B3; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">Multiplicador</div>
            <div style="font-family:'Space Mono',monospace; font-size:20px; color:#4A90E2; font-weight:700;">{multiplicador:.1f}x</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<div style="text-align:center; padding:30px; margin-top:40px; border-top:1px solid rgba(255,255,255,0.06);">
    <div style="font-family:'DM Serif Display',serif; font-size:18px; color:#F0F4FF; margin-bottom:8px;">Planifica360</div>
    <div style="font-size:12px; color:#4A5568; margin-bottom:12px;">Finanzas Inteligentes · Control Total · Libertad Financiera</div>
    <div style="display:flex; justify-content:center; gap:30px; font-size:12px; color:#4A5568;">
        <span>🔒 Datos locales</span>
        <span>📊 Sin publicidad</span>
        <span>💎 v3.0.0</span>
    </div>
    <div style="font-size:11px; color:#2D3748; margin-top:12px;">
        Solo para fines informativos. Consulta con un asesor financiero certificado.
    </div>
</div>
""", unsafe_allow_html=True)