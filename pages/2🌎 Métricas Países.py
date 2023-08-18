# libraries

import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image


st.set_page_config( page_title='Countries', page_icon='🌎', layout='wide' )

# -------------------------
#Dicionários
# -------------------------

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


def rest_country(df1):
    '''Esta função faz a distribuição da quantidade de restaurantes de acordo com o País e devolve um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[:, ['restaurant_id', 'country' ]]
                 .groupby(['country'])
                 .nunique()
                 .sort_values('restaurant_id', ascending = False)
                 .reset_index())
    # gráfico
    fig = px.bar (df_aux,
                  x='country',
                  y='restaurant_id',
                  text_auto = True,
                  labels = {'country': 'Países', 'restaurant_id': 'Quantidade de Restaurantes'})
    
    return fig

def city_country(df1):
    '''Esta função faz a distribuição das quantidade de cidades de acordo com o País e devolve um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[:, ['city', 'country' ]]
                 .groupby(['country'])
                 .nunique()
                 .sort_values('city', ascending = False)
                 .reset_index())
    # gráfico
    fig = px.bar (df_aux, x='country',
                  y='city',
                  text_auto = True,
                  labels = {'country': 'Países', 'city': 'Quantidade de Cidades'})
    
    return fig

def price_country(df1):
    '''Esta função faz uma classificação em % de acordo com a faixa de preços por País e devolve um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[:, ['price_tye', 'country','restaurant_id' ]]
                 .groupby(['country','price_tye'])
                 .count()
                 .sort_values(['country', 'restaurant_id'], ascending = [True, False])
                 .reset_index())
    
    df_aux2 = (df_aux.groupby('country')
                     .sum()
                     .reset_index())
    
    # Junção dos dois dataframes
    df_merged = df_aux.merge(df_aux2, on="country")
    df_aux['percentage'] = round((df_merged['restaurant_id_x'] / df_merged['restaurant_id_y'])*100, 0)
    
    # gráfico
    fig = px.bar (df_aux, 
                  x='country', 
                  y='restaurant_id',
                  color='price_tye', 
                  labels = {'country': 'Países', 'restaurant_id': 'Quantidade de Restaurantes'}, 
                  text='percentage', 
                  category_orders={'price_tye': ['cheap', 'normal', 'expensive', 'gourmet']})
               
    fig.update_traces(texttemplate='%{text}%', textposition='inside')
    
    return fig

def avg_country(df1):
    '''Esta função faz a distribuição das avaliações feitas de acordo com o País e devolve um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[:, ['votes', 'country' ]]
                 .groupby(['country'])
                 .mean()
                 .sort_values('votes', ascending = False)
                 .reset_index())
    # gráfico
    fig = px.bar (df_aux,
                  x='country', 
                  y='votes', 
                  labels = {'country': 'Países', 'votes': 'Quantidade de Avaliações'},
                  text_auto='.2f') 
    
    return fig


def avg_for2(df1):
    '''Esta função faz a distribuição do custo para um prato para dois de acordo com o País e devolve um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[:, ['price_in_dollar', 'country' ]]
                 .groupby(['country'])
                 .mean()
                 .sort_values('price_in_dollar', ascending = False)
                 .reset_index())
    # gráfico
    fig = px.bar (df_aux,
                  x='country', 
                  y='price_in_dollar', 
                  labels = {'country': 'Países', 'price_in_dollar': 'Preço de Prato para 2 Pessoas'},
                  text_auto='.2f') 
    
    return fig

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


# ==========================================================================
# Layout no Streamlit
# ==========================================================================


st.title('🌎 Métricas Países')

with st.container():
    col1, col2 = st.columns( 2 )
    
    with col1:
        st.markdown('#### Quantidade de Restaurantes Registrados por País')
        fig = rest_country (df1)
        st.plotly_chart( fig, use_container_width = True )
        
    with col2:
        st.markdown('#### Quantidade de Cidades Registradas por País')
        fig = city_country (df1) 
        st.plotly_chart( fig, use_container_width = True )
        
    
with st.container():
    
    st.markdown('#### Classificação de preços por País')
    fig = price_country (df1)                     
    st.plotly_chart( fig, use_container_width = True )
    
    
with st.container():
    col1, col2 = st.columns( 2 )
    
    with col1:
        st.markdown('##### Média de Avaliações feitas por País')
        fig = avg_country (df1)
        st.plotly_chart( fig, use_container_width = True )
        
        
    with col2:
        st.markdown('##### Média de Preço para um Prato para 2 Pessoas (U.S. Dollar)')
        fig = avg_for2 (df1)
        st.plotly_chart( fig, use_container_width = True )


