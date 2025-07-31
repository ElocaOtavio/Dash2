"""
Dashboard Eloca - Versão de Produção
Sistema de Gestão de Service Desk

Autor: Elô
Data: 30/07/2025
Versão: 1.0
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
    page_title="Dashboard Eloca - Service Desk",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para produção
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #17becf 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .sidebar-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #28a745;
    }
    
    .status-ok {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .nav-button {
        width: 100%;
        margin: 0.2rem 0;
        border-radius: 8px;
        border: none;
        padding: 0.5rem;
        background: #f8f9fa;
        transition: all 0.3s;
    }
    
    .nav-button:hover {
        background: #e9ecef;
        transform: translateY(-2px);
    }
    
    .nav-button.active {
        background: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do processador de dados
@st.cache_data(ttl=config.CACHE_TTL, show_spinner=True)
def load_data():
    """
    Carrega dados com cache otimizado para produção.
    """
    processor = DataProcessor()
    return processor.carregar_dados_completos()

# Inicialização do gerenciador de visualizações
@st.cache_resource
def get_visualization_manager():
    """Retorna instância do gerenciador de visualizações."""
    return VisualizationManager()

# Função principal
def main():
    # Cabeçalho principal
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard Eloca - Gestão de Vendas</h1>
        <p>Sistema Profissional de Análise de Vendas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicialização dos gerenciadores
    viz_manager = get_visualization_manager()
    
    # Carregamento de dados
    try:
        data = load_data()
        
        if not data:
            st.error("❌ Erro ao carregar dados. Verifique a configuração da API.")
            return
            
    except Exception as e:
        st.error(f"❌ Erro no sistema: {str(e)}")
        st.info("💡 Entre em contato com o suporte técnico.")
        return
    
    # Menu de navegação
    menu_options = {
        "📊 Resumo Geral": "resumo",
        "🎯 Metas Individuais": "metas", 
        "📈 Resultados Área 1": "area1",
        "📉 Resultados Área 2": "area2",
        "📋 Gráfico Individual 1": "grafico1",
        "📊 Gráfico Individual 2": "grafico2",
        "😊 CSAT - Satisfação": "csat"
    }
    
    # Navegação horizontal
    cols = st.columns(len(menu_options))
    selected_page = st.session_state.get('selected_page', 'resumo')
    
    for i, (label, key) in enumerate(menu_options.items()):
        with cols[i]:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.selected_page = key
                selected_page = key
    
    # Sidebar com informações do sistema
    with st.sidebar:
        st.markdown("### 📊 Status do Sistema")
        
        # Status de produção
        st.markdown("""
        <div class="sidebar-info">
            <h4>🚀 Modo Produção</h4>
            <p class="status-ok">✅ Sistema Ativo</p>
            <p class="status-ok">✅ Dados Atualizados</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Informações dos dados
        if data:
            total_linhas = sum(len(df) for df in data.values() if df is not None)
            total_colunas = sum(len(df.columns) for df in data.values() if df is not None)
            abas_com_dados = len([df for df in data.values() if df is not None and len(df) > 0])
            
            st.markdown("### 📋 Dados Carregados")
            st.metric("Total de Linhas", total_linhas)
            st.metric("Total de Colunas", total_colunas) 
            st.metric("Abas com Dados", f"{abas_com_dados}/5")
            
            # Última atualização
            st.markdown("### ⏰ Última Atualização")
            st.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            
            # Informações técnicas
            st.markdown("### ⚙️ Info Técnica")
            st.write(f"**Cache**: {config.CACHE_TTL//60} minutos")
            st.write(f"**Debug**: {'Habilitado' if config.DEBUG_MODE else 'Desabilitado'}")
    
    # Renderização das páginas
    if selected_page == "resumo":
        render_resumo_geral(data, viz_manager)
    elif selected_page == "metas":
        render_metas_individuais(data, viz_manager)
    elif selected_page == "area1":
        render_resultados_area(data, viz_manager, "Resultados área 1", "Área 1")
    elif selected_page == "area2":
        render_resultados_area(data, viz_manager, "Resultados área 2", "Área 2")
    elif selected_page == "grafico1":
        render_grafico_individual_1(data, viz_manager)
    elif selected_page == "grafico2":
        render_grafico_individual_2(data, viz_manager)
    elif selected_page == "csat":
        render_csat_satisfacao(data, viz_manager)

