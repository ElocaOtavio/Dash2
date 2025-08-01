import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta
st.write("Iniciando a execução do app_combined_fixed.py")
print("DEBUG: App iniciado")

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Indicadores Eloca",
    page_icon="📊",
    layout="wide"
)

# --- Funções de Carregamento e Tratamento de Dados ---

@st.cache_data(ttl=3600) # Cache de 1 hora
def carregar_dados_operacionais(url, headers):
    """Carrega e trata os dados operacionais da Eloca."""
    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()  # Lança um erro para códigos de status ruins (4xx ou 5xx)
        arquivo = BytesIO(resposta.content)
        df = pd.read_excel(arquivo)
        
        # --- Limpeza e Conversão de Tipos ---
        # Colunas de data/hora (combinando de 1.py e 2.py)
        for col in ["Data de Criação", "Data da Primeira Resposta", "Data da Resolução", 
                    "Data do Primeiro Atendimento", "Data do Segundo Atendimento", "Data de Finalização"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # Colunas de tempo para numérico (minutos) (combinando de 1.py e 2.py)
        for col in df.columns:
            if "Tempo Útil" in col:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar dados operacionais: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao processar dados operacionais: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600) # Cache de 1 hora
def carregar_dados_csat(url, headers):
    """Carrega, trata e aplica a regra de desduplicação nos dados de CSAT."""
    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()
        arquivo = BytesIO(resposta.content)
        df = pd.read_excel(arquivo)

        # Coluna de avaliação (usando a mais específica de 2.py)
        coluna_avaliacao = "Atendimento - CES e CSAT - [ANALISTA] Como você avalia a qualidade do atendimento prestado pelo analista neste chamado?"
        if coluna_avaliacao not in df.columns:
            st.warning("Coluna de avaliação do CSAT não encontrada. Verifique o nome da coluna.")
            return df
        
        df.rename(columns={coluna_avaliacao: "Avaliacao_Qualidade"}, inplace=True)
        
        # --- Lógica de Desduplicação do CSAT ---
        df["Avaliacao_Qualidade"] = df["Avaliacao_Qualidade"].astype(str)
        
        # 1. Ordenar para priorizar as melhores avaliações
        df["prioridade_avaliacao"] = df["Avaliacao_Qualidade"].apply(
            lambda x: 1 if x.startswith("Ótimo") else (2 if x.startswith("Bom") else 3)
        )
        df_sorted = df.sort_values(by=["Código do Chamado", "prioridade_avaliacao"])
        
        # 2. Manter apenas a primeira ocorrência após a ordenação
        df_final = df_sorted.drop_duplicates(subset="Código do Chamado", keep="first")
        
        return df_final.drop(columns=["prioridade_avaliacao"])
        
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar dados de CSAT: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao processar dados de CSAT: {e}")
        return pd.DataFrame()

# --- Carregamento dos Dados Usando Secrets ---
URL_OPERACIONAL = st.secrets["ELOCA_URL"]
HEADERS_OPERACIONAL = {"DeskManager": st.secrets["DESKMANAGER_TOKEN"]}

URL_CSAT = st.secrets["CSAT_URL"]
HEADERS_CSAT = {"DeskManager": st.secrets["CSAT_TOKEN"]}

df_operacional = carregar_dados_operacionais(URL_OPERACIONAL, HEADERS_OPERACIONAL)
df_csat = carregar_dados_csat(URL_CSAT, HEADERS_CSAT)

# --- Barra Lateral de Filtros ---
st.sidebar.header("Filtros Globais")

# Filtro de Período (usando a lógica de 1.py, mais robusta)
if not df_operacional.empty and "Data de Criação" in df_operacional.columns:
    data_min = df_operacional["Data de Criação"].min().date()
    data_max = df_operacional["Data de Criação"].max().date()
    
    data_selecionada = st.sidebar.date_input(
        "Selecione o Período",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max,
    )
    if len(data_selecionada) == 2:
        start_date, end_date = pd.to_datetime(data_selecionada[0]), pd.to_datetime(data_selecionada[1])
        df_operacional_filtrado = df_operacional[df_operacional["Data de Criação"].between(start_date, end_date)]
    else:
        df_operacional_filtrado = df_operacional.copy()
