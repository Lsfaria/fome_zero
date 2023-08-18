# libraries

import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config( page_title='Gastronomy', page_icon='🍽️', layout='wide' )

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

def best_food(df1, cuisine):
    
    '''Esta função encontra o melhor restaurante para um determinado tipo de culinária.

    Input: 
        - Dataframe : O DataFrame contendo os dados do restaurante
        - Cuisines: A cozinha para pesquisar
    Output: melhor_cuisine: O restaurante com a classificação agregada mais alta para a culinária especificada.
    '''
    
    
    if cuisine == 'Italian':
        df_aux = (df1.loc[df1.loc[:, 'cuisines'] == 'Italian', ['restaurant_name','restaurant_id', 'aggregate_rating', 'country', 'city', 'average_cost_for_two','votes','currency']]
                     .sort_values('aggregate_rating', ascending = False)
                     .reset_index(drop= True))
            
        agg_rating_max = df_aux['aggregate_rating'].max()
        df_aux = (df_aux.loc[df_aux['aggregate_rating'] == agg_rating_max, : ]
                        .sort_values('restaurant_id', ascending = True)
                        .reset_index(drop= True))
        melhor_cuisine = df_aux.loc[0, :]
        
        return melhor_cuisine
    
    elif cuisine == 'American':
        df_aux = (df1.loc[df1.loc[:, 'cuisines'] == 'American', ['restaurant_name','restaurant_id', 'aggregate_rating', 'country', 'city', 'average_cost_for_two','votes','currency']]
                     .sort_values('aggregate_rating', ascending = False)
                     .reset_index(drop= True))
            
        agg_rating_max = df_aux['aggregate_rating'].max()
        df_aux = (df_aux.loc[df_aux['aggregate_rating'] == agg_rating_max, : ]
                            .sort_values('restaurant_id', ascending = True)
                            .reset_index(drop= True))
        melhor_cuisine = df_aux.loc[0, :]
        
        return melhor_cuisine
 
    elif cuisine == 'Arabian':
            df_aux = (df1.loc[df1.loc[:, 'cuisines'] == 'Arabian', ['restaurant_name','restaurant_id', 'aggregate_rating', 'country', 'city', 'average_cost_for_two','votes','currency']]
                         .sort_values('aggregate_rating', ascending = False)
                         .reset_index(drop= True))

            agg_rating_max = df_aux['aggregate_rating'].max()
            df_aux = (df_aux.loc[df_aux['aggregate_rating'] == agg_rating_max, : ]
                            .sort_values('restaurant_id', ascending = True)
                            .reset_index(drop= True))
            melhor_cuisine = df_aux.loc[0, :]

            return melhor_cuisine
        
    elif cuisine == 'Japanese':
        
        df_aux = (df1.loc[df1.loc[:, 'cuisines'] == 'Japanese', ['restaurant_name','restaurant_id', 'aggregate_rating', 'country', 'city', 'average_cost_for_two','votes','currency']]
                     .sort_values('aggregate_rating', ascending = False)
                     .reset_index(drop= True))

        agg_rating_max = df_aux['aggregate_rating'].max()
        df_aux = (df_aux.loc[df_aux['aggregate_rating'] == agg_rating_max, : ]
                            .sort_values('restaurant_id', ascending = True)
                            .reset_index(drop= True))
        melhor_cuisine = df_aux.loc[0, :]

        return melhor_cuisine
    
    elif cuisine == 'Brazilian':
        df_aux = (df1.loc[df1.loc[:, 'cuisines'] == 'Brazilian', ['restaurant_name','restaurant_id', 'aggregate_rating', 'country', 'city', 'average_cost_for_two','votes','currency']]
                     .sort_values('aggregate_rating', ascending = False)
                     .reset_index(drop= True))

        agg_rating_max = df_aux['aggregate_rating'].max()
        df_aux = (df_aux.loc[df_aux['aggregate_rating'] == agg_rating_max, : ]
                            .sort_values('restaurant_id', ascending = True)
                            .reset_index(drop= True))
        melhor_cuisine = df_aux.loc[0, :]

        return melhor_cuisine
    
def top_rest(df1):
    '''Esta função retorna com um dataframe dos restaurantes mais bem avaliados.
    

    Input: Dataframe
    Output:Dataframe
    '''
    df_aux = (df2.loc[: , ['restaurant_id','restaurant_name', 'country','city', 'cuisines', 'average_cost_for_two', 'aggregate_rating','votes']]
                 .sort_values('aggregate_rating', ascending = False)
                 .reset_index(drop= True))
    agg_rating_max = df_aux['aggregate_rating'].max()

    df_top = (df_aux.loc[df_aux['aggregate_rating'] == agg_rating_max, : ]
                    .sort_values('restaurant_id', ascending = True)
                    .reset_index(drop= True))
    return df_top


