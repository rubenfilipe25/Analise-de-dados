import joblib
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
import carrega_dados

# Carregar os dados
df = carrega_dados.carregar_dados()

# Codificação de variáveis categóricas
df_encoded = pd.get_dummies(df, drop_first=True)

# Separar as variáveis independentes (X) e a variável dependente (y)
X = df_encoded.drop('sellingprice', axis=1)
y = df_encoded['sellingprice']

# Normalização (opcional, caso seja necessário)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Inicialização do modelo de regressão linear
model = LinearRegression()
model.fit(X_train, y_train)

# Salvar o modelo treinado
joblib.dump(model, 'modelo_carro.pkl')

