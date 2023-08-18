# libraries

import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config( page_title='Cities', page_icon='🏙️', layout='wide' )


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


def top_rest(df1):
    '''Esta função faz o top 10 das cidades com maior numero de restaurantes e devolve um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[:, ['city', 'restaurant_id','country']]
                 .groupby(['city', 'country'])
                 .nunique()
                 .sort_values(['restaurant_id','city'], ascending = [False, True])
                 .reset_index())
    # gráfico
    fig = px.bar( df_aux.head(10),
           x='city',
           y='restaurant_id',
           color = 'country',
           labels = {'restaurant_id': ' Quantidade de Restaurantes',
                    'city': 'Cidade',
                    'country': 'Países'},
           text_auto=True,
           color_discrete_sequence = px.colors.qualitative.Plotly)
    
    return fig


def avg_4(df1):
    '''Esta função faz o top 7 das cidades com avaliação maior ou igual a 4 e devolve um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[df1['aggregate_rating'] >= 4, ['city', 'restaurant_id','country']]
                 .groupby(['city','country'])
                 .count()
                 .sort_values(['restaurant_id','city'], ascending = [False, True])
                 .reset_index())

    # gráfico
    fig = px.bar( df_aux.head(7),
           x='city',
           y='restaurant_id',
           color = 'country',
           labels = {'restaurant_id': ' Quantidade de Restaurantes',
                    'city': 'Cidade',
                    'country': 'País'},
           text_auto=True,
           color_discrete_sequence = px.colors.qualitative.Plotly)

    return fig

def avg_2(df1):
    '''Esta função faz o top 7 das cidades com avaliação menor ou igual a 2.5 e devolve um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[df1['aggregate_rating'] <= 2.5, ['city', 'restaurant_id', 'country']]
                 .groupby(['city','country'])
                 .count()
                 .sort_values(['restaurant_id','city'], ascending = [False, True])
                 .reset_index())
    # gráfico
    fig = px.bar( df_aux.head(7),
           x='city',
           y='restaurant_id',
           color = 'country',
           labels = {'restaurant_id': ' Quantidade de restaurantes',
                    'city': 'Cidade',
                    'country': 'País'},
           text_auto=True,
           color_discrete_sequence = px.colors.qualitative.Plotly)
    
    return fig

def top_cuisi(df1):
    '''Esta função faz o top 10 das cidades com tipois de culinária distintos um gráfico de barras.
        
        Input: Dataframe
        Output: fig: gráfico de barras
    '''
    df_aux = (df1.loc[:, ['cuisines', 'city', 'country' ]]
                    .groupby(['city', 'country'])
                    .nunique()
                    .sort_values(['cuisines', 'city'], ascending = [False, True])
                    .reset_index())
    # gráfico

    fig = px.bar( df_aux.head(10),
           x='city',
           y='cuisines',
           color = 'country',
           labels = {'cuisines': ' Quantidade de Tipos de Culinária Únicos',
                    'city': 'Cidade',
                    'country': 'Países'},
           text_auto=True,
           color_discrete_sequence = px.colors.qualitative.Plotly)
    
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

st.title('🏙️ Métricas Cidades')


with st.container():
    st.markdown('### Top 10 Cidades com mais Restaurantes na Base de Dados')
    fig = top_rest (df1)
    st.plotly_chart( fig, use_container_width = True )
    
with st.container():
    col1, col2 = st.columns( 2 )
    
    with col1:
        st.markdown('##### Top 7 Cidades - Restaurantes com Avg. rating acima de 4')
        fig = avg_4 (df1)
        st.plotly_chart( fig, use_container_width = True )

    with col2:
        st.markdown('##### Top 7 Cidades - Restaurantes com Avg. rating abaixo de 2.5')
        fig = avg_2 (df1)
        st.plotly_chart( fig, use_container_width = True )

with st.container():
    st.markdown('### Top 10 Cidades com tipos culinários distintos')
    fig = top_cuisi (df1)
    st.plotly_chart( fig, use_container_width = True )
    
            
   
      
    

            
            

