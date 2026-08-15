import streamlit as st
import sqlite3

st.set_page_config(page_title="CRM Hoberg & Driesch", layout="wide")

st.title("🚀 CRM Profesional - Marc Ambite")
st.write("Bienvenido a tu panel comercial.")

# Conexión básica a base de datos
conn = sqlite3.connect('crm.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS clientes (nombre TEXT, empresa TEXT)')
conn.commit()

st.sidebar.title("Menú Principal")
opcion = st.sidebar.selectbox("Selecciona una sección", ["Dashboard", "Clientes", "Agenda"])

if opcion == "Dashboard":
    st.subheader("Tu panel de control")
    st.write("Aquí irán tus mapas y estadísticas.")
