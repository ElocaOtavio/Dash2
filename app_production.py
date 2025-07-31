"""
app_production.py

Este é o arquivo principal da aplicação Streamlit para o Dashboard Eloca.
Ele orquestra o carregamento de dados, a lógica de navegação e a renderização das visualizações.

Data: 31/07/2025
Versão: 1.1 (Ajustado para carregamento de dados de URLs e cálculo de abas)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys

# Adicionar diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from data_processor import DataProcessor
from visualizations import VisualizationManager

# Inicializar configuração
config = Config()

# Configuração da página
st.set_page_config(
    page_title=config.APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicialização do processador de dados
@st.cache_data(ttl=config.CACHE_TTL, show_spinner=True)
def load_data():
    """
    Carrega dados com cache otimizado para produção.
    """
    processor = DataProcessor()
    # Agora, carregar_dados_completos já busca de ambas as URLs e processa as abas do dashboard
    return processor.carregar_dados_completos()

# Inicialização do gerenciador de visualizações
@st.cache_resource
def get_visualization_manager():
    return VisualizationManager()

viz_manager = get_visualization_manager()

# --- Funções de Renderização de Páginas ---

def render_resumo_geral(data, viz_manager):
    """Renderiza página de resumo geral."""
    st.markdown("## 📊 Resumo Geral do Dashboard")

    if not data:
        st.warning("Nenhum dado disponível para resumo geral.")
        return

    st.markdown("### Visão Geral dos Dados Carregados")
    
    # Criar uma instância temporária do DataProcessor para usar obter_resumo_dados
    # ou passar o resumo como parte do \'data\' retornado por load_data
    # Por simplicidade, vamos instanciar aqui, mas o ideal é que o resumo venha do load_data
    processor_temp = DataProcessor()
    resumo = processor_temp.obter_resumo_dados()

    if resumo:
        for aba, info in resumo.items():
            st.write(f"**{aba}**:")
            st.write(f"  - Linhas: {info["linhas"]}")
            st.write(f"  - Colunas: {info["colunas"]}")
            st.write(f"  - Memória: {info["memoria_mb"]} MB")
            st.write("---")
    else:
        st.info("Nenhum resumo de dados disponível.")

    st.markdown("### ⚙️ Info Técnica")
    st.write(f"**Cache**: {config.CACHE_TTL//60} minutos")
    st.write(f"**Debug**: {"Habilitado" if config.DEBUG_MODE else "Desabilitado"}")
    st.write(f"**Última Atualização**: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}")

def render_metas_individuais(data, viz_manager):
    """Renderiza a página de Metas Individuais."""
    st.markdown("## 🎯 Metas Individuais")
    df_metas = data.get("Metas Individuais")
    if df_metas is None or df_metas.empty:
        st.warning("Dados de \'Metas Individuais\' não disponíveis ou vazios. Verifique a lógica de cálculo no data_processor.py.")
        return
    viz_manager.render_metas_individuais(df_metas)

def render_resultados_area1(data, viz_manager):
    """Renderiza a página de Resultados Área 1."""
    st.markdown("## 📈 Resultados Área 1")
    df_area1 = data.get("Resultados área 1")
    if df_area1 is None or df_area1.empty:
        st.warning("Dados de \'Resultados área 1\' não disponíveis ou vazios. Verifique a lógica de cálculo no data_processor.py.")
        return
    viz_manager.render_resultados_area1(df_area1)

def render_resultados_area2(data, viz_manager):
    """Renderiza a página de Resultados Área 2."""
    st.markdown("## 📈 Resultados Área 2")
    df_area2 = data.get("Resultados área 2")
    if df_area2 is None or df_area2.empty:
        st.warning("Dados de \'Resultados área 2\' não disponíveis ou vazios. Verifique a lógica de cálculo no data_processor.py.")
        return
    viz_manager.render_resultados_area2(df_area2)

def render_grafico_individual_1(data, viz_manager):
    """Renderiza a página de Gráfico Individual 1."""
    st.markdown("## 📊 Gráfico Individual 1")
    df_grafico1 = data.get("Grafico-Individual_1")
    if df_grafico1 is None or df_grafico1.empty:
        st.warning("Dados de \'Grafico-Individual_1\' não disponíveis ou vazios. Verifique a lógica de cálculo no data_processor.py.")
        return
    viz_manager.render_grafico_individual_1(df_grafico1)

def render_grafico_individual_2(data, viz_manager):
    """Renderiza a página de Gráfico Individual 2."""
    st.markdown("## 📊 Gráfico Individual 2")
    df_grafico2 = data.get("Grafico-Individual_2")
    if df_grafico2 is None or df_grafico2.empty:
        st.warning("Dados de \'Grafico-Individual_2\' não disponíveis ou vazios. Verifique a lógica de cálculo no data_processor.py.")
        return
    viz_manager.render_grafico_individual_2(df_grafico2)

def render_csat_satisfacao(data, viz_manager):
    """Renderiza a página de CSAT - Pesquisa de Satisfação."""
    st.markdown("## 😊 CSAT - Pesquisa de Satisfação")

    df_csat = data.get("CSAT")
    csat_metricas = data.get("CSAT_Metricas", {})
    csat_relatorio = data.get("CSAT_Relatorio", [])

    if df_csat is None or df_csat.empty:
        st.warning("Dados de CSAT não disponíveis ou vazios. Verifique a URL da Pesquisa de Satisfação e o nome da aba \'Pesquisa de Satisfação\' ou \'CSAT\' dentro do arquivo.")
        return

    st.markdown("### Métricas Gerais")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="CSAT Score", value=f"{csat_metricas.get("csat_score", 0.0):.2f}%")
    with col2:
        st.metric(label="Total de Registros Processados", value=csat_metricas.get("total_registros_processados", 0))
    with col3:
        st.metric(label="Registros Duplicados Removidos", value=csat_metricas.get("registros_duplicados_removidos", 0))

    st.markdown("### Distribuição das Avaliações")
    if "distribuicao_avaliacoes" in csat_metricas and csat_metricas["distribuicao_avaliacoes"]:
        df_dist = pd.DataFrame(csat_metricas["distribuicao_avaliacoes"].items(), columns=["Avaliação", "Contagem"])
        fig = px.bar(df_dist, x="Avaliação", y="Contagem", title="Contagem de Avaliações")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma distribuição de avaliações disponível.")

    st.markdown("### Dados Processados (Amostra)")
    st.dataframe(df_csat.head(), use_container_width=True)

    st.markdown("### Relatório de Deduplicação (Amostra)")
    if csat_relatorio:
        st.dataframe(pd.DataFrame(csat_relatorio).head(), use_container_width=True)
    else:
        st.info("Nenhum registro de deduplicação.")


# --- Função Principal da Aplicação --- #
def main():
    st.sidebar.image("https://www.streamlit.io/images/brand/streamlit-logo-secondary-colordark.svg", width=100 )
    st.sidebar.title("Navegação")

    # Menu de navegação
    pages = {
        "Resumo Geral": "resumo",
        "Metas Individuais": "metas",
        "Resultados Área 1": "resultados1",
        "Resultados Área 2": "resultados2",
        "Gráfico Individual 1": "grafico1",
        "Gráfico Individual 2": "grafico2",
        "CSAT - Pesquisa de Satisfação": "csat",
    }

    selected_page_name = st.sidebar.radio("Ir para", list(pages.keys()))
    selected_page = pages[selected_page_name]

    # Carregar dados (com cache)
    data = load_data()

    if data is None:
        st.error("Não foi possível carregar os dados. Verifique as configurações e os logs.")
        return

    # Renderização das páginas
    if selected_page == "resumo":
        render_resumo_geral(data, viz_manager)
    elif selected_page == "metas":
        render_metas_individuais(data, viz_manager)
    elif selected_page == "resultados1":
        render_resultados_area1(data, viz_manager)
    elif selected_page == "resultados2":
        render_resultados_area2(data, viz_manager)
    elif selected_page == "grafico1":
        render_grafico_individual_1(data, viz_manager)
    elif selected_page == "grafico2":
        render_grafico_individual_2(data, viz_manager)
    elif selected_page == "csat":
        render_csat_satisfacao(data, viz_manager)


if __name__ == "__main__":
    main()