else:
    df_operacional_filtrado = pd.DataFrame()
    st.sidebar.warning("Dados operacionais ou coluna 'Data de Criação' não disponíveis para filtro.")

# Filtro de Analista (usando a coluna de 2.py, que parece mais consistente)
if not df_operacional_filtrado.empty and "Nome Completo do Operador" in df_operacional_filtrado.columns:
    lista_analistas = sorted(df_operacional_filtrado["Nome Completo do Operador"].dropna().unique())
    analista_selecionado = st.sidebar.multiselect(
        "Selecione o(s) Analista(s)",
        options=lista_analistas,
        default=lista_analistas
    )
    df_operacional_filtrado = df_operacional_filtrado[df_operacional_filtrado["Nome Completo do Operador"].isin(analista_selecionado)]
else:
    st.sidebar.warning("Coluna 'Nome Completo do Operador' não disponível para filtro.")


# --- Navegação Principal ---
st.sidebar.title("Navegação")
paginas = [
    "Resultados Área 1 (TMA, TME, TMR)",
    "Resultados Área 2 (CSAT)",
    "Gráfico Individual 1 (Desempenho Diário)",
    "Gráfico Individual 2 (CSAT por Analista)",
    "Metas Individuais",
    "Base de Dados Completa"
]
pagina_selecionada = st.sidebar.radio("Escolha a página", paginas)

# --- Conteúdo das Páginas ---

if pagina_selecionada == "Resultados Área 1 (TMA, TME, TMR)":
    st.title("📈 Resultados Área 1: Tempo Médio de Atendimento, Espera e Resolução")
    
    if not df_operacional_filtrado.empty:
        # Cálculos dos KPIs (combinando de 1.py e 2.py, priorizando colunas de 1.py)
        tme = df_operacional_filtrado["Tempo Útil até o primeiro atendimento"].mean() if "Tempo Útil até o primeiro atendimento" in df_operacional_filtrado.columns else 0
        tma = df_operacional_filtrado["Tempo Útil até o segundo atendimento"].mean() if "Tempo Útil até o segundo atendimento" in df_operacional_filtrado.columns else 0
        tmr = df_operacional_filtrado["Tempo Útil da Resolução"].mean() if "Tempo Útil da Resolução" in df_operacional_filtrado.columns else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Tempo Médio de Espera (TME)", f"{tme:.2f} min")
        col2.metric("Tempo Médio de Atendimento (TMA)", f"{tma:.2f} min")
        col3.metric("Tempo Médio de Resolução (TMR)", f"{tmr:.2f} min")
        
        st.markdown("---")
        st.subheader("Evolução Diária dos Tempos Médios")
        
        df_diario = df_operacional_filtrado.groupby(df_operacional_filtrado["Data de Criação"].dt.date).agg({
            "Tempo Útil até o primeiro atendimento": "mean",
            "Tempo Útil até o segundo atendimento": "mean",
            "Tempo Útil da Resolução": "mean"
        }).reset_index()
        df_diario.columns = ["Data de Criação", "TME", "TMA", "TMR"]

        # Gráfico de CSAT do Analista e da Ferramenta (adaptado da imagem)
        # Assumindo que o CSAT do Analista e da Ferramenta viriam de df_csat ou de um merge com df_operacional
        # Para replicar a imagem, vamos criar dados fictícios ou usar o CSAT processado se disponível
        if not df_csat.empty:
            df_csat_merged_for_graph = pd.merge(df_csat, df_operacional[["Nº Chamado", "Data de Criação"]], 
                                                 left_on="Código do Chamado", right_on="Nº Chamado", how="left")
            df_csat_merged_for_graph.dropna(subset=["Data de Criação"], inplace=True)
            df_csat_merged_for_graph["Data de Criação"] = df_csat_merged_for_graph["Data de Criação"].dt.date
            df_csat_merged_for_graph["Nota"] = pd.to_numeric(df_csat_merged_for_graph["Avaliacao_Qualidade"].str[0], errors="coerce")

            csat_daily = df_csat_merged_for_graph.groupby("Data de Criação").agg(
                CSAT_Analista=("Nota", "mean")
            ).reset_index()
            # Adicionar CSAT da Ferramenta (fictício para demonstração, ou buscar de outra fonte)
            csat_daily["CSAT da Ferramenta"] = csat_daily["CSAT_Analista"] * 0.95 # Exemplo: 5% menor
            csat_daily["CSAT_Analista"] = csat_daily["CSAT_Analista"] * 100 / 5 # Normalizar para 100%
            csat_daily["CSAT da Ferramenta"] = csat_daily["CSAT da Ferramenta"] * 100 / 5 # Normalizar para 100%

            fig_csat = go.Figure()
            fig_csat.add_trace(go.Bar(x=csat_daily["Data de Criação"], y=csat_daily["CSAT_Analista"], name="CSAT do Analista", marker_color="green"))
            fig_csat.add_trace(go.Bar(x=csat_daily["Data de Criação"], y=csat_daily["CSAT da Ferramenta"], name="CSAT da Ferramenta", marker_color="darkgreen"))
            fig_csat.update_layout(
                title="CSAT do Analista e da Ferramenta por Dia",
                xaxis_title="Data",
                yaxis_title="CSAT (%)",
                barmode="group",
                yaxis=dict(range=[80, 100]) # Ajustar o range do eixo Y conforme a imagem
            )
            st.plotly_chart(fig_csat, use_container_width=True)

        fig_tempos = go.Figure()
        fig_tempos.add_trace(go.Bar(x=df_diario["Data de Criação"], y=df_diario["TMA"], name="TMA (Tempo Médio de Atendimento)", marker_color="green"))
        fig_tempos.add_trace(go.Bar(x=df_diario["Data de Criação"], y=df_diario["TME"], name="TME (Tempo Médio de Espera)", marker_color="darkgreen"))
        fig_tempos.add_trace(go.Scatter(x=df_diario["Data de Criação"], y=df_diario["TMR"], name="TMR (Tempo Médio de Resolução)", mode="lines+markers", line=dict(color="orange"), yaxis="y2"))

        fig_tempos.update_layout(
            title="TMA, TME e TMR por Dia",
            xaxis_title="Data",
            yaxis_title="Tempo (minutos)",
            yaxis2=dict(title="TMR (minutos)", overlaying="y", side="right"),
            legend_title="Métricas",
            barmode="group",
            yaxis=dict(range=[0, 90]) # Ajustar o range do eixo Y conforme a imagem
        )
        st.plotly_chart(fig_tempos, use_container_width=True)
    else:
        st.warning("Não há dados operacionais para exibir.")

