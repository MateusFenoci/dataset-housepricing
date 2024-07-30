import streamlit as st
import pandas as pd
import plotly.express as px
from google_maps_api.scripts.utils import get_lat_lon, get_features
from utils.use_neural_network import make_prediction




st.set_page_config(page_title='Precificando Aluguel', page_icon=':bar_chart:', layout='wide')


metros_quadrados = st.number_input('Quantos metros quadrados? Apenas números')
vagas_carros = st.number_input('Quantas vagas de carros? Apenas números')
condominio = st.number_input('Qual o valor do condomínio? Apenas números')
iptu = st.number_input('Qual o valor do IPTU? Apenas números')
seguro_incendio = st.number_input('Qual o valor do Seguro Incêndio? Apenas números')
e_mobiliado = st.selectbox('O imóvel é mobiliado?', ['Sim', 'Não'])

if e_mobiliado == 'Sim':
    e_mobiliado = 1
else:
    e_mobiliado = 0

endereco = st.text_input('Endereço de sua residência: (Ex: Rua, Bairro, Cidade)')

def prediction():
    lat, lon = get_lat_lon(endereco)

    features = get_features(lat, lon)


    df = pd.DataFrame({
        'Square Meters': metros_quadrados,
        'Parking Spaces': vagas_carros,
        'Condo Fee': condominio,
        'Property Tax': iptu,
        'Fire Insurance': seguro_incendio,
        'Furnished?': e_mobiliado,
        **features
    }, index=[0])

    
    result = make_prediction(df)

    st.success(f"O valor do aluguel estimado é de R$ {result[0][0]:.2f}")

    return 1

st.button('Calcular', on_click=prediction)


