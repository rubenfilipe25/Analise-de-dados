import streamlit as st
from PIL import Image
from email.message import EmailMessage
import smtplib

def enviar_email(nome, email_remetente, assunto, mensagem):
    email_destino = "rubenfilipesilva25@gmail.com"  # Substitui pelo e-mail para onde queres receber as mensagens
    email_utilizador = "jornadas.egi.upt@gmail.com"  # Substitui pelo teu e-mail de envio
    senha_aplicacao = "jnkw nsry yfqc rmlo"     # Substitui pela tua senha de aplicação

    msg = EmailMessage()
    msg["Subject"] = f"[AutoImport] {assunto}"
    msg["From"] = email_utilizador
    msg["To"] = email_destino

    corpo = f"""
    Nova mensagem através do formulário de contacto:

    Nome: {nome}
    Email: {email_remetente}
    Assunto: {assunto}

    Mensagem:
    {mensagem}
    """
    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_utilizador, senha_aplicacao)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Ocorreu um erro ao enviar o e-mail: {e}")
        return False

def main():
    imagem = Image.open("Imagens/Carlogo.png")

    st.markdown(
        """
        <style>
        .logo-container img {
            max-height: 90px;
            width: 100%;
            object-fit: contain;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(imagem, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")


    # Página de Apresentação

    st.header("Quem Somos")
    st.markdown("""
    Somos a **AutoImport Portugal**, uma empresa dedicada à importação de veículos dos Estados Unidos para Portugal. Oferecemos aos nossos clientes uma ampla variedade de automóveis para diferentes necessidades e orçamentos.

    Importamos desde veículos económicos a modelos desportivos, clássicos e utilitários, garantindo um serviço completo e eficiente para que cada cliente encontre a solução mais adequada.

    Com uma equipa experiente e um processo de aquisição transparente, asseguramos todas as etapas da importação, incluindo a pesquisa, compra, transporte e legalização do veículo, permitindo que o receba em Portugal sem qualquer preocupação.
    """)

    # Secção: Serviços
    st.header("O que Oferecemos")
    st.markdown("""
    Através do nosso website, é possível consultar as opções disponíveis nos Estados Unidos e, de forma simples e segura, iniciar o processo de compra.

    Após a confirmação, encarregamo-nos de toda a logística, assegurando que o automóvel chega ao destino com total conformidade legal e em perfeitas condições.

    A transparência e a confiança são princípios fundamentais da nossa atividade. Por esse motivo, estamos sempre disponíveis para esclarecer qualquer questão e garantir um acompanhamento rigoroso em todo o processo de importação.
    """)

    # Secção: História
    st.header("A Nossa História")
    st.markdown("""
    A **AutoImport Portugal** nasceu há 3 anos, com sede inicial na **Universidade Portucalense**, fruto da visão empreendedora dos seus fundadores **Rúben Almeida, Vasco Martins** e **Joana Barbosa**.

    A empresa surgiu com o propósito de simplificar e profissionalizar o processo de importação automóvel, inicialmente focando-se em veículos com elevada procura e excelente relação qualidade-preço.

    Desde então, a AutoImport Portugal tem vindo a crescer, consolidando a sua reputação no mercado nacional como uma referência em confiança, eficiência e compromisso com o cliente.

    Hoje, operamos a partir da nossa sede no **Porto**, na **Rua Dr. António Bernardino de Almeida**, continuando a inovar e a prestar um serviço diferenciado e adaptado às exigências dos nossos clientes.
    """)


    st.markdown("---")
    st.header("Contacte-nos")
    with st.form("formulario_contacto"):
        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        assunto = st.text_input("Assunto")
        mensagem = st.text_area("Mensagem")
        enviado = st.form_submit_button("Enviar")

        if enviado:
            if nome and email and mensagem:
                if enviar_email(nome, email, assunto, mensagem):
                    st.success("A sua mensagem foi enviada com sucesso! Entraremos em contacto brevemente.")
            else:
                st.warning("Por favor, preencha todos os campos obrigatórios.")

    st.markdown("---")
    st.caption("© 2025 AutoImport Portugal. Todos os direitos reservados.")

if __name__ == "__main__":
    main()
