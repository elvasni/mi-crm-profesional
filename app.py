import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="CRM - Hoberg & Driesch", layout="wide")

# Conexión a la base de datos e inicialización limpia de tablas
def init_db():
    conn = sqlite3.connect('crm_hoberg.db')
    c = conn.cursor()
    
    # Borramos la tabla antigua para evitar conflictos de columnas
    c.execute('DROP TABLE IF EXISTS familias')
    
    # Tabla de Familias de Materiales con la estructura correcta
    c.execute('''
        CREATE TABLE familias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_almacen TEXT,
            grupo_sap TEXT,
            origen TEXT,
            descripcion TEXT,
            observaciones TEXT
        )
    ''')
    
    # Insertar datos iniciales
    familias_iniciales = [
        ("1110", "DUS", "Dusseldorf", "B.P + Tubo caldera SIN SOLDADURA + Calibrados (BK) + Conducción Hidraúlica (NBK)", "Almacén origen"),
        ("1810", "DUIS", "Duisburg", "TE Frio + Tubo red. SOLDADO (Tarifa EN10219)", "Almacén origen"),
        ("1110", "DUS", "Dusseldorf **Schierle**", "H8 + H9 + tubos cromados + macizos cromados (Tarifa HIDRAULICA)", "Especial"),
        ("4210", "SPN", "Spain", "Directos de fabrica a cliente", "Nacional"),
    ]
    c.executemany("INSERT INTO familias (codigo_almacen, grupo_sap, origen, descripcion, observaciones) VALUES (?, ?, ?, ?, ?)", familias_iniciales)
    conn.commit()
    conn.close()

init_db()

st.title("🚀 CRM Comercial - Hoberg & Driesch")
st.sidebar.title("Menú Principal")

menu = st.sidebar.selectbox("Ir a:", ["Dashboard", "Gestión de Clientes", "Familias de Materiales", "Buscador BOE y Licitaciones", "Agenda"])

if menu == "Dashboard":
    st.subheader("📊 Panel de Control General")
    col1, col2, col3 = st.columns(3)
    
    conn = sqlite3.connect('crm_hoberg.db')
    total_familias = pd.read_sql("SELECT COUNT(*) as total FROM familias", conn).iloc[0]['total']
    conn.close()
    
    col1.metric("Familias de Material", str(total_familias))
    col2.metric("Clientes Activos", "0")
    col3.metric("Oportunidades Nuevas", "0")
    st.info("💡 Tu CRM está operativo en la nube.")

elif menu == "Gestión de Clientes":
    st.subheader("👥 Ficha de Clientes y Obras")
    st.write("Próximamente: Alta, baja, modificación y programación de llamadas/visitas.")

elif menu == "Familias de Materiales":
    st.subheader("📦 Familias de Materiales (Tarifas y Orígenes)")
    st.write("Consulta y gestión de los grupos de materiales y especificaciones de tubo.")
    
    conn = sqlite3.connect('crm_hoberg.db')
    df_familias = pd.read_sql("SELECT codigo_almacen AS 'Cód. Almacén', grupo_sap AS 'Grupo SAP', origen AS 'Origen / Proveedor', descripcion AS 'Descripción Material', observaciones AS 'Observaciones' FROM familias", conn)
    conn.close()
    
    st.dataframe(df_familias, use_container_width=True)
    
    with st.expander("➕ Añadir nueva familia de material"):
        with st.form("form_familia"):
            c_alm = st.text_input("Código Almacén (ej. 1110)")
            g_sap = st.text_input("Grupo SAP (ej. DUS)")
            origen = st.text_input("Origen / Proveedor")
            desc = st.text_input("Descripción del material")
            obs = st.text_input("Observaciones")
            btn_guardar = st.form_submit_button("Guardar Familia")
            
            if btn_guardar:
                conn = sqlite3.connect('crm_hoberg.db')
                c = conn.cursor()
                c.execute("INSERT INTO familias (codigo_almacen, grupo_sap, origen, descripcion, observaciones) VALUES (?, ?, ?, ?, ?)", (c_alm, g_sap, origen, desc, obs))
                conn.commit()
                conn.close()
                st.success("¡Familia añadida correctamente!")

elif menu == "Buscador BOE y Licitaciones":
    st.subheader("🔍 Novedades BOE y Plataforma de Contratación")
    st.write("Aquí integraremos el buscador por palabras clave y códigos CPV.")

elif menu == "Agenda":
    st.subheader("📅 Agenda de Acciones Comerciales")
    st.write("Control de visitas y llamadas a 2 semanas vista.")
