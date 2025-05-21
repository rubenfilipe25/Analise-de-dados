import streamlit as st
import math
from datetime import datetime, timedelta
import carrega_dados  # Presumo que esta seja a tua função para carregar os dados

# Estado de sessão para navegação
if "calculo_detalhado" not in st.session_state:
    st.session_state.calculo_detalhado = False
if "carro_selecionado" not in st.session_state:
    st.session_state.carro_selecionado = None

df = carrega_dados.carregar_dados()

# Dados de estados
states_data = {
    "ca": {"tax": 0.08, "days": 10},
    "tx": {"tax": 0.06, "days": 7},
    "pa": {"tax": 0.07, "days": 9},
    "mn": {"tax": 0.065, "days": 8},
    "az": {"tax": 0.056, "days": 7},
    "wi": {"tax": 0.05, "days": 6},
    "tn": {"tax": 0.07, "days": 8},
    "md": {"tax": 0.06, "days": 7},
    "fl": {"tax": 0.07, "days": 8},
    "ne": {"tax": 0.055, "days": 7},
    "nj": {"tax": 0.066, "days": 9},
    "nv": {"tax": 0.0685, "days": 7},
    "oh": {"tax": 0.0575, "days": 8},
    "mi": {"tax": 0.06, "days": 7},
    "ga": {"tax": 0.04, "days": 6},
    "va": {"tax": 0.053, "days": 7},
    "sc": {"tax": 0.06, "days": 8},
    "nc": {"tax": 0.0475, "days": 7},
    "in": {"tax": 0.07, "days": 9},
    "il": {"tax": 0.0625, "days": 7},
    "co": {"tax": 0.029, "days": 5},
    "ut": {"tax": 0.0485, "days": 6},
    "mo": {"tax": 0.04225, "days": 7},
    "ny": {"tax": 0.09, "days": 12},
    "ma": {"tax": 0.0625, "days": 9},
    "pr": {"tax": 0.115, "days": 10},
    "or": {"tax": 0.0, "days": 5},
    "la": {"tax": 0.0445, "days": 6},
    "wa": {"tax": 0.065, "days": 8},
    "hi": {"tax": 0.04, "days": 7},
    "qc": {"tax": 0.09975, "days": 14},
    "ab": {"tax": 0.05, "days": 10},
    "on": {"tax": 0.13, "days": 15},
    "ok": {"tax": 0.045, "days": 7},
    "ms": {"tax": 0.07, "days": 8},
    "nm": {"tax": 0.05125, "days": 6},
    "al": {"tax": 0.04, "days": 7}
}

company_fee = 500
iva_portugal = 0.23
cars_per_page = 10

def calculate_import_cost(state, car_price):
    if state in states_data:
        state_tax = states_data[state]["tax"]
        tax_amount = car_price * state_tax
        iva_amount = car_price * iva_portugal
        total_cost = car_price + tax_amount + iva_amount + company_fee
        return total_cost, tax_amount, iva_amount, states_data[state]["days"]
    else:
        return None, None, None, None

def mostrar_calculo_detalhado():
    st.title("🧮 Cálculo Detalhado de Importação")
    carro = st.session_state.carro_selecionado
    if carro is None:
        st.warning("Nenhum carro selecionado.")
        return

    row = carro
    valid_state = row["state"]
    total_cost, tax_amount, iva_amount, import_days = calculate_import_cost(valid_state, row["sellingprice"])
    arrival_date = datetime.now() + timedelta(days=import_days)

    st.write(f"**{row['make']} {row['model']} ({row['year']})**")
    st.write(f"📍 Estado: {row['state']}")
    st.write(f"🛒 Preço Base: {row['sellingprice']} €")
    st.write(f"🏛 Taxa Estadual: {tax_amount:.2f} €")
    st.write(f"🇵🇹 IVA Portugal: {iva_amount:.2f} €")
    st.write(f"🏢 Taxa da Empresa: {company_fee} €")
    st.write(f"💰 Custo Total: {total_cost:.2f} €")
    st.write(f"📅 Data estimada de chegada: {arrival_date.strftime('%Y-%m-%d')}")

    if st.button("🔙 Voltar"):
        st.session_state.calculo_detalhado = False
        st.session_state.carro_selecionado = None
        st.experimental_rerun()