def render_resumo_geral(data, viz_manager):
    """Renderiza página de resumo geral."""
    st.markdown("## 📊 Resumo Geral dos Dados")
    
    # Métricas principais
    if data:
        total_linhas = sum(len(df) for df in data.values() if df is not None)
        total_colunas = sum(len(df.columns) for df in data.values() if df is not None)
        abas_com_dados = len([df for df in data.values() if df is not None and len(df) > 0])
        memoria_total = sum(df.memory_usage(deep=True).sum() for df in data.values() if df is not None) / 1024 / 1024
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total de Linhas", total_linhas)
        with col2:
            st.metric("📋 Total de Colunas", total_colunas)
        with col3:
            st.metric("✅ Abas com Dados", f"{abas_com_dados}/5")
        with col4:
            st.metric("💾 Memória Total", f"{memoria_total:.1f} MB")
        
        # Gráficos de resumo
        st.markdown("### 📈 Resumo Geral dos Dados")
        
        # Preparar dados para gráficos
        resumo_data = []
        for nome_aba, df in data.items():
            if df is not None:
                resumo_data.append({
                    'Aba': nome_aba,
                    'Linhas': len(df),
                    'Colunas': len(df.columns),
                    'Cols_Numericas': len(df.select_dtypes(include=['number']).columns),
                    'Valores_Nulos': df.isnull().sum().sum(),
                    'Memoria_MB': df.memory_usage(deep=True).sum() / 1024 / 1024
                })
        
        resumo_df = pd.DataFrame(resumo_data)
        
        if not resumo_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_linhas = px.bar(
                    resumo_df, x='Aba', y='Linhas',
                    title='Número de Linhas por Aba'
                )
                st.plotly_chart(fig_linhas, use_container_width=True)
            
            with col2:
                fig_colunas = px.bar(
                    resumo_df, x='Aba', y='Colunas',
                    title='Número de Colunas por Aba'
                )
                st.plotly_chart(fig_colunas, use_container_width=True)
            
            # Tabela detalhada
            st.markdown("### 📋 Detalhes por Aba")
            st.dataframe(resumo_df, use_container_width=True)