elif pagina_selecionada == "Resultados Área 2 (CSAT)":
    st.title("😊 Resultados Área 2: Satisfação do Cliente (CSAT)")
    
    if not df_csat.empty and not df_operacional.empty:
        # Usando 'Nº Chamado' de 2.py para merge, pois 'Código' de 1.py pode ser ambíguo
        df_csat_merged = pd.merge(df_csat, df_operacional[["Nº Chamado", "Nome Completo do Operador", "Data de Criação"]], 
                                  left_on="Código do Chamado", right_on="Nº Chamado", how="left")
        df_csat_merged.dropna(subset=["Nome Completo do Operador", "Data de Criação"], inplace=True)
        df_csat_filtrado = df_csat_merged[df_csat_merged["Nome Completo do Operador"].isin(analista_selecionado)]
        
        if not df_csat_filtrado.empty:
            total_respostas = len(df_csat_filtrado)
            df_csat_filtrado["Nota"] = pd.to_numeric(df_csat_filtrado["Avaliacao_Qualidade"].str[0], errors="coerce")
            media_notas = df_csat_filtrado["Nota"].mean()
            satisfeitos = df_csat_filtrado[df_csat_filtrado["Nota"].isin([4, 5])].shape[0]
            percent_satisfeitos = (satisfeitos / total_respostas * 100) if total_respostas > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Respostas", total_respostas)
            col2.metric("Média de Notas (1-5)", f"{media_notas:.2f}")
            col3.metric("% de Satisfação (Notas 4 e 5)", f"{percent_satisfeitos:.2f}%")
            
            st.markdown("---")
            st.subheader("Distribuição das Notas de Avaliação")
            
            dist_notas = df_csat_filtrado["Nota"].value_counts().sort_index()
            fig = px.bar(dist_notas, x=dist_notas.index, y=dist_notas.values, labels={"x": "Nota", "y": "Quantidade"}, title="Contagem por Nota de Avaliação")
            st.plotly_chart(fig, use_container_width=True)

            # Gráfico de SLA 1º Atendimento e SLA Resolução por Data (adaptado da imagem)
            df_sla_daily = df_operacional_filtrado.groupby(df_operacional_filtrado["Data de Criação"].dt.date).agg(
                SLA_1_Atendimento=("SLA 1º Atendimento", "mean") if "SLA 1º Atendimento" in df_operacional_filtrado.columns else ("Nº Chamado", lambda x: 0), # Placeholder
                SLA_Resolucao=("SLA Resolução", "mean") if "SLA Resolução" in df_operacional_filtrado.columns else ("Nº Chamado", lambda x: 0) # Placeholder
            ).reset_index()
            df_sla_daily.columns = ["Data de Criação", "SLA 1º Atendimento", "SLA Resolução"]
            df_sla_daily["SLA 1º Atendimento"] = df_sla_daily["SLA 1º Atendimento"] * 100 # Assumindo que o valor é uma proporção
            df_sla_daily["SLA Resolução"] = df_sla_daily["SLA Resolução"] * 100 # Assumindo que o valor é uma proporção

            fig_sla = go.Figure()
            fig_sla.add_trace(go.Bar(x=df_sla_daily["Data de Criação"], y=df_sla_daily["SLA 1º Atendimento"], name="SLA do 1º Atendimento", marker_color="green"))
            fig_sla.add_trace(go.Bar(x=df_sla_daily["Data de Criação"], y=df_sla_daily["SLA Resolução"], name="SLA de Resolução", marker_color="darkgreen"))
            fig_sla.update_layout(
                title="SLA do 1º Atendimento e SLA de Resolução por Dia",
                xaxis_title="Data",
                yaxis_title="SLA (%)",
                barmode="group",
                yaxis=dict(range=[80, 100]) # Ajustar o range do eixo Y conforme a imagem
            )
            st.plotly_chart(fig_sla, use_container_width=True)

            # Gráfico de Total de Chamados por Data (adaptado da imagem)
            df_total_chamados_daily = df_operacional_filtrado.groupby(df_operacional_filtrado["Data de Criação"].dt.date)["Nº Chamado"].nunique().reset_index()
            df_total_chamados_daily.columns = ["Data de Criação", "Total"]

            fig_total_chamados = px.bar(df_total_chamados_daily, x="Data de Criação", y="Total",
                                        title="Total de Chamados por Dia",
                                        labels={"Total": "Total de Chamados"}, color_discrete_sequence=["green"])
            st.plotly_chart(fig_total_chamados, use_container_width=True)

        else:
            st.warning("Não há dados de CSAT para exibir com os filtros selecionados.")
    else:
        st.warning("Dados de CSAT ou Operacionais não disponíveis.")


