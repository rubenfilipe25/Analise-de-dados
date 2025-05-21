import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import math
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import scipy.stats as stats
import numpy as np
import carrega_dados  # Importa função de carregamento de dados

  # Importa função de carregamento de dados

df = carrega_dados.carregar_dados()

# Mapeamento dos nomes das variáveis
variable_names = {
    "year": "Ano",
    "make": "Marca",
    "model": "Modelo",
    "trim": "cc",
    "body": "Segmento",
    "transmission": "Transmissão",
    "vin": "ID",
    "state": "Estado",
    "condition": "Condição",
    "odometer": "Km",
    "color": "Cor",
    "interior": "Interior",
    "seller": "Vendedor",
    "mmr": "Valor de Mercado",
    "sellingprice": "Preço de Venda",
    "saledate": "Data de Venda"
}

# Reverter o dicionário para facilitar a tradução
reverse_variable_names = {v: k for k, v in variable_names.items()}

st.write("### Análise Isolada de Variáveis")

# Exibir o dropdown com os nomes amigáveis
variable = st.selectbox(
    "Selecione uma variável para analisar",
    list(variable_names.values())
)

# Mapeia o nome amigável de volta para o nome real da coluna
real_variable = reverse_variable_names[variable]

frequencias = df[real_variable].value_counts().reset_index()
frequencias.columns = [real_variable, "Frequência"]

# Criar coluna de porcentagem
frequencias["% do Total"] = (frequencias["Frequência"] / frequencias["Frequência"].sum() * 100).round(2)

# Criar layout com métricas destacadas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Moda (Mais comum)", frequencias.iloc[0, 0])

with col2:
    st.metric("Média de Ocorrências", f"{frequencias['Frequência'].mean():,.0f}")

with col3:
    st.metric("Mediana de Ocorrências", f"{frequencias['Frequência'].median():,.0f}")

# Adicionar o slider para definir o número de categorias a exibir
top_n = st.slider("Número de categorias para o gráfico:", min_value=1, max_value=20, value=10)

# Se for variável numérica, mostrar distribuição
if df[real_variable].dtype in ['int64', 'float64']:
    top_n_counts = df[real_variable].value_counts().nlargest(top_n)

    fig = px.bar(
        x=top_n_counts.index,
        y=top_n_counts.values,
        text=top_n_counts.values,
        labels={'x': real_variable, 'y': 'Frequência'},
        title=f"Distribuição de {real_variable}",
        color=top_n_counts.index,  # Cor automática para cada barra
        color_discrete_sequence=px.colors.qualitative.Prism
    )

else:
    # Para variáveis categóricas, mostrar os top N valores
    category_counts = df[real_variable].value_counts().nlargest(top_n)

    fig = px.bar(
        x=category_counts.values,
        y=category_counts.index,
        text=category_counts.values,
        labels={'x': 'Frequência', 'y': real_variable},
        title=f"Top {top_n} categorias - {real_variable}",
        orientation='h',
        color=category_counts.index,  # Cor automática para cada barra
        color_discrete_sequence=px.colors.qualitative.Prism
    )

# Melhorias no layout
fig.update_traces(textposition='outside')
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="black")
)

# Exibir gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Análise estatística para variáveis numéricas com emojis
if df[real_variable].dtype in ['int64', 'float64']:
    st.write("**📊 Estatísticas Descritivas:**")
    st.write(f"🔢 **Média**: {df[real_variable].mean():.2f}")
    st.write(f"📏 **Desvio Padrão**: {df[real_variable].std():.2f}")
    st.write(f"📉 **Mínimo**: {df[real_variable].min()}")
    st.write(f"📈 **Máximo**: {df[real_variable].max()}")
    st.write(f"🔘 **Mediana**: {df[real_variable].median()}")
    st.write(f"🔠 **Quartil 1 (25%)**: {df[real_variable].quantile(0.25)}")
    st.write(f"🔡 **Quartil 3 (75%)**: {df[real_variable].quantile(0.75)}")

else:
    # Para variáveis categóricas, mostrar contagens paginadas (3 por linha)
    st.write("**📊 Análise de Contagem:**")

    # Obtém todas as contagens de categorias
    category_counts = df[real_variable].value_counts()

    # Definir o tamanho da página
    page_size = 21  # Múltiplo de 3 para garantir linhas completas
    total_pages = -(-len(category_counts) // page_size)  # Arredonda para cima

    # Criar estado para armazenar a página atual
    if "page_number" not in st.session_state:
        st.session_state.page_number = 1

    # Calcula os índices para exibição
    start_idx = (st.session_state.page_number - 1) * page_size
    end_idx = start_idx + page_size
    display_counts = category_counts[start_idx:end_idx]

    # Exibir os valores 3 por linha
    cols = st.columns(3)  # Cria 3 colunas
    for i, (category, count) in enumerate(display_counts.items()):
        with cols[i % 3]:  # Distribui entre as colunas
            st.write(f"🔢 **{category}:** {count}")

    # Criar os botões de paginação
    col1, col2, col3 = st.columns([1, 2, 1])

    # Botão "Anterior"
    if col1.button("⬅ Anterior", disabled=(st.session_state.page_number == 1)):
        st.session_state.page_number -= 1

    # Mostrar a página atual
    col2.write(f"📄 Página {st.session_state.page_number} de {total_pages}")

    # Botão "Próxima"
    if col3.button("Próxima ➡", disabled=(st.session_state.page_number == total_pages)):
        st.session_state.page_number += 1






