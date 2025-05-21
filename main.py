import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Dashboard")


# CSS: oculta sidebar e estiliza menu horizontal
st.markdown("""
    <style>
        /* Esconde o cabeçalho superior do Streamlit */
        header[data-testid="stHeader"] {
            background: transparent;
            height: 0px;
            visibility: hidden;
        }

        /* Esconde o rodapé (opcional) */
        footer {
            visibility: hidden;
        }

        /* Esconde a sidebar completamente */
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none !important;
            display: none !important;

        }

        /* Remove espaços extras do layout */
        .block-container {
            padding-top: 1rem;
        }

        /* Estiliza a barra horizontal (option_menu) */
        .css-1d391kg {
            background-color: #1e1e1e !important;
            padding: 0.5rem 1rem;
            border-radius: 0px !important;
        }

        .nav-link {
            color: white !important;
            font-weight: 500;
        }

        .nav-link.active {
            background-color: #ff4b4b !important;
            color: white !important;
            border-radius: 8px;
        }

        .nav-item {
            margin-right: 1rem;
        }
    </style>
""", unsafe_allow_html=True)


if "redirect_to" in st.session_state:
    redirect_page = st.session_state.redirect_to
    del st.session_state.redirect_to
    page = redirect_page
else:
    page = None

if page is None:
    page = option_menu(
        menu_title=None,
        options=["Quem Somos","Veículos Disponíveis", "Comparar Carros", "Dashboard","Análise Macro","Machine Learning"],
        icons=["house", "car-front", "person", "bar-chart","bar-chart","bar-chart"],
        orientation="horizontal",
        default_index=0,
        key="menu"
    )

# Navegação
if page == "Quem Somos":
    from pages import Quem_Somos
    Quem_Somos.main()
elif page == "Comparar Carros":
    from pages import Comparar_Carros
    Comparar_Carros.main()
elif page == "Dashboard":
    from pages import Dashboard
    Dashboard.main()
elif page == "Veículos Disponíveis":
    from pages import Veiculos_Disponiveis
    Veiculos_Disponiveis.main()
elif page == "Análise Macro":
    from pages import Analise_Macro
    Analise_Macro.main()
elif page == "Machine Learning":
    from pages import Teste
    Teste.main()



