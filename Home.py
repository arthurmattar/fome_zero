import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home')

st.header('Dashboard Fome Zero')
st.sidebar.markdown('## Best restaurants in the world')
st.sidebar.markdown('---')

# image = Image.open('logo.jpg')
# st.sidebar.image(image,width=120)

st.write('Fome Zero Growth Dashboard')

st.markdown(
    """
    ### Visões disponíveis:
        - Visão Geral
        - Visão Países
            * Geral
            * Restaurantes
            * Avaliações
        - Visão Cidades
        - Visão Restaurantes
        - Visão Tipos de Culinária
""" )
