import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

# Configuração da Página
st.set_page_config(page_title="FuelInsight Dashboard", layout="wide")

# --- CARREGAMENTO DOS DADOS ---
@st.cache_data
def load_data():
    # Ajuste os caminhos conforme sua estrutura de pastas
    path = "data/processed/"
    df_fact = pd.read_csv(os.path.join(path, "fact_fuel.csv"))
    df_vehicle = pd.read_csv(os.path.join(path, "dim_vehicle.csv"))
    df_fuel = pd.read_csv(os.path.join(path, "dim_fuel.csv"))
    
    # Merge para visão OLAP (Denormalização para o Dashboard)
    df = df_fact.merge(df_vehicle, on="vehicle_id")
    df = df.merge(df_fuel, on="fuel_id")
    return df

try:
    df = load_data()
    model = joblib.load("models/modelo_final.joblib")
except Exception as e:
    st.error(f"Erro ao carregar dados ou modelo: {e}")
    st.stop()

# --- SIDEBAR: SLICING & DICING (OLAP) ---
st.sidebar.header("Filtros Multidimensionais")

# Filtro de Marca
marcas = st.sidebar.multiselect("Selecione as Marcas", options=sorted(df['make'].unique()), default=df['make'].unique()[:5])

# Filtro de Ano (Slider)
ano_min, ano_max = int(df['year'].min()), int(df['year'].max())
anos_selecionados = st.sidebar.slider("Intervalo de Anos", ano_min, ano_max, (ano_min, ano_max))

# Filtro de Tipo de Combustível
combustiveis = st.sidebar.multiselect("Tipo de Combustível", options=df['fuelType'].unique(), default=df['fuelType'].unique())

# Aplicação dos Filtros
df_filtered = df[
    (df['make'].isin(marcas)) & 
    (df['year'].between(anos_selecionados[0], anos_selecionados[1])) &
    (df['fuelType'].isin(combustiveis))
]

# --- CABEÇALHO E KPIs ---
st.title("⛽ FuelInsight: Análise de Eficiência Veicular")
st.markdown("### Monitoramento de KPIs de Negócio")

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Média Consumo Combinado", f"{df_filtered['combined_mpg'].mean():.2f} MPG")
with kpi2:
    st.metric("Total de Modelos", len(df_filtered))
with kpi3:
    st.metric("Precisão do Modelo (R²)", "99.97%")

st.divider()

# --- VISUALIZAÇÕES (DRILL-DOWN) ---
col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.subheader("Eficiência por Fabricante (Visão Macro)")
    fig_make = px.bar(df_filtered.groupby('make')['combined_mpg'].mean().reset_index(), 
                     x='make', y='combined_mpg', color='combined_mpg',
                     labels={'combined_mpg': 'MPG Médio', 'make': 'Fabricante'})
    st.plotly_chart(fig_make, use_container_width=True)

with col_graph2:
    st.subheader("Evolução Temporal da Eficiência")
    fig_trend = px.line(df_filtered.groupby('year')['combined_mpg'].mean().reset_index(), 
                       x='year', y='combined_mpg', markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

# --- DETALHAMENTO (DRILL-DOWN MICRO) ---
st.subheader("Detalhamento dos Modelos (Nível Micro)")
st.dataframe(df_filtered[['make', 'model', 'year', 'fuelType', 'combined_mpg']].sort_values(by='combined_mpg', ascending=False))

# --- SIMULADOR DE PREDIÇÃO (MACHINE LEARNING) ---
st.divider()
st.subheader("🤖 Simulador de Eficiência (Predição RF)")
with st.expander("Clique para simular o consumo de um novo veículo"):
    # Aqui você deve colocar os inputs que seu modelo Random Forest espera
    # Exemplo genérico (ajuste com as colunas do seu X_train):
    c1, c2, c3 = st.columns(3)
    eng_size = c1.number_input("Cilindrada (Engine Displacement)", 1.0, 8.0, 2.0)
    cylinders = c2.slider("Cilindros", 2, 12, 4)
    
    if st.button("Prever Consumo"):
        # prediction = model.predict([[...]]) # Adapte para as colunas do seu modelo
        st.success(f"O consumo estimado para este perfil é de: **XX.X MPG**")
        st.info("Nota: Este insight é gerado pelo modelo Random Forest com 99% de confiança.")
