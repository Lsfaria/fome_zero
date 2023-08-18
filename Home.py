import streamlit as st
from PIL import Image


st.set_page_config(page_title='Home', page_icon="🎲")

image_path = 'fome_zero.PNG'
image = Image.open( image_path )
st.sidebar.image( image, width=240 )

st.sidebar.markdown( ' ## World Gastronomic Best Experiences' )
st.sidebar.markdown("""___""")
st.sidebar.markdown('###### Data Scientist: Leonardo Faria ')


# ==========================================================================
# Layout no Streamlit
# ==========================================================================

st.title('O melhor lugar para encontrar seu mais novo restaurante favorito!')

st.title('Fome Zero Growth Dashboard')
st.markdown(
    ''' 
    Fome Zero Dashboard foi construido para ajudar o time de négocio a tomar melhores decisões baseados nos dados mais relevantes encontrados na análise exploratória dos dados.

    ### Como utilizar esse Growth Dashboard?
    - Visão Estratégica :   
        - Número de Restaurantes cadastrados.
        - Número de Paises cadastrados
        - Número de Cidades cadastrados.
        - Total de Avaliações Feitas na plataforma
        - Tipos de Culinária cadastrados
        - Visão Geográfica: Insights de geolocalização.
    - Métrica Países:
        - Quantidade de Restaurantes Registrados por País
        - Quantidade de Cidades Registradas por País
        - Classificação de preços por País
        - Média de Avaliações feitas por País
        - Média de Preço para um Prato para 2 Pessoas
    - Métrica Cidades:
        - Top 10 Cidades com mais Restaurantes na Base de Dados
        - Top 7 Cidades dos Restaurantes com avaliações médias superiores a 4
        - Top 7 Cidades dos Restaurantes com avaliações médias inferiores a 2.5
        - Top 10 Cidades que possuem maior variação de culinárias

    - Métrica Gastronomia
        - Visão Restaurantes
            - Seleção dos melhores Restaurantes dos principais tipos Culinários
            - Seleção dos restaurantes mais bem avaliados
            - Análise da quantidade de avaliações quando o restaurante possui delivery
            - Análise do custo médio de acordo com os restaurante que possuem reserva
        - Visão Culinárias
            - Seleção das Culinárias Mais Caras
            - Seleção das melhores avaliações médias de cada Culinária
            - Seleção das piores avaliações médias de cada Culinária

    ''')