import streamlit as st
import base64

# Lê a imagem e converte para base64
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_b64 = get_base64_image("imagens/Carlogo.png")

# Lê o HTML
with open("app.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# Substitui o {{logo}} pelo base64
html_filled = html_template.replace("{{logo}}", logo_b64)

# Mostra no app
st.markdown(html_filled, unsafe_allow_html=True)