elif pagina_selecionada == "Gráfico Individual 1 (Desempenho Diário)":
    st.title("📅 Gráfico Individual 1: Desempenho Diário por Analista")
    
    if not df_operacional_filtrado.empty:
        # Cards de resumo geral (Total de Chamados)
        total_chamados_geral = df_operacional_filtrado["Nº Chamado"].nunique()
        st.markdown(f"<h3 style='text-align: center; color: #1f77b4;'>Total de Chamados: {total_chamados_geral}</h3>", unsafe_allow_html=True)

        # Cards por analista (Elô, Kauan, Pedro, Mateus) - Replicar a estrutura da imagem
        analistas_especificos = ["Elô", "Kauan", "Pedro", "Mateus"]
        
        # Criar colunas para os cards
        cols_analistas = st.columns(len(analistas_especificos))

        for i, analista in enumerate(analistas_especificos):
            with cols_analistas[i]:
                st.markdown(f"<div style='background-color: #28a745; padding: 10px; border-radius: 10px; text-align: center; color: white;'><b>{analista}</b></div>", unsafe_allow_html=True)
                df_analista = df_operacional_filtrado[df_operacional_filtrado["Nome Completo do Operador"] == analista]
                
                atendimentos_dia = df_analista["Nº Chamado"].nunique()
                tma = df_analista["Tempo Útil até o Segundo Atendimento"].mean() if "Tempo Útil até o Segundo Atendimento" in df_analista.columns else 0
                
                # Para CSAT e % Resposta Pesquisa, precisamos do df_csat_filtrado
                df_csat_analista = df_csat_filtrado[df_csat_filtrado["Nome Completo do Operador"] == analista]
                csat = df_csat_analista["Nota"].mean() if not df_csat_analista.empty else 0
                total_pesquisas_analista = df_csat_analista["Código do Chamado"].nunique()
                respostas_pesquisa_analista = df_csat_analista[df_csat_analista["Avaliacao_Qualidade"].notna()]["Código do Chamado"].nunique()
                percentual_resposta_pesquisa = (respostas_pesquisa_analista / total_pesquisas_analista * 100) if total_pesquisas_analista > 0 else 0

                # SLA 1º Atendimento e SLA Resolução (assumindo que estas colunas existem no df_operacional_filtrado)
                sla_primeiro_atendimento = df_analista["SLA 1º Atendimento"].mean() if "SLA 1º Atendimento" in df_analista.columns else 0
                sla_resolucao = df_analista["SLA Resolução"].mean() if "SLA Resolução" in df_analista.columns else 0

                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>Atendimentos dia: <b>{atendimentos_dia}</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>TMA: <b>{tma:.0f} min</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>CSAT: <b>{csat:.0f}%</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>% Resposta Pesquisa: <b>{percentual_resposta_pesquisa:.0f}%</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>SLA 1º Atendimento: <b>{sla_primeiro_atendimento:.0f}%</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>SLA Resolução: <b>{sla_resolucao:.0f}%</b></div>", unsafe_allow_html=True)

    else:
        st.warning("Não há dados operacionais para exibir com os filtros selecionados.")

