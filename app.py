"""
Dashboard Eloca - Sistema de Gestão de Vendas
Aplicação principal Streamlit
"""
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Importar módulos locais
from config import Config
from data_processor import DataProcessor
from visualizations import VisualizationManager

# Configuração da página
st.set_page_config(
    page_title="Dashboard Eloca - Gestão de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    
    .sidebar-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .data-table {
        font-size: 0.9rem;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DashboardApp:
    """Classe principal da aplicação Dashboard"""
    
    def __init__(self):
        self.config = Config()
        self.data_processor = DataProcessor()
        self.viz_manager = VisualizationManager()
        
        # Verificar configuração
        try:
            self.config.validate_config()
            self.config_valida = True
        except ValueError as e:
            self.config_valida = False
            self.erro_config = str(e)
    
    def run(self):
        """Executa a aplicação principal"""
        
        # Header principal
        st.markdown('<div class="main-header">📊 Dashboard Eloca - Gestão de Vendas</div>', 
                   unsafe_allow_html=True)
        
        # Verificar configuração
        if not self.config_valida:
            st.error(f"❌ Erro de configuração: {self.erro_config}")
            st.info("💡 Configure as variáveis de ambiente ELOCA_URL e DESKMANAGER_TOKEN")
            self._mostrar_configuracao()
            return
        
        # Sidebar com informações e controles
        self._criar_sidebar()
        
        # Menu principal
        menu_selecionado = option_menu(
            menu_title=None,
            options=["📊 Resumo Geral", "🎯 Metas Individuais", "📈 Resultados Área 1", 
                    "📉 Resultados Área 2", "📋 Gráfico Individual 1", "📊 Gráfico Individual 2"],
            icons=["house", "target", "graph-up", "graph-down", "bar-chart", "pie-chart"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#1f77b4", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", 
                           "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#1f77b4"},
            }
        )
        
        # Carregar dados
        with st.spinner("🔄 Carregando dados..."):
            dados_completos = self.data_processor.carregar_dados_completos()
        
        if dados_completos is None:
            st.error("❌ Não foi possível carregar os dados. Verifique a conexão e configurações.")
            return
        
        # Renderizar página selecionada
        if menu_selecionado == "📊 Resumo Geral":
            self._pagina_resumo_geral(dados_completos)
        elif menu_selecionado == "🎯 Metas Individuais":
            self._pagina_metas_individuais(dados_completos)
        elif menu_selecionado == "📈 Resultados Área 1":
            self._pagina_resultados_area(dados_completos, "1")
        elif menu_selecionado == "📉 Resultados Área 2":
            self._pagina_resultados_area(dados_completos, "2")
        elif menu_selecionado == "📋 Gráfico Individual 1":
            self._pagina_grafico_individual(dados_completos, "1")
        elif menu_selecionado == "📊 Gráfico Individual 2":
            self._pagina_grafico_individual(dados_completos, "2")
    
    def _criar_sidebar(self):
        """Cria sidebar com informações e controles"""
        with st.sidebar:
            st.markdown("### ⚙️ Controles")
            
            # Botão para atualizar dados
            if st.button("🔄 Atualizar Dados", type="primary"):
                self.data_processor.limpar_cache()
                st.rerun()
            
            # Informações de status
            st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
            st.markdown("### 📊 Status do Sistema")
            
            if self.config_valida:
                st.markdown('<span class="status-success">✅ Configuração OK</span>', 
                           unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-error">❌ Erro de Configuração</span>', 
                           unsafe_allow_html=True)
            
            # Timestamp da última atualização
            st.markdown(f"**Última atualização:** {datetime.now().strftime('%H:%M:%S')}")
            st.markdown(f"**Cache TTL:** {self.config.CACHE_TTL // 60} minutos")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Informações sobre as abas
            st.markdown("### 📋 Abas Disponíveis")
            for aba in self.config.ABAS_PLANILHA:
                st.markdown(f"• {aba}")
            
            # Debug info (se habilitado)
            if self.config.DEBUG_MODE:
                st.markdown("### 🐛 Debug Info")
                st.json({
                    "URL configurada": bool(self.config.ELOCA_URL),
                    "Token configurado": bool(self.config.DESKMANAGER_TOKEN),
                    "Cache TTL": self.config.CACHE_TTL
                })
    
    def _pagina_resumo_geral(self, dados_completos):
        """Página de resumo geral dos dados"""
        st.markdown("## 📊 Resumo Geral dos Dados")
        
        # Obter resumo estatístico
        resumo = self.data_processor.obter_resumo_dados()
        
        if not resumo:
            st.warning("Não há dados para exibir no resumo")
            return
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        total_linhas = sum(aba['linhas'] for aba in resumo.values())
        total_colunas = sum(aba['colunas'] for aba in resumo.values())
        abas_com_dados = len([aba for aba in resumo.values() if aba['linhas'] > 0])
        memoria_total = sum(aba['memoria_mb'] for aba in resumo.values())
        
        with col1:
            st.metric("📊 Total de Linhas", f"{total_linhas:,}")
        with col2:
            st.metric("📋 Total de Colunas", f"{total_colunas:,}")
        with col3:
            st.metric("✅ Abas com Dados", f"{abas_com_dados}/{len(resumo)}")
        with col4:
            st.metric("💾 Memória Total", f"{memoria_total:.1f} MB")
        
        # Gráfico de resumo
        fig_resumo = self.viz_manager.criar_dashboard_resumo(resumo)
        if fig_resumo:
            st.plotly_chart(fig_resumo, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("### 📋 Detalhes por Aba")
        
        df_resumo = pd.DataFrame(resumo).T
        df_resumo.index.name = "Aba"
        df_resumo = df_resumo.reset_index()
        
        st.dataframe(
            df_resumo,
            use_container_width=True,
            column_config={
                "Aba": st.column_config.TextColumn("Aba", width="medium"),
                "linhas": st.column_config.NumberColumn("Linhas", format="%d"),
                "colunas": st.column_config.NumberColumn("Colunas", format="%d"),
                "colunas_numericas": st.column_config.NumberColumn("Cols. Numéricas", format="%d"),
                "valores_nulos": st.column_config.NumberColumn("Valores Nulos", format="%d"),
                "memoria_mb": st.column_config.NumberColumn("Memória (MB)", format="%.2f")
            }
        )
    
    def _pagina_metas_individuais(self, dados_completos):
        """Página de metas individuais"""
        st.markdown("## 🎯 Metas Individuais")
        
        df = dados_completos.get("Metas Individuais", pd.DataFrame())
        
        if df.empty:
            st.warning("Não há dados disponíveis para Metas Individuais")
            return
        
        # Validar dados
        if not self.data_processor.validar_dados_aba(df, "Metas Individuais"):
            st.warning("Os dados de Metas Individuais podem estar incompletos")
        
        # Mostrar informações básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total de Registros", len(df))
        with col2:
            st.metric("📋 Colunas", len(df.columns))
        with col3:
            colunas_numericas = len(df.select_dtypes(include=['number']).columns)
            st.metric("🔢 Colunas Numéricas", colunas_numericas)
        
        # Criar visualização
        fig = self.viz_manager.criar_grafico_metas_individuais(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar dados tabulares
        st.markdown("### 📋 Dados Detalhados")
        st.dataframe(df, use_container_width=True)
        
        # Análise adicional se houver colunas numéricas
        if colunas_numericas > 0:
            st.markdown("### 📊 Estatísticas Descritivas")
            st.dataframe(df.describe(), use_container_width=True)
    
    def _pagina_resultados_area(self, dados_completos, area):
        """Página de resultados por área"""
        st.markdown(f"## 📈 Resultados Área {area}")
        
        nome_aba = f"Resultados área {area}"
        df = dados_completos.get(nome_aba, pd.DataFrame())
        
        if df.empty:
            st.warning(f"Não há dados disponíveis para {nome_aba}")
            return
        
        # Validar dados
        if not self.data_processor.validar_dados_aba(df, nome_aba):
            st.warning(f"Os dados de {nome_aba} podem estar incompletos")
        
        # Mostrar informações básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total de Registros", len(df))
        with col2:
            st.metric("📋 Colunas", len(df.columns))
        with col3:
            colunas_numericas = len(df.select_dtypes(include=['number']).columns)
            st.metric("🔢 Colunas Numéricas", colunas_numericas)
        
        # Criar visualização
        fig = self.viz_manager.criar_grafico_resultados_area(df, area)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Filtros interativos se houver dados suficientes
        if len(df) > 10 and colunas_numericas > 0:
            st.markdown("### 🔍 Filtros Interativos")
            
            # Filtro por número de registros
            max_registros = st.slider(
                "Número máximo de registros a exibir",
                min_value=5,
                max_value=min(len(df), 100),
                value=min(len(df), 20)
            )
            
            df_filtrado = df.head(max_registros)
        else:
            df_filtrado = df
        
        # Mostrar dados tabulares
        st.markdown("### 📋 Dados Detalhados")
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Análise adicional
        if colunas_numericas > 0:
            st.markdown("### 📊 Estatísticas Descritivas")
            st.dataframe(df.describe(), use_container_width=True)
    
    def _pagina_grafico_individual(self, dados_completos, numero):
        """Página de gráfico individual"""
        st.markdown(f"## 📊 Gráfico Individual {numero}")
        
        nome_aba = f"Grafico-Individual_{numero}"
        df = dados_completos.get(nome_aba, pd.DataFrame())
        
        if df.empty:
            st.warning(f"Não há dados disponíveis para {nome_aba}")
            return
        
        # Validar dados
        if not self.data_processor.validar_dados_aba(df, nome_aba):
            st.warning(f"Os dados de {nome_aba} podem estar incompletos")
        
        # Mostrar informações básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total de Registros", len(df))
        with col2:
            st.metric("📋 Colunas", len(df.columns))
        with col3:
            colunas_numericas = len(df.select_dtypes(include=['number']).columns)
            st.metric("🔢 Colunas Numéricas", colunas_numericas)
        
        # Opções de visualização
        if colunas_numericas > 0:
            st.markdown("### ⚙️ Opções de Visualização")
            
            col_viz1, col_viz2 = st.columns(2)
            
            with col_viz1:
                tipo_grafico = st.selectbox(
                    "Tipo de Gráfico",
                    ["Automático", "Barras", "Linha", "Dispersão", "Histograma", "Box Plot"]
                )
            
            with col_viz2:
                if colunas_numericas > 1:
                    colunas_selecionadas = st.multiselect(
                        "Colunas para Visualizar",
                        df.select_dtypes(include=['number']).columns.tolist(),
                        default=df.select_dtypes(include=['number']).columns.tolist()[:3]
                    )
                else:
                    colunas_selecionadas = df.select_dtypes(include=['number']).columns.tolist()
        
        # Criar visualização
        if tipo_grafico == "Automático":
            fig = self.viz_manager.criar_grafico_individual(df, numero)
        else:
            fig = self._criar_grafico_customizado(df, tipo_grafico, colunas_selecionadas, numero)
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar dados tabulares
        st.markdown("### 📋 Dados Detalhados")
        st.dataframe(df, use_container_width=True)
        
        # Análise adicional
        if colunas_numericas > 0:
            st.markdown("### 📊 Estatísticas Descritivas")
            st.dataframe(df.describe(), use_container_width=True)
    
    def _criar_grafico_customizado(self, df, tipo_grafico, colunas, numero):
        """Cria gráfico customizado baseado na seleção do usuário"""
        if not colunas:
            st.warning("Selecione pelo menos uma coluna para visualizar")
            return None
        
        try:
            if tipo_grafico == "Barras":
                fig = px.bar(df, y=colunas[0], title=f"Gráfico Individual {numero} - Barras")
            elif tipo_grafico == "Linha":
                fig = px.line(df, y=colunas, title=f"Gráfico Individual {numero} - Linha")
            elif tipo_grafico == "Dispersão" and len(colunas) >= 2:
                fig = px.scatter(df, x=colunas[0], y=colunas[1], 
                               title=f"Gráfico Individual {numero} - Dispersão")
            elif tipo_grafico == "Histograma":
                fig = px.histogram(df, x=colunas[0], title=f"Gráfico Individual {numero} - Histograma")
            elif tipo_grafico == "Box Plot":
                fig = px.box(df, y=colunas, title=f"Gráfico Individual {numero} - Box Plot")
            else:
                return self.viz_manager.criar_grafico_individual(df, numero)
            
            fig.update_layout(**self.viz_manager.tema_plotly['layout'])
            return fig
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico customizado: {e}")
            return self.viz_manager.criar_grafico_individual(df, numero)
    
    def _mostrar_configuracao(self):
        """Mostra instruções de configuração"""
        st.markdown("### 🔧 Como Configurar")
        
        st.markdown("""
        Para usar este dashboard, você precisa configurar as seguintes variáveis de ambiente:
        
        **No Streamlit Cloud:**
        1. Vá em Settings > Secrets
        2. Adicione as seguintes variáveis:
        
        ```toml
        ELOCA_URL = "https://eloca.desk.ms/Relatorios/excel?token=SEU_TOKEN"
        DESKMANAGER_TOKEN = "SEU_VALOR_DO_HEADER"
        ```
        
        **Localmente:**
        1. Crie um arquivo `.env` na raiz do projeto
        2. Adicione as variáveis conforme o exemplo em `.env.example`
        """)

# Executar aplicação
if __name__ == "__main__":
    app = DashboardApp()
    app.run()

