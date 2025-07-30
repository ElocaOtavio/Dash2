"""
Módulo para criação de visualizações do Dashboard Eloca
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np
from typing import Optional, List, Dict, Any

class VisualizationManager:
    """Gerenciador de visualizações para o dashboard"""
    
    def __init__(self):
        self.cores_padrao = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        self.tema_plotly = {
            'layout': {
                'font': {'family': 'Arial, sans-serif', 'size': 12},
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'colorway': self.cores_padrao
            }
        }
    
    def criar_grafico_metas_individuais(self, df: pd.DataFrame) -> Optional[go.Figure]:
        """
        Cria gráfico para visualização de metas individuais
        
        Args:
            df: DataFrame com dados de metas individuais
            
        Returns:
            Figura Plotly ou None se não for possível criar
        """
        if df.empty:
            st.warning("Não há dados disponíveis para Metas Individuais")
            return None
            
        try:
            # Tentar identificar colunas relevantes
            colunas = df.columns.tolist()
            
            # Buscar colunas de meta e realizado
            col_meta = None
            col_realizado = None
            col_pessoa = None
            
            for col in colunas:
                col_lower = str(col).lower()
                if 'meta' in col_lower and col_meta is None:
                    col_meta = col
                elif any(word in col_lower for word in ['realizado', 'vendido', 'resultado']) and col_realizado is None:
                    col_realizado = col
                elif any(word in col_lower for word in ['nome', 'pessoa', 'vendedor', 'funcionario']) and col_pessoa is None:
                    col_pessoa = col
            
            # Se não encontrar colunas específicas, usar as primeiras disponíveis
            if col_pessoa is None and len(colunas) > 0:
                col_pessoa = colunas[0]
            if col_meta is None and len(colunas) > 1:
                col_meta = colunas[1]
            if col_realizado is None and len(colunas) > 2:
                col_realizado = colunas[2]
            
            # Verificar se temos dados suficientes
            if not all([col_pessoa, col_meta, col_realizado]):
                st.warning("Não foi possível identificar colunas de meta e realizado")
                return self._criar_grafico_generico(df, "Metas Individuais")
            
            # Preparar dados
            df_clean = df.dropna(subset=[col_meta, col_realizado])
            
            if df_clean.empty:
                st.warning("Não há dados válidos para criar o gráfico de metas")
                return None
            
            # Calcular percentual de atingimento
            df_clean = df_clean.copy()
            df_clean['percentual'] = (pd.to_numeric(df_clean[col_realizado], errors='coerce') / 
                                    pd.to_numeric(df_clean[col_meta], errors='coerce') * 100)
            
            # Criar gráfico de barras comparativo
            fig = go.Figure()
            
            # Adicionar barras de meta
            fig.add_trace(go.Bar(
                name='Meta',
                x=df_clean[col_pessoa],
                y=pd.to_numeric(df_clean[col_meta], errors='coerce'),
                marker_color='lightblue',
                opacity=0.7
            ))
            
            # Adicionar barras de realizado
            fig.add_trace(go.Bar(
                name='Realizado',
                x=df_clean[col_pessoa],
                y=pd.to_numeric(df_clean[col_realizado], errors='coerce'),
                marker_color='darkblue'
            ))
            
            # Configurar layout
            fig.update_layout(
                title='Metas Individuais - Meta vs Realizado',
                xaxis_title='Pessoa',
                yaxis_title='Valor',
                barmode='group',
                **self.tema_plotly['layout']
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico de metas individuais: {e}")
            return self._criar_grafico_generico(df, "Metas Individuais")
    
    def criar_grafico_resultados_area(self, df: pd.DataFrame, area: str) -> Optional[go.Figure]:
        """
        Cria gráfico para resultados por área
        
        Args:
            df: DataFrame com dados de resultados
            area: Nome da área (1 ou 2)
            
        Returns:
            Figura Plotly ou None se não for possível criar
        """
        if df.empty:
            st.warning(f"Não há dados disponíveis para Resultados {area}")
            return None
            
        try:
            # Identificar colunas numéricas
            colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if not colunas_numericas:
                st.warning(f"Não há colunas numéricas em Resultados {area}")
                return self._criar_grafico_generico(df, f"Resultados {area}")
            
            # Criar gráfico de linha temporal se houver coluna de data
            colunas_data = [col for col in df.columns if any(word in str(col).lower() 
                          for word in ['data', 'mes', 'periodo', 'tempo'])]
            
            if colunas_data and len(colunas_numericas) > 0:
                return self._criar_grafico_temporal(df, colunas_data[0], colunas_numericas, f"Resultados {area}")
            else:
                # Criar gráfico de barras com as colunas numéricas
                return self._criar_grafico_barras_multiplas(df, colunas_numericas, f"Resultados {area}")
                
        except Exception as e:
            st.error(f"Erro ao criar gráfico de resultados {area}: {e}")
            return self._criar_grafico_generico(df, f"Resultados {area}")
    
    def criar_grafico_individual(self, df: pd.DataFrame, numero: str) -> Optional[go.Figure]:
        """
        Cria gráfico individual específico
        
        Args:
            df: DataFrame com dados
            numero: Número do gráfico (1 ou 2)
            
        Returns:
            Figura Plotly ou None se não for possível criar
        """
        if df.empty:
            st.warning(f"Não há dados disponíveis para Gráfico Individual {numero}")
            return None
            
        try:
            # Para gráficos individuais, criar visualizações mais específicas
            colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(colunas_numericas) >= 2:
                # Criar gráfico de dispersão se tiver pelo menos 2 colunas numéricas
                return self._criar_grafico_dispersao(df, colunas_numericas, f"Gráfico Individual {numero}")
            elif len(colunas_numericas) == 1:
                # Criar histograma se tiver apenas 1 coluna numérica
                return self._criar_histograma(df, colunas_numericas[0], f"Gráfico Individual {numero}")
            else:
                # Criar gráfico genérico
                return self._criar_grafico_generico(df, f"Gráfico Individual {numero}")
                
        except Exception as e:
            st.error(f"Erro ao criar gráfico individual {numero}: {e}")
            return self._criar_grafico_generico(df, f"Gráfico Individual {numero}")
    
    def _criar_grafico_temporal(self, df: pd.DataFrame, col_data: str, 
                               colunas_numericas: List[str], titulo: str) -> go.Figure:
        """Cria gráfico temporal (linha)"""
        fig = go.Figure()
        
        for col in colunas_numericas[:5]:  # Limitar a 5 séries
            fig.add_trace(go.Scatter(
                x=df[col_data],
                y=pd.to_numeric(df[col], errors='coerce'),
                mode='lines+markers',
                name=col,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title=f'{titulo} - Evolução Temporal',
            xaxis_title=col_data,
            yaxis_title='Valor',
            **self.tema_plotly['layout']
        )
        
        return fig
    
    def _criar_grafico_barras_multiplas(self, df: pd.DataFrame, 
                                       colunas_numericas: List[str], titulo: str) -> go.Figure:
        """Cria gráfico de barras múltiplas"""
        fig = go.Figure()
        
        # Usar índice como eixo X se não houver coluna categórica clara
        x_values = df.index if len(df) <= 20 else df.index[:20]  # Limitar a 20 itens
        
        for i, col in enumerate(colunas_numericas[:5]):  # Limitar a 5 séries
            fig.add_trace(go.Bar(
                name=col,
                x=x_values,
                y=pd.to_numeric(df[col].iloc[:20], errors='coerce'),
                marker_color=self.cores_padrao[i % len(self.cores_padrao)]
            ))
        
        fig.update_layout(
            title=f'{titulo} - Comparativo',
            xaxis_title='Registro',
            yaxis_title='Valor',
            barmode='group',
            **self.tema_plotly['layout']
        )
        
        return fig
    
    def _criar_grafico_dispersao(self, df: pd.DataFrame, 
                                colunas_numericas: List[str], titulo: str) -> go.Figure:
        """Cria gráfico de dispersão"""
        fig = px.scatter(
            df,
            x=colunas_numericas[0],
            y=colunas_numericas[1],
            title=f'{titulo} - Correlação',
            template='plotly_white'
        )
        
        fig.update_layout(**self.tema_plotly['layout'])
        return fig
    
    def _criar_histograma(self, df: pd.DataFrame, coluna: str, titulo: str) -> go.Figure:
        """Cria histograma"""
        fig = px.histogram(
            df,
            x=coluna,
            title=f'{titulo} - Distribuição de {coluna}',
            template='plotly_white'
        )
        
        fig.update_layout(**self.tema_plotly['layout'])
        return fig
    
    def _criar_grafico_generico(self, df: pd.DataFrame, titulo: str) -> go.Figure:
        """Cria gráfico genérico quando não é possível identificar padrão específico"""
        fig = go.Figure()
        
        # Mostrar informações básicas sobre os dados
        fig.add_annotation(
            text=f"Dados carregados: {len(df)} linhas, {len(df.columns)} colunas<br>" +
                 f"Colunas: {', '.join(df.columns[:5].tolist())}" +
                 ("..." if len(df.columns) > 5 else ""),
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14)
        )
        
        fig.update_layout(
            title=f'{titulo} - Dados Carregados',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            **self.tema_plotly['layout']
        )
        
        return fig
    
    def criar_dashboard_resumo(self, resumo_dados: Dict[str, Dict]) -> go.Figure:
        """
        Cria gráfico de resumo geral dos dados
        
        Args:
            resumo_dados: Dicionário com resumo de cada aba
            
        Returns:
            Figura Plotly com resumo
        """
        if not resumo_dados:
            return None
            
        abas = list(resumo_dados.keys())
        linhas = [resumo_dados[aba]['linhas'] for aba in abas]
        colunas = [resumo_dados[aba]['colunas'] for aba in abas]
        
        # Criar subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Número de Linhas por Aba', 'Número de Colunas por Aba'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Adicionar gráfico de linhas
        fig.add_trace(
            go.Bar(x=abas, y=linhas, name='Linhas', marker_color='lightblue'),
            row=1, col=1
        )
        
        # Adicionar gráfico de colunas
        fig.add_trace(
            go.Bar(x=abas, y=colunas, name='Colunas', marker_color='lightcoral'),
            row=1, col=2
        )
        
        fig.update_layout(
            title='Resumo Geral dos Dados',
            showlegend=False,
            **self.tema_plotly['layout']
        )
        
        return fig

