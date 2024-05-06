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
        return "very_expensive"
    

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



st.header('Overview Países')

tab1, tab2, tab3 = st.tabs(['Restaurantes','Avaliações','Outros'])

#3.1, 3.6, 3.7 e 3.8
with tab1:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Nº Restaurantes por cidade')
            dimensions = ['city','country_code']
            values = ['restaurant_id']
            metrics = ['nunique']
            df_aux = groupby_columns(df,dimensions,values,metrics)
            fig = px.bar(df_aux,x='city',y='restaurant_id_nunique',color='country_code',text_auto=True,width=360)
            st.plotly_chart(fig)
    
        with col2:
            st.markdown('Nº Restaurantes que aceitam reserva')
            dimensions = ['city','country_code']
            values = ['restaurant_id']
            metrics = ['nunique']
            df_aux = df.loc[df['has_table_booking'] == 1,:]
            df_aux2 = groupby_columns(df_aux,dimensions,values,metrics)
            fig = px.bar(df_aux2,x='city',y='restaurant_id_nunique',color='country_code',text_auto=True,width=360)
            st.plotly_chart(fig)
    
                        
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Nº Restaurantes que aceitam pedidos online')
            dimensions = ['city','country_code']
            values = ['restaurant_id']
            metrics = ['nunique']
            df_aux = df.loc[df['has_online_delivery'] == 1,:]
            df_aux2 = groupby_columns(df_aux,dimensions,values,metrics)
            fig = px.bar(df_aux2,x='city',y='restaurant_id_nunique',color='country_code',text_auto=True,width=360)
            st.plotly_chart(fig)

        with col2:
            st.markdown('Nº Restaurantes que fazem entregas')
            dimensions = ['city','country_code']
            values = ['restaurant_id']
            metrics = ['nunique']
            df_aux = df.loc[df['is_delivering_now'] == 1,:]
            df_aux2 = groupby_columns(df_aux,dimensions,values,metrics)
            fig = px.bar(df_aux2,x='city',y='restaurant_id_nunique',color='country_code',text_auto=True,width=360)
            st.plotly_chart(fig)

    
#3.2 e 3.3
with tab2:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Nº Restaurantes com nota acima de 4')
            dimensions = ['city','country_code']
            values = ['restaurant_id']
            metrics = ['nunique']
            df_aux = df.loc[df['aggregate_rating'] >= 4.0,:]
            df_aux2 = groupby_columns(df_aux,dimensions,values,metrics)
            fig = px.bar(df_aux2,x='city',y='restaurant_id_nunique',color='country_code',text_auto=True,width=360)
            st.plotly_chart(fig)
    
        with col2:
            st.markdown('Nº Restaurantes com nota abaixo de 2.5')
            dimensions = ['city','country_code']
            values = ['restaurant_id']
            metrics = ['nunique']
            df_aux = df.loc[df['aggregate_rating'] <= 2.5,:]
            df_aux2 = groupby_columns(df_aux,dimensions,values,metrics)
            fig = px.bar(df_aux2,x='city',y='restaurant_id_nunique',color='country_code',text_auto=True,width=360)
            st.plotly_chart(fig)


#3.4 e 3.5
with tab3:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Maiores valores médios de um prato pra 2')
            dimensions = ['city','country_code']
            values = ['average_cost_for_two']
            metrics = ['mean']
            df_aux = groupby_columns(df,dimensions,values,metrics)
            df_aux = df_aux.apply(lambda x: round(x,2))
            fig = px.bar(df_aux,x='city',y='average_cost_for_two_mean',color='country_code',text_auto=True,width=360)
            st.plotly_chart(fig)
    
        with col2:
            st.markdown('Nº Tipos de culinária por cidade')
            dimensions = ['city','country_code']
            values = ['cuisines']
            metrics = ['nunique']
            df_aux = groupby_columns(df,dimensions,values,metrics)
            df_aux = df_aux.apply(lambda x: round(x,2))
            fig = px.bar(df_aux,x='city',y='cuisines_nunique',color='country_code',text_auto=True,width=360)
            st.plotly_chart(fig)



