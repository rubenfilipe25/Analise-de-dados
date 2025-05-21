import streamlit as st
import math
import io
from PIL import Image
from datetime import datetime, timedelta
import carrega_dados
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
)

# Estilos base
styles = getSampleStyleSheet()

# Estilo de título centralizado
heading_centered = ParagraphStyle(
    name='HeadingCentered',
    parent=styles['Heading1'],
    alignment=TA_CENTER,
    fontSize=14,
    leading=16,
    textColor=colors.HexColor('#003366'),
    spaceAfter=12,
)

# --- Dados base ---
df = carrega_dados.carregar_dados()





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


# Estados e taxas
states_data = {
    "ca": {"tax": 0.08, "days": 30}, "tx": {"tax": 0.06, "days": 24}, "pa": {"tax": 0.024, "days": 21},
    "mn": {"tax": 0.065, "days": 25}, "az": {"tax": 0.056, "days": 24}, "wi": {"tax": 0.05, "days": 30},
    "tn": {"tax": 0.024, "days": 25}, "md": {"tax": 0.06, "days": 24}, "fl": {"tax": 0.07, "days": 25},
    "ne": {"tax": 0.055, "days": 33}, "nj": {"tax": 0.066, "days": 21}, "nv": {"tax": 0.06255, "days": 33},
    "oh": {"tax": 0.05335, "days": 25}, "mi": {"tax": 0.06, "days": 33}, "ga": {"tax": 0.04, "days": 16},
    "va": {"tax": 0.053, "days": 33}, "sc": {"tax": 0.06, "days": 25}, "nc": {"tax": 0.04335, "days": 33},
    "in": {"tax": 0.033, "days": 21}, "il": {"tax": 0.0625, "days": 33}, "co": {"tax": 0.0221, "days": 11},
    "ut": {"tax": 0.04211, "days": 21}, "mo": {"tax": 0.04225, "days": 33}, "ny": {"tax": 0.021, "days": 12},
    "ma": {"tax": 0.02125, "days": 21}, "pr": {"tax": 0.115, "days": 30}, "or": {"tax": 0.0, "days": 13},
    "la": {"tax": 0.0445, "days": 21}, "wa": {"tax": 0.0215, "days": 25}, "hi": {"tax": 0.04, "days": 33},
    "qc": {"tax": 0.0219335, "days": 14}, "ab": {"tax": 0.05, "days": 30}, "on": {"tax": 0.13, "days": 15},
    "ok": {"tax": 0.045, "days": 33}, "ms": {"tax": 0.033, "days": 25}, "nm": {"tax": 0.05125, "days": 21},
    "al": {"tax": 0.04, "days": 33}
}




company_fee = 500
iva_portugal = 0.23
cars_per_page = 10

# Inicializa estado de sessão
if "aba" not in st.session_state:
    st.session_state.aba = "Listagem de Carros"
if "carro_selecionado" not in st.session_state:
    st.session_state.carro_selecionado = None
    


def calculate_import_cost(state, car_price):
    if state in states_data:
        state_tax = states_data[state]["tax"]
        tax_amount = car_price * state_tax
        iva_amount = car_price * iva_portugal
        total_cost = car_price + tax_amount + iva_amount + company_fee
        return total_cost, tax_amount, iva_amount, states_data[state]["days"]
    return None, None, None, None


# Informações da empresa
empresa_nome = "AutoImport Portugal "
empresa_endereco = " Rua Dr. António Bernardino de Almeida, 541 4200-072 Porto - Portugal"
empresa_telefone = "+351 919 999 999"
empresa_email = "AutoImportPortugal@gmai.com"
empresa_logo_url = "Imagens/Carlogo.png"


