"""
Dashboard Eloca - Versão de Teste
Aplicação Streamlit para testes locais
"""
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Importar módulos locais (versão de teste)
from config import Config
from data_processor_test import DataProcessorTest
from visualizations import VisualizationManager

# Configuração da página
st.set_page_config(
    page_title="Dashboard Eloca - Teste",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
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
    
    .test-banner {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        color: #856404;
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
</style>
""", unsafe_allow_html=True)

class DashboardTestApp:
    """Classe principal da aplicação de teste"""
    
    def __init__(self):
        self.config = Config()
        self.data_processor = DataProcessorTest()
        self.viz_manager = VisualizationManager()
        
        # Para testes, sempre considerar configuração válida
        self.config_valida = True
    
    def run(self):
        """Executa a aplicação de teste"""
        
        # Banner de teste
        st.markdown("""
        <div class="test-banner">
            🧪 <strong>MODO DE TESTE</strong> - Usando dados simulados para demonstração
        </div>
        """, unsafe_allow_html=True)
        
        # Header principal
        st.markdown('<div class="main-header">🧪 Dashboard Eloca - Teste com Dados Simulados</div>', 
                   unsafe_allow_html=True)
        
        # Sidebar com informações
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
        
        # Carregar dados de teste
        with st.spinner("🔄 Carregando dados de teste..."):
            dados_completos = self.data_processor.carregar_dados_completos()
        
        if dados_completos is None:
            st.error("❌ Não foi possível carregar os dados de teste.")
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
        """Cria sidebar com informações de teste"""
        with st.sidebar:
            st.markdown("### 🧪 Controles de Teste")
            
            # Botão para atualizar dados
            if st.button("🔄 Regenerar Dados de Teste", type="primary"):
                self._regenerar_dados_teste()
                self.data_processor.limpar_cache()
                st.rerun()
            
            # Informações de status
            st.markdown("### 📊 Status do Sistema")
            st.markdown('<span class="status-success">✅ Modo de Teste Ativo</span>', 
                       unsafe_allow_html=True)
            st.markdown('<span class="status-success">✅ Dados Simulados OK</span>', 
                       unsafe_allow_html=True)
            
            # Timestamp
            st.markdown(f"**Última atualização:** {datetime.now().strftime('%H:%M:%S')}")
            
            # Informações sobre os dados de teste
            st.markdown("### 📋 Dados de Teste")
            st.markdown("• Metas Individuais (10 registros)")
            st.markdown("• Resultados área 1 (15 registros)")
            st.markdown("• Resultados área 2 (15 registros)")
            st.markdown("• Gráfico Individual 1 (20 registros)")
            st.markdown("• Gráfico Individual 2 (20 registros)")
            
            # Informações técnicas
            st.markdown("### 🔧 Info Técnica")
            st.markdown("**Fonte:** Arquivo Excel local")
            st.markdown("**Cache:** 60 segundos")
            st.markdown("**Debug:** Habilitado")
    
    def _regenerar_dados_teste(self):
        """Regenera os dados de teste"""
        try:
            from test_data_generator import TestDataGenerator
            generator = TestDataGenerator()
            generator.salvar_excel_teste("/home/ubuntu/eloca-dashboard/dados_teste.xlsx")
            st.success("✅ Dados de teste regenerados com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao regenerar dados: {e}")
    
    def _pagina_resumo_geral(self, dados_completos):
        """Página de resumo geral dos dados de teste"""
        st.markdown("## 📊 Resumo Geral dos Dados de Teste")
        
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
        
        st.dataframe(df_resumo, use_container_width=True)
        
        # Informações sobre os dados de teste
        st.markdown("### 🧪 Sobre os Dados de Teste")
        st.info("""
        **Dados Simulados:** Estes dados foram gerados automaticamente para demonstrar 
        as funcionalidades do dashboard. Incluem:
        
        - **Metas Individuais:** Vendedores fictícios com metas e realizações
        - **Resultados por Área:** Dados de vendas diárias das últimas 2 semanas
        - **Gráficos Individuais:** Análises de produtos e performance de vendedores
        
        Os dados são regenerados a cada execução para simular variações reais.
        """)
    
    def _pagina_metas_individuais(self, dados_completos):
        """Página de metas individuais com dados de teste"""
        st.markdown("## 🎯 Metas Individuais (Dados de Teste)")
        
        df = dados_completos.get("Metas Individuais", pd.DataFrame())
        
        if df.empty:
            st.warning("Não há dados de teste disponíveis para Metas Individuais")
            return
        
        # Mostrar informações básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total de Vendedores", len(df))
        with col2:
            meta_total = df["Meta_Mensal"].sum() if "Meta_Mensal" in df.columns else 0
            st.metric("🎯 Meta Total", f"R$ {meta_total:,.0f}")
        with col3:
            realizado_total = df["Realizado"].sum() if "Realizado" in df.columns else 0
            st.metric("💰 Realizado Total", f"R$ {realizado_total:,.0f}")
        
        # Criar visualização
        fig = self.viz_manager.criar_grafico_metas_individuais(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Análise de performance
        if "Percentual_Atingimento" in df.columns:
            st.markdown("### 📈 Análise de Performance")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Vendedores acima da meta
                acima_meta = len(df[df["Percentual_Atingimento"] >= 100])
                st.metric("✅ Acima da Meta", f"{acima_meta}/{len(df)}")
                
                # Melhor performance
                melhor_idx = df["Percentual_Atingimento"].idxmax()
                melhor_vendedor = df.loc[melhor_idx, "Nome"]
                melhor_perc = df.loc[melhor_idx, "Percentual_Atingimento"]
                st.metric("🏆 Melhor Performance", f"{melhor_vendedor} ({melhor_perc:.1f}%)")
            
            with col2:
                # Performance média
                perc_medio = df["Percentual_Atingimento"].mean()
                st.metric("📊 Performance Média", f"{perc_medio:.1f}%")
                
                # Gráfico de distribuição
                fig_dist = px.histogram(
                    df, 
                    x="Percentual_Atingimento", 
                    title="Distribuição de Performance",
                    nbins=10
                )
                fig_dist.update_layout(height=300)
                st.plotly_chart(fig_dist, use_container_width=True)
        
        # Mostrar dados tabulares
        st.markdown("### 📋 Dados Detalhados")
        st.dataframe(df, use_container_width=True)
    
    def _pagina_resultados_area(self, dados_completos, area):
        """Página de resultados por área com dados de teste"""
        st.markdown(f"## 📈 Resultados Área {area} (Dados de Teste)")
        
        nome_aba = f"Resultados área {area}"
        df = dados_completos.get(nome_aba, pd.DataFrame())
        
        if df.empty:
            st.warning(f"Não há dados de teste disponíveis para {nome_aba}")
            return
        
        # Mostrar informações básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Dias de Dados", len(df))
        with col2:
            vendas_total = df["Vendas_Diarias"].sum() if "Vendas_Diarias" in df.columns else 0
            st.metric("💰 Vendas Totais", f"R$ {vendas_total:,.0f}")
        with col3:
            if "Ticket_Medio" in df.columns:
                ticket_medio = df["Ticket_Medio"].mean()
                st.metric("🎫 Ticket Médio", f"R$ {ticket_medio:.0f}")
        
        # Criar visualização
        fig = self.viz_manager.criar_grafico_resultados_area(df, area)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Análise temporal se houver dados de data
        if "Data" in df.columns:
            st.markdown("### 📅 Análise Temporal")
            
            # Gráfico de evolução das vendas
            fig_evolucao = px.line(
                df, 
                x="Data", 
                y="Vendas_Diarias",
                title=f"Evolução das Vendas - Área {area}",
                markers=True
            )
            fig_evolucao.add_hline(
                y=df["Meta_Diaria"].iloc[0] if "Meta_Diaria" in df.columns else 15000,
                line_dash="dash",
                line_color="red",
                annotation_text="Meta Diária"
            )
            st.plotly_chart(fig_evolucao, use_container_width=True)
        
        # Mostrar dados tabulares
        st.markdown("### 📋 Dados Detalhados")
        st.dataframe(df, use_container_width=True)
    
    def _pagina_grafico_individual(self, dados_completos, numero):
        """Página de gráfico individual com dados de teste"""
        st.markdown(f"## 📊 Gráfico Individual {numero} (Dados de Teste)")
        
        nome_aba = f"Grafico-Individual_{numero}"
        df = dados_completos.get(nome_aba, pd.DataFrame())
        
        if df.empty:
            st.warning(f"Não há dados de teste disponíveis para {nome_aba}")
            return
        
        # Mostrar informações básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total de Registros", len(df))
        with col2:
            st.metric("📋 Colunas", len(df.columns))
        with col3:
            colunas_numericas = len(df.select_dtypes(include=['number']).columns)
            st.metric("🔢 Colunas Numéricas", colunas_numericas)
        
        # Criar visualização principal
        fig = self.viz_manager.criar_grafico_individual(df, numero)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Análises específicas por gráfico
        if numero == "1" and "Valor_Total" in df.columns:
            st.markdown("### 💰 Análise de Vendas por Produto")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top produtos por valor
                top_produtos = df.groupby("Produto")["Valor_Total"].sum().sort_values(ascending=False).head(5)
                fig_top = px.bar(
                    x=top_produtos.index,
                    y=top_produtos.values,
                    title="Top 5 Produtos por Valor"
                )
                st.plotly_chart(fig_top, use_container_width=True)
            
            with col2:
                # Distribuição por categoria
                if "Categoria" in df.columns:
                    cat_vendas = df.groupby("Categoria")["Valor_Total"].sum()
                    fig_cat = px.pie(
                        values=cat_vendas.values,
                        names=cat_vendas.index,
                        title="Vendas por Categoria"
                    )
                    st.plotly_chart(fig_cat, use_container_width=True)
        
        elif numero == "2" and "Performance_Score" in df.columns:
            st.markdown("### 🏆 Análise de Performance de Vendedores")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top vendedores
                top_vendedores = df.nlargest(5, "Performance_Score")[["Vendedor", "Performance_Score"]]
                fig_top = px.bar(
                    top_vendedores,
                    x="Vendedor",
                    y="Performance_Score",
                    title="Top 5 Vendedores por Performance"
                )
                st.plotly_chart(fig_top, use_container_width=True)
            
            with col2:
                # Performance por região
                if "Regiao" in df.columns:
                    perf_regiao = df.groupby("Regiao")["Performance_Score"].mean()
                    fig_regiao = px.bar(
                        x=perf_regiao.index,
                        y=perf_regiao.values,
                        title="Performance Média por Região"
                    )
                    st.plotly_chart(fig_regiao, use_container_width=True)
        
        # Mostrar dados tabulares
        st.markdown("### 📋 Dados Detalhados")
        st.dataframe(df, use_container_width=True)

# Executar aplicação de teste
if __name__ == "__main__":
    app = DashboardTestApp()
    app.run()