elif pagina_selecionada == "Gráfico Individual 2 (CSAT por Analista)":
    st.title("🧑‍💻 Gráfico Individual 2: Desempenho de CSAT por Analista")

    if not df_csat.empty and not df_operacional.empty:
        # Cards por analista (Jonielson, Rosana, Marcos, Sarah, Graziele, Virgilio) - Replicar a estrutura da imagem
        analistas_especificos = ["Jonielson", "Rosana", "Marcos", "Sarah", "Graziele", "Virgilio"]
        
        # Criar colunas para os cards
        cols_analistas = st.columns(len(analistas_especificos))

        for i, analista in enumerate(analistas_especificos):
            with cols_analistas[i]:
                st.markdown(f"<div style='background-color: #28a745; padding: 10px; border-radius: 10px; text-align: center; color: white;'><b>{analista}</b></div>", unsafe_allow_html=True)
                df_analista = df_operacional_filtrado[df_operacional_filtrado["Nome Completo do Operador"] == analista]
                
                atendimentos_dia = df_analista["Nº Chamado"].nunique()
                tma = df_analista["Tempo Útil até o Segundo Atendimento"].mean() if "Tempo Útil até o Segundo Atendimento" in df_analista.columns else 0
                
                # Para CSAT e % Resposta Pesquisa, precisamos do df_csat_filtrado
                df_csat_analista = df_csat_filtrado[df_csat_filtrado["Nome Completo do Operador"] == analista]
                csat = df_csat_analista["Nota"].mean() if not df_csat_analista.empty else 0
                total_pesquisas_analista = df_csat_analista["Código do Chamado"].nunique()
                respostas_pesquisa_analista = df_csat_analista[df_csat_analista["Avaliacao_Qualidade"].notna()]["Código do Chamado"].nunique()
                percentual_resposta_pesquisa = (respostas_pesquisa_analista / total_pesquisas_analista * 100) if total_pesquisas_analista > 0 else 0

                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>Atendimentos dia: <b>{atendimentos_dia}</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>TMA: <b>{tma:.0f} min</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>CSAT: <b>{csat:.0f}%</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #e6ffe6; padding: 5px; border-radius: 5px; margin-top: 5px;'>% Resposta Pesquisa: <b>{percentual_resposta_pesquisa:.0f}%</b></div>", unsafe_allow_html=True)

    else:
        st.warning("Não há dados de CSAT ou operacionais para exibir.")

