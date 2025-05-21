import pandas as pd
import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score

# Carregar e preparar os dados
def main():
    # Limitar a leitura a 100 mil linhas para otimizar o desempenho
    df = pd.read_csv('car_prices_sem_na.csv', nrows=100000)  # Lê apenas as primeiras 100 mil linhas

    # Remove colunas irrelevantes ou identificadores
    df.columns = df.columns.str.strip()  # Remove espaços nos nomes das colunas
    df = df.drop(columns=['Unnamed: 0', 'vin', 'seller'])


    # Codificação de variáveis categóricas
    df_encoded = pd.get_dummies(df, drop_first=True)

    # Separar as variáveis independentes (X) e a variável dependente (y)
    X = df_encoded.drop('sellingprice', axis=1)
    y = df_encoded['sellingprice']

    # Divisão dos dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # Inicialização do modelo de regressão linear
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Interface do Streamlit
    st.title("Previsão do Preço de Venda de Carros")

    # Inputs do utilizador
    year = st.slider('Ano', int(df['year'].min()), int(df['year'].max()))
    make = st.selectbox('Marca', df['make'].unique())
    model_input = st.selectbox('Modelo', df[df['make'] == make]['model'].unique())
    trim = st.selectbox('Versão', df['trim'].unique())
    body = st.selectbox('Tipo de carroçaria', df['body'].unique())
    transmission = st.selectbox('Transmissão', df['transmission'].unique())
    state = st.selectbox('Estado (EUA)', df['state'].unique())
    condition = st.slider('Condição', 1, 5)
    color = st.selectbox('Cor', df['color'].unique())
    interior = st.selectbox('Interior', df['interior'].unique())

    # Construção do DataFrame do novo carro com os inputs
    new_car = pd.DataFrame([{
        'year': year,
        'make': make,
        'model': model_input,
        'trim': trim,
        'body': body,
        'transmission': transmission,
        'state': state,
        'condition': condition,
        'color': color,
        'interior': interior,
    }])

    # Codificação das variáveis categóricas do novo carro
    new_car_encoded = pd.get_dummies(new_car)
    missing_cols = set(X.columns) - set(new_car_encoded.columns)
    for col in missing_cols:
        new_car_encoded[col] = 0
    new_car_encoded = new_car_encoded[X.columns]  # garantir que as colunas têm a mesma ordem

    # Previsão
    predicted_price = model.predict(new_car_encoded)

    # Mostrar o preço previsto
    st.subheader(f"Preço previsto de venda: ${predicted_price[0]:,.2f}")

# Chama a função principal para rodar a aplicação Streamlit
if __name__ == '__main__':
    main()
