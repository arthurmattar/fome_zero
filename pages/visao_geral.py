#------------------
#Libraries---------
#------------------

import pandas as pd
import folium
import io
import inflection
from haversine import haversine
import streamlit as st
import plotly.express as px

#------------------
#Arquivos----------
#------------------

df_raiz = pd.read_csv("zomato.csv")
df = df_raiz.copy()

#------------------
#Dicionários-------
#------------------

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


#------------------
#Funções-----------
#------------------


def country_name(country_id):
    return COUNTRIES[country_id]


def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    elif price_range == 4:
        return "very expensive"
    

def color_name(color_code):
    return COLORS[color_code]


def rename_columns(dataframe):
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


def clean_code(df):

    #0.1: Transformar colunas nos tipos corretos (int, str ou float)
    df["Cuisines"] = df["Cuisines"].astype(str)

    #0.2: Alterar valores e/ou informações
    df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

    #0.3: Adicionar valores e/ou informações
    df["Country Code"] = df.loc[:, "Country Code"].apply(lambda x: country_name(x))
    df["Rating color"] = df.loc[:, "Rating color"].apply(lambda x: color_name(x))
    df["Price range"] = df.loc[:, "Price range"].apply(lambda x: create_price_type(x))

    #0.4: Renomear colunas
    df = rename_columns(df)

    #0.5: Remover duplicatas
    df = df.drop_duplicates(subset="restaurant_id")
    
    return df


def groupby_columns (df,dimensions,values,metrics,order=False):
    cols = []
    for i in dimensions:
      cols.append(i)
    for i in values:
      cols.append(i)
    df1 = df.loc[:,cols].groupby(dimensions).agg(metrics).reset_index()
    cols_names = []
    for i in dimensions:
      cols_names.append(i)
    for i in values:
      for j in metrics:
        coluna = i + "_" + j
        cols_names.append(coluna)
    df1.columns = cols_names
    df1 = df1.sort_values(cols_names[len(cols_names)-1],ascending=order).reset_index()
    df1 = df1.head(5)
    return df1


#------------------
#Formatação do DF--
#------------------

df = clean_code(df)


#---------------------------
#layout Sidebar==-----------
#---------------------------

country_options = st.sidebar.multiselect('Países selecionados',df['country_code'].unique(),default=df['country_code'].unique())
df = df.loc[df['country_code'].isin(country_options),:]

cuisines_options = st.sidebar.multiselect('Tipos de culinária selecionados',df['cuisines'].unique(),default=df['cuisines'].unique())
df = df.loc[df['cuisines'].isin(cuisines_options),:]


#---------------------------
#layout da Página-----------
#---------------------------



st.header('Overview Geral')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    #1.1
    with col1:
        df_aux = df.loc[:,'restaurant_id'].nunique()
        st.metric(label='Total Restaurantes',value=df_aux)

    #1.2
    with col2:
        df_aux = df.loc[:,'country_code'].nunique()
        st.metric(label='Total Países',value=df_aux)

    #1.3
    with col3:
        df_aux = df.loc[:,'city'].nunique()
        st.metric(label='Total Cidades',value=df_aux)

    #1.4
    with col4:
        df_aux = df.loc[:,'votes'].sum()
        st.metric(label='Total avaliações',value=df_aux)

    #1.5
    with col5:  
        df_aux = df.loc[:,'cuisines'].nunique()
        st.metric(label='Total Culinárias',value=df_aux)





    