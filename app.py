import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="CRM - Hoberg & Driesch", layout="wide")

def init_db():
    conn = sqlite3.connect('crm_hoberg.db')
    c = conn.cursor()
    
    # Tabla Familias (se mantiene)
    c.execute('DROP TABLE IF EXISTS familias')
    c.execute('''CREATE TABLE familias (id INTEGER PRIMARY KEY AUTOINCREMENT, codigo_almacen TEXT, grupo_sap TEXT, origen TEXT, descripcion TEXT, observaciones TEXT)''')
    
    # Tabla Clientes (Nueva)
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    provincia TEXT,
                    estado TEXT
                )''')
    
    # Datos iniciales familias
    familias_iniciales = [("1110", "DUS", "Dusseldorf", "B.P + Tubo caldera", "Almacén origen"),
                          ("1810", "DUIS", "Duisburg", "TE Frio + Tubo red. SOLDADO", "Almacén origen")]
    c.executemany("INSERT INTO familias (codigo_almacen, grupo_sap, origen, descripcion, observaciones) VALUES (?, ?, ?, ?, ?)", familias_iniciales)
    conn.commit()
    conn.close()

# Inicializamos solo la primera vez si es necesario
try:
    conn = sqlite3.connect('crm_hoberg.db')
    conn.execute("SELECT * FROM clientes")
    conn.close()
except:
    init_db()

st.title("🚀 CRM Comercial - Hoberg & Driesch")
menu = st.sidebar.selectbox("Ir a:", ["Dashboard", "Gestión de Clientes", "Familias de Materiales", "Buscador BOE", "Agenda"])

if menu == "Dashboard":
    st.subheader("📊 Panel de Control")
    st.info("CRM operativo en la nube.")

elif menu == "Gestión de Clientes":
    st.subheader("👥 Gestión de Clientes")
    
    # Formulario Alta
    with st.expander("➕ Añadir Nuevo Cliente"):
        with st.form("form_cliente"):
            nombre = st.text_input("Nombre de la Empresa / Obra")
            prov = st.text_input("Provincia")
            est = st.selectbox("Estado", ["Prospecto", "Activo", "Inactivo"])
            if st.form_submit_button("Registrar Cliente"):
                conn = sqlite3.connect('crm_hoberg.db')
                conn.execute("INSERT INTO clientes (nombre, provincia, estado) VALUES (?, ?, ?)", (nombre, prov, est))
                conn.commit()
                conn.close()
                st.success("Cliente guardado.")

    # Tabla Clientes
    conn = sqlite3.connect('crm_hoberg.db')
    df_c = pd.read_sql("SELECT * FROM clientes", conn)
    conn.close()
    st.dataframe(df_c, use_container_width=True)

elif menu == "Familias de Materiales":
    st.subheader("📦 Familias de Materiales")
    conn = sqlite3.connect('crm_hoberg.db')
    df_f = pd.read_sql("SELECT * FROM familias", conn)
    conn.close()
    st.dataframe(df_f, use_container_width=True)

elif menu == "Buscador BOE":
    st.write("Módulo en desarrollo.")
elif menu == "Agenda":
    st.write("Módulo en desarrollo.")
