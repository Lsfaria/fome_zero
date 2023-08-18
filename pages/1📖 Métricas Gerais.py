# libraries

import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from PIL import Image

st.set_page_config( page_title='Overview', page_icon='📖', layout='wide' )

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America"
    }

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

exchange_rates = {
    'Botswana Pula(P)': 12.85,
    'Brazilian Real(R$)': 5.31,
    'Dollar($)': 1,
    'Emirati Diram(AED)': 3.67,
    'Indian Rupees(Rs.)': 82.68,
    'Indonesian Rupiah(IDR)': 15608.45,
    'NewZealand($)': 1.57,
    'Pounds(£)': 0.819257,
    'Qatari Rial(QR)': 3.64,
    'Rand(R)': 17.59,
    'Sri Lankan Rupee(LKR)': 366.86,
    'Turkish Lira(TL)': 18.65,
  }
# -------------------------
# Funções
# -------------------------

def rename_columns(dataframe):
    '''Esta função tem a responsabilidade de renomear as colunas do dataframe
    
        Tipos:

        1. Formata o nome das colunas para o padrão snake case
        2. Remoção dos espaços das variáveis de texto

    Input: Dataframe
    Output: Dataframe
    '''
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def country_name(country_id): 
    '''Esta função tem a responsabilidade de adicionar uma coluna no dataframe com o nome dos Países de acordo com o dicionário COUNTRIES.

    Input: Dataframe
    Output: Dataframe
    '''
    
    return COUNTRIES[country_id]

def create_price_tye(price_range):
    '''Esta função tem a responsabilidade de adicionar uma coluna com o a classificação dos preços no dataframe. 

    Input: Dataframe
    Output: Dataframe
    '''
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


def color_name(color_code):
    '''Esta função tem a responsabilidade de adicionar uma coluna com o nome das cores no dataframe  de acordo com o dicionário COLORS.

    Input: Dataframe
    Output: Dataframe
    '''
    return COLORS[color_code]

def convert_currency(df1):
    '''Converte a moeda para USD.
    

    Input: Dataframe
    Retorna:Dataframe
    '''
    df1['price_in_dollar'] =  df1.apply(lambda x: x['average_cost_for_two'] / exchange_rates.get(x['currency'], 1), axis=1)
    
    return df1

def clean_code( df1 ):
    '''Esta função tem a responsabilidade de limpar o dataframe
    
        Tipos de limpeza:
        1. Colunas renomeadas
        2. Cria colunas para novos Insights
        3. Retira colunas com todos os valores iguais
        4. Remove as linhas duplicadas
        5. Remoção dos dados Nan
    
    Input: Dataframe
    Output: Dataframe
    '''
    # Renomeando as colunas
    df1 = rename_columns(df)

    #Substitui os códigos de países pelos nomes respectivos
    df1["country"] = df1.loc[:, "country_code"].apply(lambda x: country_name(x))

    #Define categorias de preço de acordo com o range
    df1["price_tye"] = df1.loc[:, "price_range"].apply(lambda x: create_price_tye(x))

    #Define o padrão de cores das avaliações
    df1["name_color"] = df1.loc[:, "rating_color"].apply(lambda x: color_name(x))

    ## Excluindo valores ausentes (NaN) da coluna cuisines
    df1.dropna(subset =['cuisines'], inplace = True)

    #Definindo os restaurantes por apenas um tipo de culinária
    df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

    #Removendo a coluna 'Switch to order menu', pois todos os valores eram iguais.
    df1 = df1.drop(columns = ['switch_to_order_menu'], axis = 1)

    #Removendo linhas duplicadas
    df1 = df1.drop_duplicates().reset_index(drop= True)

    #Unifica os valores do prato na moeda Dólar
    df1 = convert_currency(df1)

    #Removendo um outlier
    df1 = df1.drop(df1[(df1['average_cost_for_two'] == 25000017)].index)
    
    return df1

def convert_df(df):
  
    return df.to_csv(index=False, sep=';')

# --------------------------- Inicio da Estrutura lógica do código --------------------------

# ------------------------
# Import dataset
# ------------------------

df = pd.read_csv ('zomato.csv')

# ------------------------
# Limpando os dados
# ------------------------

df1 = clean_code(df)

# ==========================================================================
# Barra lateral
# ==========================================================================

st.sidebar.markdown( ' # Filtros' )

lista_paises = list(df1['country'].unique())

country_options = st.sidebar.multiselect( 'Escolha os Paises que Deseja visualizar as Informações', lista_paises, default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])


# Filtro de países
linhas_selecionadas = df1['country'].isin( country_options )
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown( ' # Dados Tratados' )

clean_code = clean_code(df)
csv = convert_df( clean_code )
st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='data.csv')

# ==========================================================================
# Layout no Streamlit
# ==========================================================================

with st.container():
        st.title ('📈 Métricas Gerais')
        col1, col2, col3, col4, col5 = st.columns( 5 )


        with col1:
            rest_quant = len(df1['restaurant_id'].unique())
            col1.metric( 'Restaurantes Cadastrados', rest_quant )

        with col2:
            pais_quant = df1['country'].nunique()
            col2.metric( 'Países Cadastrados', pais_quant )

        with col3:
            city_quant = df1['city'].nunique()
            col3.metric( 'Cidades Cadastradas', city_quant )

        with col4:
            aval_total = df1['votes'].sum()
            col4.metric( 'Avaliações Feitas na Plataforma', city_quant )

        with col5:
            cuisines_total = df1['cuisines'].nunique()
            col5.metric( 'Tipos de Culinárias Oferecidas', cuisines_total )
    
with st.container():

    df_aux = df1.loc[:, ['restaurant_name', 'latitude', 'longitude', 'name_color','cuisines',                       'aggregate_rating','average_cost_for_two','currency']]

    
    fig = folium.Figure(width=1024, height=720)
    
    m = folium.Map(max_bounds=True).add_to(fig)
    
    # 'MarkerCluster()' cria um objeto que agrupará os
# os marcadores dependendo do zoom aplicado ao mapa. No comando
# abaixo estamos criando um objeto do tipo 'MarkerCluster'
# (instanciando a classe) e o adicionando ao mapa 
marker_cluster = MarkerCluster().add_to(m)

for index, line in df_aux.iterrows():

    name = line["restaurant_name"]
    price_for_two = line["average_cost_for_two"]
    cuisine = line["cuisines"]
    currency = line["currency"]
    rating = line["aggregate_rating"]
    color = line["name_color"]

    html = "<p><strong>{}</strong></p>"
    html += "<p>Price: {},00 para dois"
    html += "<br />Type: {}"
    html += "<br />Aggregate Rating: {}/5.0"
    html = html.format(name, price_for_two, cuisine, rating)

    popup = folium.Popup(
        folium.Html(html, script=True),
        max_width=500,
    )

    folium.Marker(
        [line["latitude"], line["longitude"]],
        popup=popup,
        icon=folium.Icon(color=color, icon="home", prefix="fa")).add_to(marker_cluster)


folium_static( m , width=1024 , height=600 )