def avg_delivery(df1):
    '''Esta função faz a distribuição do média da quantidade de avaliações c/ delivery e devolve um gráfico de rosca.
    
    Input: Dataframe
    Output:fig: gráfico de rosca
    '''
    df_aux = df1.loc[:, ['has_online_delivery', 'votes' ]].groupby(['has_online_delivery']).mean().reset_index()
    fig = px.pie(df_aux,
    values='votes',
    names=["Não faz entrega", "Faz entrega"],
    hole=0.6,
    labels = {'votes': 'Quantidade de Avaliações'})
    fig.update_traces(texttemplate='%{value:.2s}<br> %{percent}', textposition='inside', textfont_size=12)
    
    return fig


def avg_cost(df1):
    '''Esta função faz a distribuição do custo médio para os restaurantes que possuem reserva e devolve um gráfico de rosca.
    
    Input: Dataframe
    Output:fig: gráfico de rosca
    '''
    df_aux = df1.loc[:, ['has_table_booking', 'price_in_dollar' ]].groupby(['has_table_booking']).mean().reset_index()
    fig = px.pie(df_aux,
    values='price_in_dollar',
    names=['Não faz reserva', 'Faz reserva'],
    hole=0.6,
    labels = {'price_in_dollar': 'Custo do prato'})
    fig.update_traces(texttemplate='%{value:.2s}<br> %{percent}', textposition='inside', textfont_size=12)
    
    return fig


def top_cuisine(df1):
    '''Esta função retorna o top 10 das culinárias mais caras e devolve um gráfico de barras.
    
    Input: Dataframe
    Output:fig: gráfico de barras
    '''
    df_aux = (df2.loc[:, ['price_in_dollar', 'cuisines' ]]
                 .groupby(['cuisines'])
                 .mean()
                 .sort_values('price_in_dollar', ascending = False)
                 .reset_index())
    fig = px.bar( df_aux.head(quantidade_rest),
    x='cuisines',
    y='price_in_dollar',
    labels = {'cuisines': 'Culinárias', 'price_in_dollar': 'Custo em Dólar'},
    text_auto='.2f')

    return fig

def avg_cuisine_top(df1):
    '''Esta função retorna o top 10 das culinárias com as melhores médias de avaliaçãoe devolve um gráfico de barras.
    
    Input: Dataframe
    Output:fig: gráfico de barras
    '''
    df_aux = (df2.loc[:, ['cuisines', 'aggregate_rating' ]]
                 .groupby(['cuisines'])
                 .mean()
                 .sort_values('aggregate_rating', ascending = False)
                 .reset_index())
    df_aux = df_aux.loc[df_aux['aggregate_rating'] != 0, :]

    fig = px.bar( df_aux.head(quantidade_rest),
                  x='cuisines',
                  y='aggregate_rating',
                  labels = {'cuisines': 'Tipo de Culinária', 'aggregate_rating': 'Avaliação Média'},
                  text_auto='.2f')
    return fig


def avg_cuisine_bot(df1):
    '''Esta função retorna o top 10 das culinárias com as piores médias de avaliaçãoe devolve um gráfico de barras.
    
    Input: Dataframe
    Output:fig: gráfico de barras
    '''
    df_aux = (df2.loc[:, ['cuisines', 'aggregate_rating' ]]
              .groupby(['cuisines'])
              .mean()
              .sort_values('aggregate_rating', ascending = True)
              .reset_index())
    df_aux = df_aux.loc[df_aux['aggregate_rating'] != 0, :]

    fig = px.bar( df_aux.head(quantidade_rest),
                  x='cuisines',
                  y='aggregate_rating',
                  labels = {'cuisines': 'Tipo de Culinária', 'aggregate_rating': 'Avaliação Média'},
                  text_auto='.2f')
    return fig

def top_offer(df1):
    '''Esta função retorna o top 10 das culinárias mais ofertadas.
    
    Input: Dataframe
    Output:fig: gráfico de barras
    '''
    df_aux = (df2.loc[:, ['restaurant_id', 'cuisines' ]]
                 .groupby(['cuisines'])
                 .count()
                 .sort_values('restaurant_id', ascending = False)
                 .reset_index())
    fig = px.funnel(df_aux.head(quantidade_rest), x='restaurant_id', y='cuisines',color='cuisines')
    fig.update_layout(showlegend=False)

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
lista_culinarias = list(df1['cuisines'].unique())

country_options = st.sidebar.multiselect( 
                                         'Escolha os Paises que deseja visualizar:',
                                         lista_paises,
                                         default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia']
)
              
quantidade_rest = st.sidebar.slider(
                                    'Selecione a quantidade de Restaurantes/Culinárias que deseja visualizar:',
                                    value=10,
                                    min_value= 1,
                                    max_value=20
)