def gerar_pdf(carro):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=36, bottomMargin=36)
    content = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=18, alignment=1, spaceAfter=12, textColor=colors.HexColor("#003366"))
    heading_style = ParagraphStyle('HeadingCustom', parent=styles['Heading2'], fontSize=13, leading=16, textColor=colors.HexColor("#003366"), spaceAfter=12)
    normal_style = ParagraphStyle('NormalCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, spaceAfter=6)
    small_centered = ParagraphStyle('SmallCentered', parent=styles['Normal'], fontSize=9, alignment=1, textColor=colors.HexColor("#444444"))

    # Logo
    try:
        logo = Image(empresa_logo_url, width=2.5 * inch, height=1 * inch)
        logo.hAlign = 'CENTER'
        content.append(logo)
    except:
        content.append(Paragraph("Logo não disponível", normal_style))

    content.append(Spacer(1, 8))
    content.append(Paragraph(f"<b>{empresa_nome}</b>", title_style))
    content.append(Paragraph(f"{empresa_endereco}<br/>{empresa_telefone} | {empresa_email}", normal_style))
    content.append(Spacer(1, 10))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    content.append(Spacer(1, 18))

    # Seção: Informações do Carro
    content.append(Paragraph("Informações do Carro", heading_centered))


    carro_info = [
        [Paragraph("<b>Marca:</b>", normal_style), Paragraph(str(carro.get('make', 'N/A')), normal_style)],
        [Paragraph("<b>Modelo:</b>", normal_style), Paragraph(str(carro.get('model', 'N/A')), normal_style)],
        [Paragraph("<b>Ano:</b>", normal_style), Paragraph(str(carro.get('year', 'N/A')), normal_style)],
        [Paragraph("<b>Cor:</b>", normal_style), Paragraph(str(carro.get('color', 'N/A')), normal_style)],
        [Paragraph("<b>Kilometragem:</b>", normal_style), Paragraph(f"{carro.get('mmr', 0):,.0f} km", normal_style)],
        [Paragraph("<b>Transmissão:</b>", normal_style), Paragraph(str(carro.get('transmission', 'N/A')), normal_style)],
        [Paragraph("<b>Condição:</b>", normal_style), Paragraph(str(carro.get('condition', 'N/A')), normal_style)],
        [Paragraph("<b>Preço de Venda:</b>", normal_style), Paragraph(f"{carro.get('sellingprice', 0):,.2f} €", normal_style)],
    ]

    table = Table(carro_info, hAlign='CENTER', colWidths=[2.5 * inch, 2.5 * inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(table)
    content.append(Spacer(1, 24))

    # Seção: Cálculo de Importação
    content.append(Paragraph("Cálculo de Importação", heading_centered))

    total_cost, tax_amount, iva_amount, import_days = calculate_import_cost(
        carro["state"], float(carro.get("sellingprice", 0))
    )
    chegada = datetime.now() + timedelta(days=import_days)

    import_data = [
        [Paragraph("<b>Preço Base:</b>", normal_style), f"{carro.get('sellingprice', 0):,.2f} €"],
        [Paragraph(f"<b>Taxa Estadual ({carro['state']}):</b>", normal_style), f"{tax_amount:,.2f} €"],
        [Paragraph("<b>IVA Portugal (23%):</b>", normal_style), f"{iva_amount:,.2f} €"],
        [Paragraph("<b>Taxa da Empresa:</b>", normal_style), f"{company_fee:,.2f} €"],
        [Paragraph("<b>Custo Total de Importação:</b>", normal_style), f"{total_cost:,.2f} €"],
        [Paragraph("<b>Entrega Estimada:</b>", normal_style), chegada.strftime("%d/%m/%Y")],
    ]

    import_table = Table(import_data, hAlign='CENTER', colWidths=[2.5 * inch, 2.5 * inch])
    import_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(import_table)
    content.append(Spacer(1, 30))

    # Rodapé
    content.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"{empresa_nome} | {empresa_telefone} | {empresa_email}", small_centered))

    doc.build(content)
    buffer.seek(0)
    return buffer


def mostrar_calculo_detalhado():
    carro = st.session_state.get("carro_selecionado")

    # Verifica se o carro foi selecionado corretamente
    if carro is None or carro.empty:
        st.warning("⚠️ Nenhum carro selecionado. Volte à listagem e escolha um carro.")
        return

    # Cabeçalho com detalhes do carro
    st.markdown(f"## 📋 Detalhes do Cálculo: `{carro['make']} {carro['model']} ({carro['year']})`")

    # Calcula os custos de importação
    total_cost, tax_amount, iva_amount, import_days = calculate_import_cost(
        carro["state"], carro["sellingprice"]
    )

    # Verifica se o cálculo foi bem-sucedido
    if total_cost is None:
        st.error("❌ Erro ao calcular. Estado inválido.")
        return

    chegada = datetime.now() + timedelta(days=import_days)

    # Cria duas colunas
# Cria duas colunas
    col1, col2 = st.columns([2, 1])  # 2:1 ratio para dar mais espaço ao conteúdo

    with col1:
        st.markdown("### 💵 Custos Totais")
        st.write(f"• 🛒 **Preço Base:** `{carro['sellingprice']} €`")
        st.write(f"• 🏛 **Taxa Estadual ({carro['state']}):** `{tax_amount:.2f} €`")
        st.write(f"• 🇵🇹 **IVA Portugal (23%):** `{iva_amount:.2f} €`")
        st.write(f"• 🏢 **Taxa da Empresa:** `{company_fee} €`")

        st.markdown("---")
        st.success(f"💰 **Custo Total Estimado:** {total_cost:.2f} €")
        st.info(f"📦 **Entrega em aproximadamente:** `{import_days} dias 📅 Data Estimada de Chegada: {chegada.strftime('%Y-%m-%d')}")

    with col2:
        imagens_carros = {
        "Kia Sorento": "https://cdn.jornaldenegocios.pt/images/2015-05/img_1280x720$2015_05_21_14_48_00_253987.jpg",

        'BMW 3 Series': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5C1qb4d8NySH6ihw82AObr1CAqj3_sg830w&s',
        'Volvo S60': 'https://live.staticflickr.com/4847/31160916547_857678737c_o.jpg',
        'BMW 6 Series Gran Coupe': 'https://carwow-uk-wp-3.imgix.net/BMW-6-Series-Gran-Coupe-driving-front.jpg',
        'Nissan Altima': 'https://upload.wikimedia.org/wikipedia/commons/9/92/2019_Nissan_Altima_SR_AWD%2C_front_9.30.19.jpg',
        'BMW M5': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRq1knharO-QcGfcUKitodl-gwUCjlH73Qwxw&s',
        'Chevrolet Cruze': 'https://media.ed.edmunds-media.com/chevrolet/cruze/2013/oem/2013_chevrolet_cruze_sedan_2lt_fq_oem_1_1600.jpg',
        'Audi A4': 'https://upload.wikimedia.org/wikipedia/commons/7/7e/2018_Audi_A4_Sport_TDi_Quattro_S-A_2.0.jpg',
        'Chevrolet Camaro': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLyxu_5NDD-vJ9HV9zn-HLB9vkaEIsJa1SWw&s',
        'Audi A6': 'https://fleetmagazine.pt/wp-content/uploads/2019/04/audi-a6.jpg',
        'Kia Optima': 'https://www.razaoautomovel.com/wp-content/uploads/2016/10/Kia-Optima-Sportswagon-1-e1476439555145.jpg',
        'Ford Fusion': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPTfPT0wmCM7Pmhy1WA2esHetZJVrDh5aqBA&s',
        'Audi Q5': 'https://cdn.motor1.com/images/mgl/3W41Jx/s3/audi-q5-2024.jpg',
        'BMW 6 Series': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZSw2ViUSHPYIZesPzbX_gkI82gdTs4WjLqQ&s',
        'Chevrolet Impala': 'https://upload.wikimedia.org/wikipedia/commons/6/63/2014_Chevy_Impala_Europe.jpg',
        'BMW 5 Series': 'https://bmw.scene7.com/is/image/BMW/bmw-5-series-overview-g30?wid=3000&hei=3000',
        'Audi A3': 'https://www.razaoautomovel.com/wp-content/uploads/2024/06/AUDI-A3-SPORTBACK.webp',
        'Volvo XC70': 'https://ireland.apollo.olxcdn.com/v1/files/280p16li3vvz1-PT/image;s=1008x567',
        'Audi SQ5': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsaqAXgNW9g76SuLnb4LGonybFSAC_W6gRNA&s',
        'Audi S5': 'https://upload.wikimedia.org/wikipedia/commons/7/7d/2018_Audi_S5_TFSi_Quattro_Automatic_3.0_Front.jpg',
        'Chevrolet Suburban': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/2015_Chevrolet_Suburban_1500_LTZ%2C_front_4.18.19.jpg/1200px-2015_Chevrolet_Suburban_1500_LTZ%2C_front_4.18.19.jpg',
        'Cadillac ELR': 'https://upload.wikimedia.org/wikipedia/commons/7/79/2014_Cadillac_ELR_trimmed.jpg',
        'Volvo V60': 'https://feirauto.pt/wp-content/uploads/2021/07/V60_T6_2.jpg',
        'BMW X6': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ341AbkFRvUUTSVThctoeZh9P3ks4FVpBMQg&s',
        'Acura ILX': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQztuQVU4vBhngx3xBaCAqpHZnChRPv6Stw&s',
        'Kia K900': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlpIQB2NzwH5jagsAN9sWCp0CCiJtqi6VreQ&s',
        'Chevrolet Malibu': 'https://upload.wikimedia.org/wikipedia/commons/a/a2/2017_Chevrolet_Malibu_%28E2XX%29_front_3.25.18.jpg',
        'Lexus RX 350': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Lexus_RX_450h_F_Sport_%28IV%29_%E2%80%93_Frontansicht%2C_14._Februar_2016%2C_D%C3%BCsseldorf.jpg/1200px-Lexus_RX_450h_F_Sport_%28IV%29_%E2%80%93_Frontansicht%2C_14._Februar_2016%2C_D%C3%BCsseldorf.jpg',
        'Nissan Versa': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlO53TkrlSxhPKP9IHma9A_-pAmH9Ra69MJw&s',
        'Hyundai Elantra': 'https://upload.wikimedia.org/wikipedia/commons/a/ac/0_Hyundai_Avante_%28CN7%29_FL_2.jpg',
        'Nissan Versa Note': 'https://hips.hearstapps.com/hmg-prod/images/2015-nissan-versa-note-sr-mmp-1-1557254081.jpg',
        'Audi A8': 'https://upload.wikimedia.org/wikipedia/commons/3/31/2018_Audi_A8_50_TDi_Quattro_Automatic_3.0.jpg',
        'BMW X1': 'https://mediapool.bmwgroup.com/cache/P9/202205/P90465697/P90465697-the-first-ever-bmw-ix1-xdrive30-mineral-white-metallic-20-bmw-individual-styling-869i-05-22-2250px.jpg',
        'Audi TTS': 'https://upload.wikimedia.org/wikipedia/commons/f/f5/Audi_TT_Coup%C3%A9_2.0_TFSI_quattro_S-line_%288S%29_%E2%80%93_Frontansicht%2C_3._April_2015%2C_D%C3%BCsseldorf.jpg',
        'BMW 4 Series': 'https://connectingcars-pt.com/wp-content/uploads/2024/10/BMW-4-Series-Gran-Coupe-1024x768.jpeg',
        'Acura MDX': 'https://upload.wikimedia.org/wikipedia/commons/5/5b/2022_Acura_MDX_Technology%2C_front_7.2.22.jpg',
        'Chevrolet Silverado 1500': 'https://upload.wikimedia.org/wikipedia/commons/d/d0/2020_Chevrolet_Silverado_1500_High_Country%2C_front_10.25.20.jpg',
        'Cadillac SRX': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQydZwD9qg7tsL2JC0lkcvzMvOuEjefXmbsDw&s',
        'BMW X5': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/2019_BMW_X5_M50d_Automatic_3.0.jpg/1200px-2019_BMW_X5_M50d_Automatic_3.0.jpg'
    }

        car_key = f"{carro['make']} {carro['model']}"
        car_image = imagens_carros.get(
            car_key,
            "https://img.freepik.com/free-vector/404-error-background-with-car-wheel-flat-style_23-2147761283.jpg"
        )

        st.image(car_image, caption=car_key, use_container_width=True)


    # Adicionando botão para gerar o PDF
    if st.button("📄 Gerar PDF com Detalhes"):
        pdf_buffer = gerar_pdf(carro)
        st.download_button(
            label="Baixar PDF",
            data=pdf_buffer,
            file_name=f"{carro['make']}_{carro['model']}_{carro['year']}_detalhes.pdf",
            mime="application/pdf"
        )

    if st.button("🔙 Voltar aos Veículos Disponiveis"):
        st.session_state.aba = "Listagem de Carros"
        st.session_state.carro_selecionado = None
        st.rerun()
    st.markdown("---")
    st.caption("© 2025 AutoImport Portugal. Todos os direitos reservados.")




def mostrar():
    st.title(" Calculadora de Importação de Veículos")
    




    with st.form("filtros"):
        col1, col2, col3 = st.columns(3)

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


        # Siglas únicas no DataFrame
        state_abbrs = df["state"].unique().tolist()

        # Monta opções legíveis com nome + sigla
        state_display_map = {abbr: f"{state_names.get(abbr, abbr.upper())} ({abbr.upper()})" for abbr in state_abbrs}
        state_options_display = ["Selecione o Estado"] + [state_display_map[abbr] for abbr in state_abbrs]



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
            selected_display = st.selectbox("Estado", options=state_options_display, index=0)  # Corrigido para usar 'state_options_display'
            
            # Selectbox com opção padrão

            # Extrai sigla da opção selecionada (ou None)
            selected_state = None
            if selected_display != "Selecione o Estado":
                selected_state = selected_display.split("(")[-1].strip(")").lower()


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
        if selected_state != "Selecione o Estado":
            df_filtered = df_filtered[df_filtered["state"] == selected_state]
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

    imagens_carros = {
        "Kia Sorento": "https://cdn.jornaldenegocios.pt/images/2015-05/img_1280x720$2015_05_21_14_48_00_253987.jpg",
        'BMW 3 Series': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5C1qb4d8NySH6ihw82AObr1CAqj3_sg830w&s',
        'Volvo S60': 'https://live.staticflickr.com/4847/31160916547_857678737c_o.jpg',
        'BMW 6 Series Gran Coupe': 'https://carwow-uk-wp-3.imgix.net/BMW-6-Series-Gran-Coupe-driving-front.jpg',
        'Nissan Altima': 'https://upload.wikimedia.org/wikipedia/commons/9/92/2019_Nissan_Altima_SR_AWD%2C_front_9.30.19.jpg',
        'BMW M5': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRq1knharO-QcGfcUKitodl-gwUCjlH73Qwxw&s',
        'Chevrolet Cruze': 'https://media.ed.edmunds-media.com/chevrolet/cruze/2013/oem/2013_chevrolet_cruze_sedan_2lt_fq_oem_1_1600.jpg',
        'Audi A4': 'https://upload.wikimedia.org/wikipedia/commons/7/7e/2018_Audi_A4_Sport_TDi_Quattro_S-A_2.0.jpg',
        'Chevrolet Camaro': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLyxu_5NDD-vJ9HV9zn-HLB9vkaEIsJa1SWw&s',
        'Audi A6': 'https://fleetmagazine.pt/wp-content/uploads/2019/04/audi-a6.jpg',
        'Kia Optima': 'https://www.razaoautomovel.com/wp-content/uploads/2016/10/Kia-Optima-Sportswagon-1-e1476439555145.jpg',
        'Ford Fusion': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPTfPT0wmCM7Pmhy1WA2esHetZJVrDh5aqBA&s',
        'Audi Q5': 'https://cdn.motor1.com/images/mgl/3W41Jx/s3/audi-q5-2024.jpg',
        'BMW 6 Series': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZSw2ViUSHPYIZesPzbX_gkI82gdTs4WjLqQ&s',
        'Chevrolet Impala': 'https://upload.wikimedia.org/wikipedia/commons/6/63/2014_Chevy_Impala_Europe.jpg',
        'BMW 5 Series': 'https://bmw.scene7.com/is/image/BMW/bmw-5-series-overview-g30?wid=3000&hei=3000',
        'Audi A3': 'https://www.razaoautomovel.com/wp-content/uploads/2024/06/AUDI-A3-SPORTBACK.webp',
        'Volvo XC70': 'https://ireland.apollo.olxcdn.com/v1/files/280p16li3vvz1-PT/image;s=1008x567',
        'Audi SQ5': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsaqAXgNW9g76SuLnb4LGonybFSAC_W6gRNA&s',
        'Audi S5': 'https://upload.wikimedia.org/wikipedia/commons/7/7d/2018_Audi_S5_TFSi_Quattro_Automatic_3.0_Front.jpg',
        'Chevrolet Suburban': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/2015_Chevrolet_Suburban_1500_LTZ%2C_front_4.18.19.jpg/1200px-2015_Chevrolet_Suburban_1500_LTZ%2C_front_4.18.19.jpg',
        'Cadillac ELR': 'https://upload.wikimedia.org/wikipedia/commons/7/79/2014_Cadillac_ELR_trimmed.jpg',
        'Volvo V60': 'https://feirauto.pt/wp-content/uploads/2021/07/V60_T6_2.jpg',
        'BMW X6': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ341AbkFRvUUTSVThctoeZh9P3ks4FVpBMQg&s',
        'Acura ILX': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQztuQVU4vBhngx3xBaCAqpHZnChRPv6Stw&s',
        'Kia K900': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlpIQB2NzwH5jagsAN9sWCp0CCiJtqi6VreQ&s',
        'Chevrolet Malibu': 'https://upload.wikimedia.org/wikipedia/commons/a/a2/2017_Chevrolet_Malibu_%28E2XX%29_front_3.25.18.jpg',
        'Lexus RX 350': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Lexus_RX_450h_F_Sport_%28IV%29_%E2%80%93_Frontansicht%2C_14._Februar_2016%2C_D%C3%BCsseldorf.jpg/1200px-Lexus_RX_450h_F_Sport_%28IV%29_%E2%80%93_Frontansicht%2C_14._Februar_2016%2C_D%C3%BCsseldorf.jpg',
        'Nissan Versa': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlO53TkrlSxhPKP9IHma9A_-pAmH9Ra69MJw&s',
        'Hyundai Elantra': 'https://upload.wikimedia.org/wikipedia/commons/a/ac/0_Hyundai_Avante_%28CN7%29_FL_2.jpg',
        'Nissan Versa Note': 'https://hips.hearstapps.com/hmg-prod/images/2015-nissan-versa-note-sr-mmp-1-1557254081.jpg',
        'Audi A8': 'https://upload.wikimedia.org/wikipedia/commons/3/31/2018_Audi_A8_50_TDi_Quattro_Automatic_3.0.jpg',
        'BMW X1': 'https://mediapool.bmwgroup.com/cache/P9/202205/P90465697/P90465697-the-first-ever-bmw-ix1-xdrive30-mineral-white-metallic-20-bmw-individual-styling-869i-05-22-2250px.jpg',
        'Audi TTS': 'https://upload.wikimedia.org/wikipedia/commons/f/f5/Audi_TT_Coup%C3%A9_2.0_TFSI_quattro_S-line_%288S%29_%E2%80%93_Frontansicht%2C_3._April_2015%2C_D%C3%BCsseldorf.jpg',
        'BMW 4 Series': 'https://connectingcars-pt.com/wp-content/uploads/2024/10/BMW-4-Series-Gran-Coupe-1024x768.jpeg',
        'Acura MDX': 'https://upload.wikimedia.org/wikipedia/commons/5/5b/2022_Acura_MDX_Technology%2C_front_7.2.22.jpg',
        'Chevrolet Silverado 1500': 'https://upload.wikimedia.org/wikipedia/commons/d/d0/2020_Chevrolet_Silverado_1500_High_Country%2C_front_10.25.20.jpg',
        'Cadillac SRX': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQydZwD9qg7tsL2JC0lkcvzMvOuEjefXmbsDw&s',
        'BMW X5': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/2019_BMW_X5_M50d_Automatic_3.0.jpg/1200px-2019_BMW_X5_M50d_Automatic_3.0.jpg'
    }
    st.write("### 🚗 Veículos Disponíveis")
    if total_cars == 0:
        st.warning("⚠️ Nenhum veículo encontrado com os filtros selecionados.")
    else:
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

                    with st.expander("Calcular Importação"):
                        valid_state = row["state"]
                        total_cost, tax_amount, iva_amount, import_days = calculate_import_cost(
                            valid_state, row["sellingprice"])
                        arrival_date = datetime.now() + timedelta(days=import_days)

                        st.write(f"🛒 **Preço Base:** {row['sellingprice']} €")
                        st.write(f"🏛 **Taxa Estadual ({valid_state}):** {tax_amount:.2f} €")
                        st.write(f"🇵🇹 **IVA Portugal (23%):** {iva_amount:.2f} €")
                        st.write(f"🏢 **Taxa da Empresa:** {company_fee} €")
                        st.write(f"💰 **Custo Total de Importação:** {total_cost:.2f} €")
                        st.write(f"📅 **Data estimada de chegada:** {arrival_date.strftime('%Y-%m-%d')}")

                        if st.button(f"📊 Ver Detalhes do {row['make']} {row['model']}", key=f"det_{index}"):
                            st.session_state.carro_selecionado = row
                            st.session_state.aba = "Cálculo Detalhado"
                            st.rerun()
    st.markdown("---")
    st.caption("© 2025 AutoImport Portugal. Todos os direitos reservados.")



# Página principal
def main():


    # Inicializa o estado da aba, se não existir
    if "aba" not in st.session_state:
        st.session_state.aba = "Listagem de Carros"

    # Navegação entre abas usando st.radio
    aba_selecionada = st.radio(
        "🔁 Navegar:",
        ["Listagem de Carros", "Cálculo Detalhado"],
        index=["Listagem de Carros", "Cálculo Detalhado"].index(st.session_state.aba)
    )

    # Atualiza o estado da aba atual
    st.session_state.aba = aba_selecionada

    # Mostra o conteúdo conforme a aba ativa
    if aba_selecionada == "Listagem de Carros":
        mostrar()
    elif aba_selecionada == "Cálculo Detalhado":
        mostrar_calculo_detalhado()




if __name__ == "__main__":
    main()
