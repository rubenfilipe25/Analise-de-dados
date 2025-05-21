import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta
import carrega_dados  # Importa função de carregamento de dados

df = carrega_dados.carregar_dados()


# Simulação de dados de estados com taxas e tempo de importação
states_data = {
    "ca": {"tax": 0.08, "days": 10},
    "Texas": {"tax": 0.06, "days": 7},
    "Florida": {"tax": 0.07, "days": 8},
    "New York": {"tax": 0.09, "days": 12}
}

company_fee = 500  # Taxa fixa da empresa
iva_portugues = 0.23  # IVA de Portugal 23%


def calculate_import_cost(state, car_price):
    state_tax = states_data[state]["tax"]
    tax_amount = car_price * state_tax
    iva_amount = car_price * iva_portugues
    total_cost = car_price + tax_amount + company_fee + iva_amount
    return total_cost, states_data[state]["days"], tax_amount, iva_amount




def mostrar():

    # Interface Streamlit
    st.title("Calculadora de Importação de Veículos")

    # Seleção da marca
    todas_marcas = df["make"].unique()
    make1 = st.selectbox("Escolha a marca do veículo", todas_marcas)

    # Filtrar os modelos apenas das marcas disponíveis
    modelos_disponiveis = df[df["make"] == make1]["model"].unique()
    veiculo1 = st.selectbox("Escolha o modelo do veículo", modelos_disponiveis)

    # Filtrar os estados onde esse modelo está disponível
    estados_disponiveis = df[df["model"] == veiculo1]["state"].unique()
    state = st.selectbox("Selecione o Estado de Origem", estados_disponiveis)

    # Filtrar dataframe para obter os detalhes do veículo
    dados_veiculo1 = df[(df["make"] == make1) & (df["model"] == veiculo1) & (df["state"] == state)].iloc[0]

    st.subheader(f"{make1} {veiculo1}")
    st.write(f"📅 **Ano:** {dados_veiculo1['year']}")
    st.write(f"⚙️ **Trim:** {dados_veiculo1['trim']}")
    st.write(f"🚗 **Categoria:** {dados_veiculo1['body']}")
    st.write(f"🔄 **Caixa:** {dados_veiculo1['transmission']}")
    st.write(f"📍 **Estado:** {dados_veiculo1['state']}")
    st.write(f"📌 **Condição:** {dados_veiculo1['condition']}")
    st.write(f"⏳ **Km:** {dados_veiculo1['mmr']}")
    st.write(f"🎨 **Cor:** {dados_veiculo1['color']}")
    st.write(f"💰 **Preço do Veiculo:** {dados_veiculo1['sellingprice']} €")

    # Obter o preço do veículo selecionado
    car_price = dados_veiculo1["sellingprice"]

    # Botão de cálculo
    if st.button("Calcular"):
        total_cost, import_days, tax_amount, iva_amount = calculate_import_cost(state, car_price)
        arrival_date = datetime.now() + timedelta(days=import_days)

        st.subheader("🧾 Fatura de Importação")
        st.write(f"- **Preço do Veículo:** ${car_price:.2f}")
        st.write(f"- **Taxa de Importação ({states_data[state]['tax'] * 100}%):** ${tax_amount:.2f}")
        st.write(f"- **IVA Português (23%):** ${iva_amount:.2f}")
        st.write(f"- **Taxa da Empresa:** ${company_fee:.2f}")
        st.write(f"### 💰 Custo Total de Importação: ${total_cost:.2f}")
        st.write(f"### 📦 Dias estimados para entrega: {import_days} dias")
        st.write(f"### 📅 Data estimada de chegada: {arrival_date.strftime('%Y-%m-%d')}")
