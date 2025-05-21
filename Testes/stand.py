
import streamlit as st
import math
from datetime import datetime, timedelta
import carrega_dados  # Certifica-te que esse módulo existe

# --- Dados base ---
df = carrega_dados.carregar_dados()

states_data = {
    "ca": {"tax": 0.08, "days": 10}, "tx": {"tax": 0.06, "days": 7}, "pa": {"tax": 0.07, "days": 9},
    "mn": {"tax": 0.065, "days": 8}, "az": {"tax": 0.056, "days": 7}, "wi": {"tax": 0.05, "days": 6},
    "tn": {"tax": 0.07, "days": 8}, "md": {"tax": 0.06, "days": 7}, "fl": {"tax": 0.07, "days": 8},
    "ne": {"tax": 0.055, "days": 7}, "nj": {"tax": 0.066, "days": 9}, "nv": {"tax": 0.0685, "days": 7},
    "oh": {"tax": 0.0575, "days": 8}, "mi": {"tax": 0.06, "days": 7}, "ga": {"tax": 0.04, "days": 6},
    "va": {"tax": 0.053, "days": 7}, "sc": {"tax": 0.06, "days": 8}, "nc": {"tax": 0.0475, "days": 7},
    "in": {"tax": 0.07, "days": 9}, "il": {"tax": 0.0625, "days": 7}, "co": {"tax": 0.029, "days": 5},
    "ut": {"tax": 0.0485, "days": 6}, "mo": {"tax": 0.04225, "days": 7}, "ny": {"tax": 0.09, "days": 12},
    "ma": {"tax": 0.0625, "days": 9}, "pr": {"tax": 0.115, "days": 10}, "or": {"tax": 0.0, "days": 5},
    "la": {"tax": 0.0445, "days": 6}, "wa": {"tax": 0.065, "days": 8}, "hi": {"tax": 0.04, "days": 7},
    "qc": {"tax": 0.09975, "days": 14}, "ab": {"tax": 0.05, "days": 10}, "on": {"tax": 0.13, "days": 15},
    "ok": {"tax": 0.045, "days": 7}, "ms": {"tax": 0.07, "days": 8}, "nm": {"tax": 0.05125, "days": 6},
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
    return None, None, None, None


# ------------------------- MOSTRAR ABA PRINCIPAL -------------------------
def mostrar():
    st.title("📦 Importação de Veículos")

    # Inicializa a aba
    if "aba" not in st.session_state:
        st.session_state.aba = "Listagem de Carros"

    aba_selecionada = st.radio("🔁 Navegar:", ["Listagem de Carros", "Cálculo Detalhado"],
                               index=["Listagem de Carros", "Cálculo Detalhado"].index(st.session_state.aba))

    st.session_state.aba = aba_selecionada

    if aba_selecionada == "Listagem de Carros":
        mostrar_listagem()
    elif aba_selecionada == "Cálculo Detalhado":
        mostrar_calculo_detalhado()


# ------------------------- ABA 1: LISTAGEM DE CARROS -------------------------
def mostrar_listagem():
    st.subheader("🚗 Lista de Carros")

    # Simples filtro por estado para este exemplo
    state = st.selectbox("Escolher estado:", ["Selecione"] + sorted(df["state"].unique().tolist()))

    df_filtrado = df.copy()
    if state != "Selecione":
        df_filtrado = df_filtrado[df_filtrado["state"] == state]

    total = len(df_filtrado)
    pagina = st.number_input("Página", min_value=1, max_value=max(1, math.ceil(total / cars_per_page)), step=1)
    inicio = (pagina - 1) * cars_per_page
    fim = inicio + cars_per_page


    for i, row in df_filtrado.iloc[inicio:fim].iterrows():
        with st.expander(f"{row['make']} {row['model']} ({row['year']}) - {row['sellingprice']} €"):
            st.write(f"📍 Estado: {row['state']} | Cor: {row['color']}")
            st.write(f"Condição: {row['condition']} | Transmissão: {row['transmission']}")
            st.write(f"Km: {row['mmr']}")

            if st.button("🔍 Cálculo Detalhado", key=f"btn_{i}"):
                st.session_state.carro_selecionado = {
                    "make": row["make"],
                    "model": row["model"],
                    "price": row["sellingprice"],
                    "state": row["state"],
                    "year": row["year"]
                }
                st.session_state.aba = "Cálculo Detalhado"
                st.rerun()


# ------------------------- ABA 2: CÁLCULO DETALHADO -------------------------
def mostrar_calculo_detalhado():
    carro = st.session_state.get("carro_selecionado")

    if not carro:
        st.warning("⚠️ Nenhum carro selecionado. Volte à listagem e escolha um carro.")
        return

    st.subheader(f"📋 Cálculo para {carro['make']} {carro['model']} ({carro['year']})")

    total_cost, tax_amount, iva_amount, import_days = calculate_import_cost(
        carro["state"], carro["price"]
    )

    if total_cost is None:
        st.error("Erro ao calcular. Estado inválido.")
        return

    chegada = datetime.now() + timedelta(days=import_days)

    st.write(f"🛒 Preço Base: **{carro['price']} €**")
    st.write(f"🏛 Taxa Estadual ({carro['state']}): **{tax_amount:.2f} €**")
    st.write(f"🇵🇹 IVA Portugal (23%): **{iva_amount:.2f} €**")
    st.write(f"🏢 Taxa da Empresa: **{company_fee} €**")
    st.success(f"💰 Custo Total: **{total_cost:.2f} €**")
    st.info(f"📆 Entrega em cerca de **{import_days} dias** — Chegada estimada: **{chegada.strftime('%Y-%m-%d')}**")

    if st.button("🔙 Voltar à Lista"):
        st.session_state.aba = "Listagem de Carros"
        st.rerun()