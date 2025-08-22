import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página y tema Spotify
st.set_page_config(
    page_title="Spotify Data Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados para feeling Spotify
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1db954 0%, #191414 100%);
        color: #fff;
    }
    .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2 {
        background-color: #191414 !important;
        color: #fff !important;
    }
    .stButton>button {
        background-color: #1db954 !important;
        color: #fff !important;
        border-radius: 20px;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-color: #1db954;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 style='color:#1db954;font-size:3em;'>🎧 Spotify Music Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#fff;'>KPIs y análisis musical interactivo</h3>", unsafe_allow_html=True)

# Cargar datos
data_path = 'data.csv'
df = pd.read_csv(data_path)

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Promedio Danceability", f"{df['danceability'].mean():.2f}")
col2.metric("Promedio Energy", f"{df['energy'].mean():.2f}")
col3.metric("Promedio Valence", f"{df['valence'].mean():.2f}")
col4.metric("% Canciones Liked", f"{df['liked'].mean()*100:.1f}%")

st.markdown("---")

# Gráficos principales
st.subheader("Distribución de Valence")
fig_valence, ax_valence = plt.subplots()
sns.histplot(df['valence'], bins=20, kde=True, color="#1db954", ax=ax_valence)
ax_valence.set_title('Distribución de Valence', color="#1db954")
ax_valence.set_xlabel('Valence')
ax_valence.set_ylabel('Cantidad de canciones')
st.pyplot(fig_valence)

st.subheader("Danceability según si la canción fue 'liked'")
fig_dance, ax_dance = plt.subplots()
sns.boxplot(x='liked', y='danceability', data=df, palette=["#191414", "#1db954"], ax=ax_dance)
ax_dance.set_title('Danceability por Liked', color="#1db954")
st.pyplot(fig_dance)

st.subheader("Energy según si la canción fue 'liked'")
fig_energy, ax_energy = plt.subplots()
sns.boxplot(x='liked', y='energy', data=df, palette=["#191414", "#1db954"], ax=ax_energy)
ax_energy.set_title('Energy por Liked', color="#1db954")
st.pyplot(fig_energy)

st.subheader("Matriz de correlación entre variables")
fig_corr, ax_corr = plt.subplots(figsize=(10,8))
sns.heatmap(df.corr(), annot=True, cmap='Greens', ax=ax_corr)
ax_corr.set_title('Correlación entre variables', color="#1db954")
st.pyplot(fig_corr)

# Sidebar para filtros
st.sidebar.header("🎚️ Filtros musicales")
dance_range = st.sidebar.slider('Danceability', float(df['danceability'].min()), float(df['danceability'].max()), (float(df['danceability'].min()), float(df['danceability'].max())))
energy_range = st.sidebar.slider('Energy', float(df['energy'].min()), float(df['energy'].max()), (float(df['energy'].min()), float(df['energy'].max())))
liked_filter = st.sidebar.selectbox('Liked', options=['Todos', 'Sí', 'No'])

filtered_df = df[(df['danceability'] >= dance_range[0]) & (df['danceability'] <= dance_range[1]) &
                 (df['energy'] >= energy_range[0]) & (df['energy'] <= energy_range[1])]
if liked_filter == 'Sí':
    filtered_df = filtered_df[filtered_df['liked'] == 1]
elif liked_filter == 'No':
    filtered_df = filtered_df[filtered_df['liked'] == 0]

st.markdown("---")
st.subheader("🎵 Canciones filtradas")
st.dataframe(filtered_df.head(20), use_container_width=True)

st.markdown("<small style='color:#fff;'>Dashboard inspirado en Spotify. Hecho con Streamlit.</small>", unsafe_allow_html=True)
