import streamlit as st
import pandas as pd
import plotly.express as px
import carrega_dados

# ⏳ Cache para não recarregar o CSV constantemente
@st.cache_data
def obter_dados():
    return carrega_dados.carregar_dados()

df = obter_dados()

def main():

    st.title("Dashboard de Análise de Vendas")

    opcoes = [
        "Boxplot de Vendas por Estado",
        "Vendas por Segmento do Carro",
        "Vendas por Transmissão",
        "Marca vs Estado",
        "Preço de Venda vs Quilometragem"
    ]

    grafico_escolhido = st.selectbox("Escolha o gráfico que deseja visualizar:", opcoes)

    if grafico_escolhido == "Boxplot de Vendas por Estado":


        # Dicionário de nomes dos estados
        state_names = {
            "ca": "California", "tx": "Texas", "pa": "Pennsylvania", "mn": "Minnesota",
            "az": "Arizona", "wi": "Wisconsin", "tn": "Tennessee", "md": "Maryland",
            "fl": "Florida", "ne": "Nebraska", "nj": "New Jersey", "nv": "Nevada",
            "oh": "Ohio", "mi": "Michigan", "ga": "Georgia", "va": "Virginia",
            "sc": "South Carolina", "nc": "North Carolina", "in": "Indiana", "il": "Illinois",
            "co": "Colorado", "ut": "Utah", "mo": "Missouri", "ny": "New York",
            "ma": "Massachusetts", "pr": "Puerto Rico", "or": "Oregon", "la": "Louisiana",
            "wa": "Washington", "hi": "Hawaii", "qc": "Quebec", "ab": "Alberta",
            "on": "Ontario", "ok": "Oklahoma", "ms": "Mississippi", "nm": "New Mexico",
            "al": "Alabama"
        }

        # 🧊 GRÁFICO
        st.subheader(grafico_escolhido)

        fig = px.box(
            df, 
            x="state", 
            y="sellingprice", 
            points="outliers",
            labels={'sellingprice': 'Preço de Venda', 'state': 'Estado'},
            color="state",
            color_discrete_sequence=px.colors.qualitative.Prism
        )

        # Remove legenda do gráfico
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig)

        # 🧾 LEGENDA EXTERNA (abaixo do gráfico)
        st.markdown("### 🗺️ Legenda de Estados")

        # Lista formatada: "🔹 CA: California"
        state_legenda_texto = [f"🔹 **{abbr.upper()}**: {name}" for abbr, name in state_names.items()]
        state_legenda_texto.sort()

        # Divide em colunas
        col1, col2, col3 = st.columns(3)

        for i, item in enumerate(state_legenda_texto):
            if i % 3 == 0:
                col1.markdown(item)
            elif i % 3 == 1:
                col2.markdown(item)
            else:
                col3.markdown(item)

    elif grafico_escolhido == "Vendas por Segmento do Carro":
        st.subheader(grafico_escolhido)

        # Contagem de vendas por tipo de carroçaria
        vendas_body = df['body'].value_counts().reset_index()
        vendas_body.columns = ['body', 'vendas']

        # Calcular percentagens
        total_vendas = vendas_body['vendas'].sum()
        vendas_body['percentagem'] = vendas_body['vendas'] / total_vendas

        # Agrupar categorias com menos de 2%
        limite = 0.02  # 2%
        principais = vendas_body[vendas_body['percentagem'] >= limite]
        outras = vendas_body[vendas_body['percentagem'] < limite]
        outras_total = outras['vendas'].sum()

        # Adicionar linha "Outros"
        vendas_agrupadas = principais.copy()
        if outras_total > 0:
            vendas_agrupadas.loc[len(vendas_agrupadas.index)] = ['Outros', outras_total, outras_total / total_vendas]

        # Gráfico de pizza com categorias agrupadas
        fig = px.pie(vendas_agrupadas, names='body', values='vendas',
                    labels={'vendas': 'Vendas'}, color='body',
                    color_discrete_sequence=px.colors.qualitative.Prism,
                    hover_data=['percentagem'])

        fig.update_traces(textinfo='percent+label')  # Mostrar só percentagem e nome
        st.plotly_chart(fig)


    elif grafico_escolhido == "Vendas por Transmissão":
        st.subheader(grafico_escolhido)
        vendas_transmissao = df['transmission'].value_counts().reset_index()
        vendas_transmissao.columns = ['transmission', 'vendas']
        fig = px.pie(vendas_transmissao, names='transmission', values='vendas',
                    labels={'vendas': 'Vendas'}, color='transmission',
                    color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig)

    elif grafico_escolhido == "Marca vs Estado":
        st.subheader(grafico_escolhido)

        # Dicionário com os nomes dos estados
        state_names = {
            "ca": "California", "tx": "Texas", "pa": "Pennsylvania", "mn": "Minnesota",
            "az": "Arizona", "wi": "Wisconsin", "tn": "Tennessee", "md": "Maryland",
            "fl": "Florida", "ne": "Nebraska", "nj": "New Jersey", "nv": "Nevada",
            "oh": "Ohio", "mi": "Michigan", "ga": "Georgia", "va": "Virginia",
            "sc": "South Carolina", "nc": "North Carolina", "in": "Indiana", "il": "Illinois",
            "co": "Colorado", "ut": "Utah", "mo": "Missouri", "ny": "New York",
            "ma": "Massachusetts", "pr": "Puerto Rico", "or": "Oregon", "la": "Louisiana",
            "wa": "Washington", "hi": "Hawaii", "qc": "Quebec", "ab": "Alberta",
            "on": "Ontario", "ok": "Oklahoma", "ms": "Mississippi", "nm": "New Mexico",
            "al": "Alabama"
        }

        # --- Parte do gráfico ---
        # Suponha que o DataFrame "df" já está filtrado

        # Substituir no DataFrame os códigos pelos nomes (para a legenda, se quiser no gráfico)
        df["state_name"] = df["state"].map(state_names).fillna(df["state"])

        top_marcas = df['make'].value_counts().nlargest(10).index
        df_filtrado = df[df['make'].isin(top_marcas)]
        make_state_count = df_filtrado.groupby(['make', 'state']).size().reset_index(name='count')

        fig = px.bar(
            make_state_count.sort_values(by="count", ascending=False),
            x="make", y="count", color="state",
            labels={'make': 'Marca', 'count': 'Contagem', 'state': 'Estado'},
            color_discrete_sequence=px.colors.qualitative.Prism
        )

        # Remove a legenda interna
        fig.update_layout(showlegend=False)

        # Exibe o gráfico
        st.plotly_chart(fig)

        # --- Parte da legenda fora do gráfico ---
        st.markdown("### 🗺️ Legenda de Estados")

        # Formata as strings
        state_legenda_texto = [f"🔹 **{abbr.upper()}**: {name}" for abbr, name in state_names.items()]
        state_legenda_texto.sort()

        # Divide em colunas
        col1, col2, col3 = st.columns(3)

        for i, item in enumerate(state_legenda_texto):
            if i % 3 == 0:
                col1.markdown(item)
            elif i % 3 == 1:
                col2.markdown(item)
            else:
                col3.markdown(item)


    elif grafico_escolhido == "Preço de Venda vs Quilometragem":
        st.subheader(grafico_escolhido)
        df_grouped = df.groupby('odometer').agg({'sellingprice': 'mean'}).reset_index()
        fig = px.line(df_grouped, x='odometer', y='sellingprice',
                    labels={'odometer': 'Quilometragem', 'sellingprice': 'Preço de Venda'},
                    markers=True, line_shape='linear',
                    color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig)