def mostrar():
    st.title("📦 Calculadora de Importação de Veículos")

    # Filtros
    with st.form("filtros"):
        col1, col2, col3 = st.columns(3)

        with col1:
            make1 = st.selectbox("Marca", options=["Todos"] + df["make"].unique().tolist(), index=0)
            min_year, max_year = int(df["year"].min()), int(df["year"].max())
            year_range = st.slider("Ano (intervalo)", min_year, max_year, (min_year, max_year))
            body = st.selectbox("Categoria", options=["Todos"] + df["body"].unique().tolist(), index=0)
            min_odo, max_odo = int(df["mmr"].min()), int(df["mmr"].max())
            odometer = st.slider("Quilometragem (km)", min_odo, max_odo, (min_odo, max_odo))

        with col2:
            filtered_models = df["model"].unique() if make1 == "Todos" else df[df["make"] == make1]["model"].unique()
            veiculo1 = st.selectbox("Modelo", options=["Todos"] + filtered_models.tolist(), index=0)
            trim = st.selectbox("Versão (Trim)", options=["Todos"] + df["trim"].unique().tolist(), index=0)
            condicao = st.selectbox("Condição", options=["Todos"] + df["condition"].unique().tolist(), index=0)
            cor_exterior = st.selectbox("Cor Exterior", options=["Todos"] + df["color"].unique().tolist(), index=0)

        with col3:
            state = st.selectbox("Estado", options=["Selecione o Estado"] + df["state"].unique().tolist(), index=0)
            transmissao = st.selectbox("Transmissão", options=["Todos"] + df["transmission"].unique().tolist(), index=0)
            interior = st.selectbox("Cor Interior", options=["Todos"] + df["interior"].unique().tolist(), index=0)
            vendedor = st.selectbox("Vendedor", options=["Todos"] + df["seller"].unique().tolist(), index=0)

        min_price, max_price = int(df["sellingprice"].min()), int(df["sellingprice"].max())
        sellingprice_range = st.slider("Preço de Venda (intervalo)", min_price, max_price, (min_price, max_price))

        submitted = st.form_submit_button("Aplicar Filtros")

    df_filtered = df.copy()

    if submitted:
        if make1 != "Todos":
            df_filtered = df_filtered[df_filtered["make"] == make1]
        if veiculo1 != "Todos":
            df_filtered = df_filtered[df_filtered["model"] == veiculo1]
        if body != "Todos":
            df_filtered = df_filtered[df_filtered["body"] == body]
        if trim != "Todos":
            df_filtered = df_filtered[df_filtered["trim"] == trim]
        if state != "Selecione o Estado":
            df_filtered = df_filtered[df_filtered["state"] == state]
        if transmissao != "Todos":
            df_filtered = df_filtered[df_filtered["transmission"] == transmissao]
        if condicao != "Todos":
            df_filtered = df_filtered[df_filtered["condition"] == condicao]
        if cor_exterior != "Todos":
            df_filtered = df_filtered[df_filtered["color"] == cor_exterior]
        if interior != "Todos":
            df_filtered = df_filtered[df_filtered["interior"] == interior]
        if vendedor != "Todos":
            df_filtered = df_filtered[df_filtered["seller"] == vendedor]

        df_filtered = df_filtered[(df_filtered["year"] >= year_range[0]) & (df_filtered["year"] <= year_range[1])]
        df_filtered = df_filtered[(df_filtered["mmr"] >= odometer[0]) & (df_filtered["mmr"] <= odometer[1])]
        df_filtered = df_filtered[(df_filtered["sellingprice"] >= sellingprice_range[0]) &
                                  (df_filtered["sellingprice"] <= sellingprice_range[1])]

    total_cars = len(df_filtered)
    total_pages = max(1, math.ceil(total_cars / cars_per_page))
    page = st.number_input("Página", min_value=1, max_value=total_pages, value=1, step=1) - 1
    start_idx = page * cars_per_page
    end_idx = start_idx + cars_per_page

    st.write("### 🚗 Veículos Disponíveis")

    if total_cars == 0:
        st.warning("⚠️ Nenhum veículo encontrado com os filtros selecionados.")
    else:
        imagens_carros = {
            "Kia Sorento": "https://cdn.jornaldenegocios.pt/images/2015-05/img_1280x720$2015_05_21_14_48_00_253987.jpg",
        }

        for index, row in df_filtered.iloc[start_idx:end_idx].iterrows():
            with st.container():
                st.markdown("---")
                col1, col2 = st.columns([1, 2])

                car_key = f"{row['make']} {row['model']}"
                car_image = imagens_carros.get(car_key,
                    "https://img.freepik.com/free-vector/404-error-background-with-car-wheel-flat-style_23-2147761283.jpg")

                with col1:
                    st.image(car_image, width=250)

                with col2:
                    st.write(f"**{row['make']} {row['model']} ({row['year']})**")
                    st.write(f"📍 Estado: {row['state']} | ⚙️ Transmissão: {row['transmission']} | 🎨 Cor: {row['color']}")
                    st.write(f"📌 Condição: {row['condition']} | ⏳ Km: {row['mmr']} km")
                    st.write(f"💰 Preço: **{row['sellingprice']} €**")

                    with st.expander(f"Calcular Importação - {row['make']} {row['model']} (ID: {index})"):
                        valid_state = state if state in states_data else row["state"]

                        if valid_state in states_data:
                            total_cost, tax_amount, iva_amount, import_days = calculate_import_cost(
                                valid_state, row["sellingprice"])
                            arrival_date = datetime.now() + timedelta(days=import_days)

                            st.write(f"🛒 **Preço Base:** {row['sellingprice']} €")
                            st.write(f"🏛 **Taxa Estadual ({valid_state} - {states_data[valid_state]['tax'] * 100}%):** {tax_amount:.2f} €")
                            st.write(f"🇵🇹 **IVA Portugal (23%):** {iva_amount:.2f} €")
                            st.write(f"🏢 **Taxa da Empresa:** {company_fee} €")
                            st.write(f"💰 **Custo Total de Importação:** {total_cost:.2f} €")
                            st.write(f"📆 **Tempo estimado de entrega:** {import_days} dias")
                            st.write(f"📅 **Data estimada de chegada:** {arrival_date.strftime('%Y-%m-%d')}")

                            if st.button(f"Ir para cálculo detalhado (ID: {index})"):
                                st.session_state.calculo_detalhado = True
                                st.session_state.carro_selecionado = row
                                st.rerun()      
                        else:
                            st.warning("⚠️ Selecione um estado válido para calcular os custos.")

# Renderização condicional
if st.session_state.calculo_detalhado:
    mostrar_calculo_detalhado()
else:
    mostrar()