cuisine_options = st.sidebar.multiselect(
                                         'Selecione as Culinárias que deseja visualizar: ',
                                         lista_culinarias,
                                         default = lista_culinarias
)

# Filtro de países e das culinárias
selec_cuisines = df1['cuisines'].isin(cuisine_options)
selec_country = df1['country'].isin(country_options)
df2 = df1.loc[(selec_cuisines & selec_country), :]

# ==========================================================================
# Layout no Streamlit
# ==========================================================================

st.title ('🍽️ Métricas Gastronômicas')

tab1, tab2 = st.tabs( ['Visão Restaurantes', ' Visão Culinárias'] )

with tab1:

    with st.container():
        st.markdown ('### Melhores Restaurantes dos Principais tipos Culinários')
        col1, col2, col3, col4, col5 = st.columns( 5 )

        with col1:
            melhor_italian = best_food (df1, 'Italian')
            col1.metric(label = f'Italiana: {melhor_italian["restaurant_name"]}',
                        value = f'{melhor_italian["aggregate_rating"]}/5.0', 
                        help=f""" 
                        País: {melhor_italian["country"]} \n
                        Cidade: {melhor_italian["city"]} \n
                        Preço para duas pessoas: {melhor_italian["currency"]}{melhor_italian["average_cost_for_two"]} 
                    """
                    )
        with col2:
            melhor_american = best_food (df1, 'American')
            col2.metric(label = f'Americana: {melhor_american["restaurant_name"]}',
                        value = f'{melhor_american["aggregate_rating"]}/5.0', 
                        help=f""" 
                        País: {melhor_american["country"]} \n
                        Cidade: {melhor_american["city"]} \n
                        Preço para duas pessoas: {melhor_american["currency"]}{melhor_american["average_cost_for_two"]} 
                    """
                    )
        with col3:
            melhor_arabe = best_food (df1, 'Arabian')
            col3.metric(label = f'Árabe: {melhor_arabe["restaurant_name"]}',
                        value = f'{melhor_arabe["aggregate_rating"]}/5.0', 
                        help=f""" 
                        País: {melhor_arabe["country"]} \n
                        Cidade: {melhor_arabe["city"]} \n
                        Preço para duas pessoas: {melhor_arabe["currency"]}{melhor_arabe["average_cost_for_two"]} 
                    """
                    )
        with col4:
            melhor_japa = best_food (df1, 'Japanese')
            col4.metric(label = f'Japonesa: {melhor_japa["restaurant_name"]}',
                        value = f'{melhor_japa["aggregate_rating"]}/5.0', 
                        help=f""" 
                        País: {melhor_japa["country"]} \n
                        Cidade: {melhor_japa["city"]} \n
                        Preço para duas pessoas: {melhor_japa["currency"]}{melhor_japa["average_cost_for_two"]} 
                    """
                    )
        with col5:
            melhor_br = best_food (df1, 'Brazilian')
            col5.metric(label = f'Brasileira: {melhor_br["restaurant_name"]}',
                        value = f'{melhor_br["aggregate_rating"]}/5.0', 
                        help=f""" 
                        País: {melhor_br["country"]} \n
                        Cidade: {melhor_br["city"]} \n
                        Preço para duas pessoas: {melhor_br["currency"]}{melhor_br["average_cost_for_two"]} 
                    """
                    )

    with st.container():
        st.markdown (f'### Top {quantidade_rest} Restaurantes')
        df_top = top_rest (df1)
        st.dataframe( df_top.head(quantidade_rest) )

    with st.container():

        col1, col2 = st.columns( 2 )

        with col1:
            st.markdown (f'##### Média da quantidade de avaliações c/ delivery')
            fig = avg_delivery (df1)
            st.plotly_chart( fig, use_container_width = True )

        with col2:
            st.markdown (f'##### Custo médio dos restaurantes que possuem reserva')
            fig = avg_cost (df1)
            st.plotly_chart( fig, use_container_width = True )
        
with tab2:
    
    with st.container():
        st.markdown (f'#### Top {quantidade_rest} Culinárias Mais Caras')
        fig = top_cuisine (df1)                   
        st.plotly_chart( fig, use_container_width = True )              
    
    with st.container():

        col1, col2 = st.columns( 2 )

        with col1:    
            st.markdown (f'#### Top 10 Melhores Avaliações Médias de Culinária')
            fig = avg_cuisine_top (df1)
            st.plotly_chart( fig, use_container_width = True )

        with col2:
            st.markdown (f'#### Top 10 Piores Avaliações Médias de Culinária')
            fig = avg_cuisine_bot (df1)
            st.plotly_chart( fig, use_container_width = True )
            
        with st.container():
            st.markdown (f'#### Top {quantidade_rest} Culinárias mais Ofertadas')
            fig = top_offer (df1)
            st.plotly_chart( fig, use_container_width = True )
            