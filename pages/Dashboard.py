
import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as stats
import streamlit as st
import carrega_dados  # Importa função de carregamento de dados

# 🔹 Carregar os dados
df = carrega_dados.carregar_dados()

def main ():
    # 🔹 Lista das variáveis categóricas
    variaveis_categoricas = ["make", "model", "trim", "body", "transmission", "state", "color", "interior", "seller"]

    # 🔹 Configuração de layout do Streamlit com abas estilizadas
    st.markdown("""
        <style>
            /* Fundo da aplicação */
            .stApp {
                background-color: #f8f9fa;
            }

            /* Estilo das métricas */
            .stMetric {
                font-size: 22px;
                font-weight: bold;
                color: #333333;
            }

            /* Tabela */
            table {
                border-collapse: collapse;
                width: 100%;
            }

            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }

            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }

            /* Estilo customizado para as abas */
            .stTabs [data-baseweb="tab"] {
                font-size: 17px;
                color: #495057;
                background-color: #e9ecef;
                padding: 10px 20px;
                margin-right: 6px;
                border-radius: 10px 10px 0 0;
                border: 1px solid #dee2e6;
                transition: all 0.3s ease-in-out;
            }

            .stTabs [aria-selected="true"] {
                background-color: #ffffff;
                color: #d6336c;
                font-weight: 600;
                border-bottom: none;
                box-shadow: 0 -3px 0 #d6336c inset;
            }
        </style>
    """, unsafe_allow_html=True)

    # 🔸 Título da aplicação
    st.title("Dashboard de Análise de Vendas")

    # 🔹 Abas com títulos e ícones
    aba1, aba2, aba3 = st.tabs(["📈 Visão Geral", "📋 Análise Isolada", "🧮 Matriz Correlação"])

    # 🔹 Lista das variáveis categóricas
    variaveis_categoricas = ["make", "model", "trim", "body", "transmission", "state", "color", "interior", "seller"]

    with aba1:
        st.subheader("📋 Top Frequência")


        # Dicionário para traduzir os nomes das variáveis
        nomes_traduzidos = {
            "year": "Ano",
            "make": "Marca",
            "model": "Modelo",
            "trim": "Especificação",
            "body": "Segmento do Carro",
            "transmission": "Transmissão",
            "vin": "ID",
            "state": "Estado",
            "condition": "Condição do Carro",
            "odometer": "Kilometros do Carro",
            "color": "Cor do Carro",
            "interior": "Cor do Interior",
            "seller": "Vendedor",
            "mmr": "Valor de Mercado",
            "sellingprice": "Preço de Venda"
            # Adiciona mais conforme necessário
        }

        num_categorias = st.slider("Número de categorias", min_value=3, max_value=20, value=10)

        # Se ainda não existir o estado 'figs_para_pdf' em session_state, criamos uma lista vazia
        if 'figs_para_pdf' not in st.session_state:
            st.session_state.figs_para_pdf = []

        i = 0
        while i < len(variaveis_categoricas):
            if i == len(variaveis_categoricas) - 1:
                col = st.columns([0.7, 0.3])[0]
            else:
                col1, col2 = st.columns(2)

            for j, col in enumerate([col1, col2] if i < len(variaveis_categoricas) - 1 else [col]):
                if i + j < len(variaveis_categoricas):
                    variavel = variaveis_categoricas[i + j]
                    if variavel in df.columns:
                        frequencias = df[variavel].value_counts().head(num_categorias)
                        labels_curto = [x[:10] + "..." if len(x) > 10 else x for x in frequencias.index]

                        nome_exibido = nomes_traduzidos.get(variavel, variavel.capitalize())

                        with col:
                            st.subheader(f"📌 {nome_exibido}")

                            # 📌 Gráfico de donut para 'transmission'
                            if variavel == "transmission":
                                fig_donut = px.pie(
                                    values=frequencias.values,
                                    names=labels_curto,
                                    hole=0.5,
                                    title=f"Distribuição de {nome_exibido}",
                                    color_discrete_sequence=px.colors.qualitative.Prism
                                )
                                fig_donut.update_layout(
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                )
                                st.plotly_chart(fig_donut, use_container_width=True)
                                st.session_state.figs_para_pdf.append(fig_donut)  # Adiciona à lista de gráficos

                            else:
                                # 📊 Gráfico de barras
                                fig_bar = px.bar(
                                    x=labels_curto,
                                    y=frequencias.values,
                                    text=frequencias.values,
                                    labels={'x': nome_exibido, 'y': 'Frequência'},
                                    title=f"Top {num_categorias} categorias - {nome_exibido}",
                                    color=frequencias.index,
                                    color_discrete_sequence=px.colors.qualitative.Prism
                                )
                                fig_bar.update_traces(textposition='outside')
                                fig_bar.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color="black")
                                )
                                st.plotly_chart(fig_bar, use_container_width=True)
                                st.session_state.figs_para_pdf.append(fig_bar)  # Adiciona à lista de gráficos

            i += 2


        # Verificando se os gráficos foram gerados
        if not st.session_state.figs_para_pdf:
            st.warning("Nenhum gráfico foi gerado para o PDF.")  # Mensagem de aviso caso a lista esteja vazia
        st.markdown("---")
        st.caption("© 2025 AutoImport Portugal. Todos os direitos reservados.")


    # 🔹 ABA - Análise Estatística Profissional
    with aba2:

        # Mapeamento dos nomes das variáveis
        variable_names = {
            "year": "Ano",
            "make": "Marca",
            "model": "Modelo",
            "trim": "Especificação",
            "body": "Segmento do Carro",
            "transmission": "Transmissão",
            "vin": "ID",
            "state": "Estado",
            "condition": "Condição do Carro",
            "odometer": "Kilometros do Carro",
            "color": "Cor do Carro",
            "interior": "Cor do Interior",
            "seller": "Vendedor",
            "mmr": "Valor de Mercado",
            "sellingprice": "Preço de Venda"
        }

        # Reverter o dicionário para facilitar a tradução
        reverse_variable_names = {v: k for k, v in variable_names.items()}

        st.write("### 🔍 Análise Isolada de Variáveis")

        # Exibir o dropdown com os nomes amigáveis
        variable = st.selectbox(
            "Selecione uma variável para analisar",
            list(variable_names.values())
        )

        # Mapeia o nome amigável de volta para o nome real da coluna
        real_variable = reverse_variable_names[variable]

        # Descrições das variáveis
        descriptions = {
            "year": "📅 Representa o ano de fabrico do veículo, sendo um indicador crucial para determinar a idade, o valor de mercado e possíveis atualizações tecnológicas ou regulamentares associadas à sua produção.",
            "make": "🏭 Refere-se ao fabricante do veículo, identificando a empresa responsável pela sua criação. A marca pode transmitir valores relacionados à qualidade, inovação e reputação no mercado automóvel.",
            "model": "🚗 Designa a designação específica do veículo dentro da linha da marca, distinguindo-o de outras variantes e influenciando a sua posição competitiva e perceção de valor.",
            "trim": "🔧 Indica o nível de acabamento ou a configuração escolhida para o veículo, que pode incluir opções e características adicionais que diferenciam as variantes em termos de conforto, tecnologia e desempenho.",
            "body": "🚙 Define o tipo de carroçaria do veículo, descrevendo a sua estrutura e design, o que afeta a funcionalidade, o espaço interior e a dinâmica de condução.",
            "transmission": "⚙️ Especifica o sistema de transmissão, automático ou manual. Esta característica determina como a potência é transmitida para as rodas e influencia a experiência de condução e a eficiência do veículo.",
            "vin": "🔑 Trata-se de um código único atribuído a cada veículo, essencial para a verificação da sua autenticidade, rastreamento do histórico e registo de manutenção ao longo do tempo.",
            "state": "🌍 Indica o estado de onde o veículo está disponível, fornecendo a localização geográfica que pode ser relevante para questões de logística, transporte e acesso ao automóvel.",
            "condition": "🔍 Avalia o estado geral do veículo, considerando fatores como desgaste, manutenção e eventuais danos, expressa através de uma escala que facilita a comparação entre diferentes exemplares.",
            "odometer": "📏 Regista a distância total percorrida pelo veículo, um parâmetro fundamental para estimar o nível de utilização e, consequentemente, o desgaste mecânico e a depreciação do automóvel.",
            "color": "🎨 Descreve a cor predominante da pintura do veículo, um aspeto que pode influenciar tanto a estética como a preferência dos potenciais compradores.",
            "interior": "🛋️ Detalha a cor e os materiais empregados no interior do veículo, refletindo a qualidade, o conforto e o estilo do design interno, elementos que impactam a experiência do utilizador.",
            "seller": "👤 Identifica a entidade ou indivíduo responsável pela venda do veículo, sendo um fator relevante na avaliação da credibilidade e da transparência na transação.",
            "mmr": "💰 Fornece uma estimativa do valor de mercado do veículo, baseada em análises de dados históricos de transações e leilões, servindo como referência para avaliações e negociações."
        }

        st.markdown(f"<h><strong>Descrição:</strong></h4><p style='font-size:20px'>{descriptions[real_variable]}</p>", unsafe_allow_html=True)



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
            # st.write("**📊 Estatísticas Descritivas:**")
            # st.write(f"🔢 **Média**: {df[real_variable].mean():.2f}")
            # st.write(f"📏 **Desvio Padrão**: {df[real_variable].std():.2f}")
            # st.write(f"📉 **Mínimo**: {df[real_variable].min()}")
            # st.write(f"📈 **Máximo**: {df[real_variable].max()}")
            # st.write(f"🔘 **Mediana**: {df[real_variable].median()}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Média", f"{df[real_variable].mean():,.2f}")
                st.metric("📉 Mínimo", f"{df[real_variable].min():,.2f}")

            with col2:
                st.metric("📏 Desvio Padrão", f"{df[real_variable].std():,.2f}")
                st.metric("📈 Máximo", f"{df[real_variable].max():,.2f}")

            with col3:
                st.metric("🔘 Mediana", f"{df[real_variable].median():,.2f}")
                st.metric("📊 Intervalo Interquartil",
                            f"{df[real_variable].quantile(0.75) - df[real_variable].quantile(0.25):,.2f}")

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



    with aba3:
        # Dicionário de tradução (pode estar declarado fora para reutilização geral)
        nomes_traduzidos = {
            "year": "Ano",
            "make": "Marca",
            "model": "Modelo",
            "trim": "Especificação",
            "body": "Segmento do Carro",
            "transmission": "Transmissão",
            "vin": "ID",
            "state": "Estado",
            "condition": "Condição do Carro",
            "odometer": "Km",
            "color": "Cor do Carro",
            "interior": "Cor do Interior",
            "seller": "Vendedor",
            "mmr": "Valor de Mercado",
            "sellingprice": "Preço"
        }

        # Inverso do dicionário para obter o nome técnico a partir do nome traduzido
        nomes_invertidos = {v: k for k, v in nomes_traduzidos.items()}

        st.subheader("🔗 Matriz de Correlação")


        def cramers_v(x, y):
            """Calcula a correlação de Cramér's V entre duas variáveis categóricas."""
            confusion_matrix = pd.crosstab(x, y)
            chi2 = stats.chi2_contingency(confusion_matrix)[0]
            n = confusion_matrix.sum().sum()
            min_dim = min(confusion_matrix.shape) - 1
            return np.sqrt(chi2 / (n * min_dim))


        # Criar lista de nomes exibidos no multiselect
        # Excluir a coluna "rua"
        colunas_filtradas = [col for col in df.columns if col != "Unnamed: 0"]

        # Gerar lista de nomes traduzidos (exibidos)
        variaveis_traduzidas = [nomes_traduzidos.get(col, col.capitalize()) for col in colunas_filtradas]

        # Mapa de nomes exibidos para os nomes reais das colunas
        mapa_nome_exibido_para_coluna = {
            nomes_traduzidos.get(col, col.capitalize()): col for col in colunas_filtradas
        }


        # Seleção de variáveis com nomes traduzidos
        selected_display_names = st.multiselect("Selecione as variáveis para a matriz", variaveis_traduzidas)

        # Mapear de volta para os nomes reais do DataFrame
        selected_vars = [mapa_nome_exibido_para_coluna[nome] for nome in selected_display_names]

        if len(selected_vars) < 2:
            st.warning("Selecione pelo menos duas variáveis.")
            st.stop()  # Impede que o código continue

        # Criar matriz vazia
        corr_matrix = pd.DataFrame(index=selected_vars, columns=selected_vars, dtype=float)

        for var1 in selected_vars:
            for var2 in selected_vars:
                if var1 == var2:
                    corr_matrix.loc[var1, var2] = 1.0
                elif df[var1].dtype in ['int64', 'float64'] and df[var2].dtype in ['int64', 'float64']:
                    # Correlação de Pearson
                    corr_matrix.loc[var1, var2] = df[[var1, var2]].corr().iloc[0, 1]
                elif df[var1].dtype == 'object' and df[var2].dtype == 'object':
                    if df[var1].nunique() > 1 and df[var2].nunique() > 1:
                        corr_matrix.loc[var1, var2] = cramers_v(df[var1], df[var2])
                    else:
                        corr_matrix.loc[var1, var2] = np.nan
                else:
                    # Correlação entre categórica e numérica
                    categories = pd.get_dummies(df[var1] if df[var1].dtype == 'object' else df[var2])
                    target = df[var2] if df[var1].dtype == 'object' else df[var1]
                    r_squared = np.mean([np.corrcoef(categories[col], target)[0, 1] ** 2 for col in categories.columns])
                    corr_matrix.loc[var1, var2] = r_squared

        # Preencher NaNs
        corr_matrix = corr_matrix.fillna(0)

        # Trocar nomes das linhas/colunas para os traduzidos, para visualização
        corr_matrix.index = [nomes_traduzidos.get(v, v.capitalize()) for v in corr_matrix.index]
        corr_matrix.columns = [nomes_traduzidos.get(v, v.capitalize()) for v in corr_matrix.columns]

        # Mostrar gráfico
        if not corr_matrix.isnull().values.all():
            fig = px.imshow(
                corr_matrix,
                text_auto=".2f",
                color_continuous_scale="viridis",
                title="Matriz de Correlação",
                labels=dict(color="Correlação")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("A matriz de correlação está vazia. Verifique os dados selecionados.")

        st.markdown("---")
        st.caption("© 2025 AutoImport Portugal. Todos os direitos reservados.")



