import streamlit as st
import pandas as pd
import carrega_dados  # tua função personalizada
df = carrega_dados.carregar_dados()

def main():

    st.title("Comparação Avançada de Veículos")
    st.subheader("🔍 Filtros para Selecionar os Veículos")
    col1, col2 = st.columns(2)

    with col1:
        make1 = st.selectbox("Marca (1º Veículo)", sorted(df["make"].dropna().unique()), key="make1")

        modelos1_disponiveis = df[df["make"] == make1]["model"].dropna().unique()
        veiculo1 = st.selectbox("Modelo (1º Veículo)", sorted(modelos1_disponiveis), key="modelo1")

        estados1_disponiveis = df[(df["make"] == make1) & (df["model"] == veiculo1)]["state"].dropna().unique()
        estado1 = st.selectbox("Estado (1º Veículo)", sorted(estados1_disponiveis), key="estado1")

        # Filtragem acumulada até aqui
        df_filtrado = df[(df["make"] == make1) & (df["model"] == veiculo1) & (df["state"] == estado1)]

        # Ano do carro
        anos_disponiveis = df_filtrado["year"].dropna().unique()
        ano1 = st.selectbox("Ano (1º Veículo)", sorted(anos_disponiveis, reverse=True), key="ano1")

        # Quilometragem
        km_disponiveis = df_filtrado[df_filtrado["year"] == ano1]["odometer"].dropna().unique()
        km1 = st.selectbox("Quilometragem (1º Veículo)", sorted(km_disponiveis), key="km1")

        # Interior
        interior_disponivel = df_filtrado[df_filtrado["year"] == ano1]["interior"].dropna().unique()
        interior1 = st.selectbox("Interior (1º Veículo)", sorted(interior_disponivel), key="interior1")

        # Cor do carro
        cores_disponiveis = df_filtrado[df_filtrado["year"] == ano1]["color"].dropna().unique()
        cor1 = st.selectbox("Cor (1º Veículo)", sorted(cores_disponiveis), key="cor1")

    with col2:
        make2 = st.selectbox("Marca (2º Veículo)", sorted(df["make"].dropna().unique()), key="make2")

        modelos2_disponiveis = df[df["make"] == make2]["model"].dropna().unique()
        veiculo2 = st.selectbox("Modelo (2º Veículo)", sorted(modelos2_disponiveis), key="modelo2")

        estados2_disponiveis = df[(df["make"] == make2) & (df["model"] == veiculo2)]["state"].dropna().unique()
        estado2 = st.selectbox("Estado (2º Veículo)", sorted(estados2_disponiveis), key="estado2")

        # Filtragem acumulada até aqui
        df_filtrado2 = df[(df["make"] == make2) & (df["model"] == veiculo2) & (df["state"] == estado2)]

        # Ano do carro
        anos2_disponiveis = df_filtrado2["year"].dropna().unique()
        ano2 = st.selectbox("Ano (2º Veículo)", sorted(anos2_disponiveis, reverse=True), key="ano2")

        # Quilometragem
        km2_disponiveis = df_filtrado2[df_filtrado2["year"] == ano2]["odometer"].dropna().unique()
        km2 = st.selectbox("Quilometragem (2º Veículo)", sorted(km2_disponiveis), key="km2")

        # Interior
        interior2_disponivel = df_filtrado2[df_filtrado2["year"] == ano2]["interior"].dropna().unique()
        interior2 = st.selectbox("Interior (2º Veículo)", sorted(interior2_disponivel), key="interior2")

        # Cor do carro
        cores2_disponiveis = df_filtrado2[df_filtrado2["year"] == ano2]["color"].dropna().unique()
        cor2 = st.selectbox("Cor (2º Veículo)", sorted(cores2_disponiveis), key="cor2")


    comparar = st.button("Comparar Veículos")

    if comparar:
        filtro1 = df[(df["make"] == make1) & (df["model"] == veiculo1) & (df["state"] == estado1)]
        filtro2 = df[(df["make"] == make2) & (df["model"] == veiculo2) & (df["state"] == estado2)]

        if filtro1.empty or filtro2.empty:
            st.error("⚠️ Um dos filtros não retornou resultados. Ajuste os critérios.")
            return

        dados_veiculo1 = filtro1.iloc[0]
        dados_veiculo2 = filtro2.iloc[0]

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


        # Obter as chaves para os carros com base nas informações do dicionário
        car_key1 = f"{dados_veiculo1['make']} {dados_veiculo1['model']}"
        car_key2 = f"{dados_veiculo2['make']} {dados_veiculo2['model']}"

        # Buscar as imagens usando as chaves
        imagem1 = imagens_carros.get(car_key1, "https://img.freepik.com/free-vector/404-error-background-with-car-wheel-flat-style_23-2147761283.jpg")
        imagem2 = imagens_carros.get(car_key2, "https://img.freepik.com/free-vector/404-error-background-with-car-wheel-flat-style_23-2147761283.jpg")

        col1, col2 = st.columns(2)
        with col1:
            st.image(imagem1, caption="Imagem do carro", use_container_width=True)
            st.subheader(f"{dados_veiculo1['make']} {dados_veiculo1['model']}")
            st.write(f"📅 Ano: {dados_veiculo1['year']}")
            st.write(f"⚙️ Trim: {dados_veiculo1['trim']}")
            st.write(f"🚗 Categoria: {dados_veiculo1['body']}")
            st.write(f"🔄 Caixa: {dados_veiculo1['transmission']}")
            st.write(f"📍 Estado: {dados_veiculo1['state']}")
            st.write(f"📌 Condição: {dados_veiculo1['condition']}")
            st.write(f"⏳ Km: {dados_veiculo1['mmr']}")
            st.write(f"🎨 Cor: {dados_veiculo1['color']}")
            st.subheader(f"💰 Preço: {dados_veiculo1['sellingprice']} €")

        with col2:
            st.image(imagem2, caption="Imagem do carro", use_container_width=True)
            st.subheader(f"{dados_veiculo2['make']} {dados_veiculo2['model']}")
            st.write(f"📅 Ano: {dados_veiculo2['year']}")
            st.write(f"⚙️ Trim: {dados_veiculo2['trim']}")
            st.write(f"🚗 Categoria: {dados_veiculo2['body']}")
            st.write(f"🔄 Caixa: {dados_veiculo2['transmission']}")
            st.write(f"📍 Estado: {dados_veiculo2['state']}")
            st.write(f"📌 Condição: {dados_veiculo2['condition']}")
            st.write(f"⏳ Km: {dados_veiculo2['mmr']}")
            st.write(f"🎨 Cor: {dados_veiculo2['color']}")
            st.subheader(f"💰 Preço: {dados_veiculo2['sellingprice']} €")

        st.markdown("---")
        st.subheader("📊 Comparação de Destaques")

        if dados_veiculo1["sellingprice"] < dados_veiculo2["sellingprice"]:
            st.success(f'💸 **{dados_veiculo1["make"]} {dados_veiculo1["model"]}** é mais barato.')
        else:
            st.success(f'💸 **{dados_veiculo2["make"]} {dados_veiculo2["model"]}** é mais barato.')

        if dados_veiculo1["year"] > dados_veiculo2["year"]:
            st.success(f'⏳ **{dados_veiculo1["make"]} {dados_veiculo1["model"]}** é mais recente.')
        else:
            st.success(f'⏳ **{dados_veiculo2["make"]} {dados_veiculo2["model"]}** é mais recente.')

        if dados_veiculo1["odometer"] < dados_veiculo2["odometer"]:
            st.info(f'⛽ **{dados_veiculo1["make"]} {dados_veiculo1["model"]}** tem menos quilometragem.')
        else:
            st.info(f'⛽ **{dados_veiculo2["make"]} {dados_veiculo2["model"]}** tem menos quilometragem.')

        if dados_veiculo1["condition"] < dados_veiculo2["condition"]:
            st.info(f'⭐ **{dados_veiculo1["make"]} {dados_veiculo1["model"]}** tem uma melhor avaliação.')
        else:
            st.info(f'⭐ **{dados_veiculo2["make"]} {dados_veiculo2["model"]}** tem uma melhor avaliação.')
        st.caption("🔎 Dados extraídos com base nos filtros e na base disponível.")

if __name__ == "__main__":
    main()
