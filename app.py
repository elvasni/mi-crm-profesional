import streamlit as st
import sqlite3

st.set_page_config(page_title="CRM - Hoberg & Driesch", layout="wide")

# Conexión a la base de datos SQLite local en la nube
def init_db():
    conn = sqlite3.connect('crm_hoberg.db')
    c = conn.cursor()
    # Tabla de Familias de Materiales
    c.execute('''
        CREATE TABLE IF NOT EXISTS familias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_almacen TEXT,
            origen TEXT,
            descripcion TEXT,
            notas TEXT
        )
    ''')
    # Tabla de Clientes
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            provincia TEXT,
            comercial TEXT,
            estado TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

st.title("🚀 CRM Comercial - Hoberg & Driesch")
st.sidebar.title("Menú Principal")

menu = st.sidebar.selectbox("Ir a:", ["Dashboard", "Gestión de Clientes", "Familias de Materiales", "Buscador BOE y Licitaciones", "Agenda"])

if menu == "Dashboard":
    st.subheader("📊 Panel de Control General")
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes Totales", "0")
    col2.metric("Clientes Activos", "0")
    col3.metric("Oportunidades Nuevas", "0")
    st.info("💡 Tu CRM ya está preparado. Selecciona un apartado en el menú lateral para empezar a trabajar.")

elif menu == "Gestión de Clientes":
    st.subheader("👥 Ficha de Clientes y Obras")
    st.write("Próximamente: Alta, baja, modificación y programación de llamadas/visitas.")

elif menu == "Familias de Materiales":
    st.subheader("📦 Familias de Materiales (Tarifas y Orígenes)")
    st.write("Aquí cargaremos las familias de tubos, soldaduras y aceros de tus catálogos.")

elif menu == "Buscador BOE y Licitaciones":
    st.subheader("🔍 Novedades BOE y Plataforma de Contratación")
    st.write("Aquí integraremos el buscador por palabras clave y códigos CPV.")

elif menu == "Agenda":
    st.subheader("📅 Agenda de Acciones Comerciales")
    st.write("Control de visitas y llamadas a 2 semanas vista.")