def render_metas_individuais(data, viz_manager):
    """Renderiza página de metas individuais."""
    st.markdown("## 🎯 Metas Individuais")
    
    df = data.get('Metas Individuais')
    if df is None or df.empty:
        st.warning("⚠️ Dados de metas individuais não disponíveis.")
        return
    
    # Usar o gerenciador de visualizações
    fig = viz_manager.criar_grafico_metas_individuais(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Dados detalhados
    st.markdown("### 📋 Dados Detalhados")
    st.dataframe(df, use_container_width=True)

def render_resultados_area(data, viz_manager, aba_nome, area_display):
    """Renderiza página de resultados por área."""
    st.markdown(f"## 📈 {area_display}")
    
    df = data.get(aba_nome)
    if df is None or df.empty:
        st.warning(f"⚠️ Dados de {area_display} não disponíveis.")
        return
    
    # Usar o gerenciador de visualizações
    fig = viz_manager.criar_grafico_resultados_area(df, area_display)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Dados detalhados
    st.markdown("### 📋 Dados Detalhados")
    st.dataframe(df, use_container_width=True)

def render_grafico_individual_1(data, viz_manager):
    """Renderiza página do gráfico individual 1."""
    st.markdown("## 📋 Gráfico Individual 1")
    
    df = data.get('Grafico-Individual_1')
    if df is None or df.empty:
        st.warning("⚠️ Dados do gráfico individual 1 não disponíveis.")
        return
    
    # Usar o gerenciador de visualizações
    fig = viz_manager.criar_grafico_individual_1(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Dados detalhados
    st.markdown("### 📋 Dados Detalhados")
    st.dataframe(df, use_container_width=True)

def render_grafico_individual_2(data, viz_manager):
    """Renderiza página do gráfico individual 2."""
    st.markdown("## 📊 Gráfico Individual 2")
    
    df = data.get('Grafico-Individual_2')
    if df is None or df.empty:
        st.warning("⚠️ Dados do gráfico individual 2 não disponíveis.")
        return
    
    # Usar o gerenciador de visualizações
    fig = viz_manager.criar_grafico_individual_2(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Dados detalhados
    st.markdown("### 📋 Dados Detalhados")
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()


def render_csat_satisfacao(data, viz_manager):
    """Renderiza página de CSAT - Pesquisa de Satisfação."""
    st.markdown("## 😊 CSAT - Pesquisa de Satisfação")
    
    # Tentar carregar dados de CSAT
    processor = DataProcessor()
    dados_csat = processor.load_csat_data('/home/ubuntu/eloca-dashboard/pesquisa_satisfacao_teste.xlsx')
    
    if not dados_csat.get('sucesso'):
        st.warning("⚠️ Dados de CSAT não disponíveis.")
        st.info("💡 Carregue um arquivo de Pesquisa de Satisfação para visualizar os dados.")
        
        # Upload de arquivo
        uploaded_file = st.file_uploader(
            "Carregar Pesquisa de Satisfação", 
            type=['xlsx', 'xls'],
            help="Selecione o arquivo Excel da Pesquisa de Satisfação"
        )
        
        if uploaded_file:
            # Salvar arquivo temporário
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Processar arquivo
            dados_csat = processor.load_csat_data(temp_path)
            
            if dados_csat.get('sucesso'):
                st.success("✅ Arquivo processado com sucesso!")
            else:
                st.error(f"❌ Erro ao processar arquivo: {dados_csat.get('erro')}")
                return
        else:
            return
    
    # Exibir métricas principais
    metricas = dados_csat['metricas']
    relatorio = dados_csat['relatorio_deduplicacao']
    
    st.markdown("### 📊 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total de Respostas", metricas['total_respostas'])
    with col2:
        st.metric("😊 CSAT Score", f"{metricas['csat_score']}%")
    with col3:
        st.metric("✅ Avaliações Positivas", metricas['avaliacoes_positivas'])
    with col4:
        st.metric("❌ Avaliações Negativas", metricas['avaliacoes_negativas'])
    
    # Gráfico de distribuição de avaliações
    st.markdown("### 📈 Distribuição de Avaliações")
    
    if metricas['distribuicao_avaliacoes']:
        dist_df = pd.DataFrame(
            list(metricas['distribuicao_avaliacoes'].items()),
            columns=['Avaliação', 'Quantidade']
        )
        
        # Simplificar nomes das avaliações para o gráfico
        dist_df['Avaliacao_Simples'] = dist_df['Avaliação'].str.split(' - ').str[0]
        
        fig_dist = px.pie(
            dist_df, 
            values='Quantidade', 
            names='Avaliacao_Simples',
            title='Distribuição de Avaliações CSAT',
            color_discrete_sequence=['#2E8B57', '#32CD32', '#FFD700', '#FF6347', '#DC143C']
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Relatório de processamento
    st.markdown("### 🔧 Relatório de Processamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Estatísticas de Deduplicação:**")
        st.write(f"• Registros originais: {relatorio['registros_originais']}")
        st.write(f"• Registros finais: {relatorio['registros_finais']}")
        st.write(f"• Registros removidos: {relatorio['registros_removidos']}")
        st.write(f"• Percentual removido: {relatorio['percentual_removido']}%")
    
    with col2:
        st.markdown("**Códigos de Chamado:**")
        st.write(f"• Códigos únicos originais: {relatorio['codigos_unicos_originais']}")
        st.write(f"• Códigos únicos finais: {relatorio['codigos_unicos_finais']}")
        st.write(f"• Códigos duplicados: {relatorio['codigos_duplicados']}")
    
    # Avaliações removidas
    if relatorio.get('avaliacoes_removidas'):
        st.markdown("**Avaliações Removidas por Tipo:**")
        for avaliacao, quantidade in relatorio['avaliacoes_removidas'].items():
            st.write(f"• {avaliacao}: {quantidade}")
    
    # Dados processados
    st.markdown("### 📋 Dados Processados")
    
    df_processado = dados_csat['dados_processados']
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Analista Responsável' in df_processado.columns:
            analistas = ['Todos'] + sorted(df_processado['Analista Responsável'].unique().tolist())
            analista_selecionado = st.selectbox("Filtrar por Analista", analistas)
        else:
            analista_selecionado = 'Todos'
    
    with col2:
        if 'Área' in df_processado.columns:
            areas = ['Todas'] + sorted(df_processado['Área'].unique().tolist())
            area_selecionada = st.selectbox("Filtrar por Área", areas)
        else:
            area_selecionada = 'Todas'
    
    # Aplicar filtros
    df_filtrado = df_processado.copy()
    
    if analista_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Analista Responsável'] == analista_selecionado]
    
    if area_selecionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Área'] == area_selecionada]
    
    # Exibir dados filtrados
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Botão para download
    if not df_filtrado.empty:
        csv = df_filtrado.to_csv(index=False)
        st.download_button(
            label="📥 Download dados processados (CSV)",
            data=csv,
            file_name=f"csat_processado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