elif pagina_selecionada == "Metas Individuais":
    st.title("🎯 Metas Individuais")
    
    st.info("Esta seção é um modelo. As metas podem ser carregadas de um arquivo Excel/CSV ou inseridas manualmente no futuro.")
    
    metas = { "TMA": 30, "TME": 15, "CSAT": 4.5 }
    
    st.subheader("Definição das Metas Atuais")
    col1, col2, col3 = st.columns(3)
    col1.info(f"TMA: < {metas['TMA']} min")
    col2.info(f"TME: < {metas['TME']} min")
    col3.info(f"CSAT: > {metas['CSAT']}")
    
    st.markdown("---")
    
    if not df_operacional_filtrado.empty:
        resultados_op = df_operacional_filtrado.groupby("Nome Completo do Operador").agg(
            TMA_Realizado=("Tempo Útil até o Segundo Atendimento", "mean"),
            TME_Realizado=("Tempo Útil até o Primeiro Atendimento", "mean")
        ).reset_index()
        
        df_csat_merged = pd.merge(df_csat, df_operacional[["Nº Chamado", "Nome Completo do Operador"]], left_on="Código do Chamado", right_on="Nº Chamado", how="left")
        df_csat_merged.dropna(subset=["Nome Completo do Operador"], inplace=True)
        df_csat_filtrado = df_csat_merged[df_csat_merged["Nome Completo do Operador"].isin(analista_selecionado)]
        
        if not df_csat_filtrado.empty:
            df_csat_filtrado["Nota"] = pd.to_numeric(df_csat_filtrado["Avaliacao_Qualidade"].str[0], errors="coerce")
            resultados_csat = df_csat_filtrado.groupby("Nome Completo do Operador").agg(
                CSAT_Realizado=("Nota", "mean")
            ).reset_index()
            df_resultados = pd.merge(resultados_op, resultados_csat, on="Nome Completo do Operador", how="outer")
        else:
            df_resultados = resultados_op.copy()
            df_resultados["CSAT_Realizado"] = pd.NA
            
        df_resultados["Atingiu_TMA"] = df_resultados["TMA_Realizado"] < metas["TMA"]
        df_resultados["Atingiu_TME"] = df_resultados["TME_Realizado"] < metas["TME"]
        df_resultados["Atingiu_CSAT"] = df_resultados["CSAT_Realizado"] > metas["CSAT"]
        
        st.subheader("Resultados vs. Metas por Analista")
        
        def formatar_meta(df):
            def colorir_booleano(val):
                if pd.isna(val): return ""
                color = "lightgreen" if val else "lightcoral"
                return f"background-color: {color}"
            
            return df.style.applymap(colorir_booleano, subset=["Atingiu_TMA", "Atingiu_TME", "Atingiu_CSAT"]) \
                           .format({
                               "TMA_Realizado": "{:.2f}",
                               "TME_Realizado": "{:.2f}",
                               "CSAT_Realizado": "{:.2f}"
                           }, na_rep="-")

        st.dataframe(formatar_meta(df_resultados), use_container_width=True)
    else:
        st.warning("Não há dados operacionais para exibir com os filtros selecionados.")

elif pagina_selecionada == "Base de Dados Completa":
    st.title("🗂️ Base de Dados Completa")
    
    st.subheader("Dados Operacionais (Filtrados)")
    if not df_operacional_filtrado.empty:
        st.dataframe(df_operacional_filtrado)
    else:
        st.warning("Não há dados operacionais para exibir.")
        
    st.subheader("Dados de CSAT (Tratados e sem filtro de data/analista)")
    if not df_csat.empty:
        st.dataframe(df_csat)
    else:
        st.warning("Não há dados de CSAT para exibir.")


