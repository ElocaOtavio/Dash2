import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import requests
from typing import Dict, Optional, Any
import logging
from io import BytesIO
import streamlit as st # Importar streamlit para usar st.error

from config import Config
from csat_processor import CSATProcessor

logger = logging.getLogger(__name__)

class DataProcessor:
    """Classe para processar dados da planilha Eloca"""
    
    def __init__(self):
        self.config = Config()
        
    def _fetch_excel_from_url(self, url: str) -> Optional[BytesIO]:
        """
        Busca um arquivo Excel de uma URL e retorna como BytesIO.
        """
        try:
            logger.info(f"Tentando buscar arquivo Excel da URL: {url}")
            response = requests.get(url, headers=self.config.HEADERS, timeout=60) # Aumentar timeout
            response.raise_for_status() # Levanta HTTPError para 4xx/5xx respostas
            logger.info(f"Arquivo Excel da URL {url} buscado com sucesso.")
            return BytesIO(response.content)
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar arquivo Excel da URL {url}: {e}. Verifique a URL e sua conexão.")
            logger.error(f"Erro ao buscar arquivo Excel da URL {url}: {e}")
            return None
        except Exception as e:
            st.error(f"Erro inesperado ao buscar arquivo Excel da URL {url}: {e}")
            logger.error(f"Erro inesperado ao buscar arquivo Excel da URL {url}: {e}")
            return None

    def carregar_dados_completos(self) -> Optional[Dict[str, pd.DataFrame]]:
        """
        Carrega todos os dados das URLs configuradas e processa as abas do dashboard.
        """
        dados_brutos = {}
        dados_dashboard = {}

        # 1. Carregar dados do Relatório de Chamados (URL_RELATORIO_CHAMADOS)
        excel_chamados_bytes = self._fetch_excel_from_url(self.config.URL_RELATORIO_CHAMADOS)
        if excel_chamados_bytes:
            try:
                # Carrega a aba principal do relatório de chamados
                df_chamados = pd.read_excel(excel_chamados_bytes, sheet_name="Relatório_Chamados_08-04-2024_1")
                dados_brutos["Relatório_Chamados_08-04-2024_1"] = df_chamados
                logger.info(f"Aba \'Relatório_Chamados_08-04-2024_1\' carregada com {len(df_chamados)} linhas")
            except Exception as e:
                st.error(f"Erro ao carregar a aba \'Relatório_Chamados_08-04-2024_1\': {e}")
                logger.error(f"Erro ao carregar a aba \'Relatório_Chamados_08-04-2024_1\': {e}")
                dados_brutos["Relatório_Chamados_08-04-2024_1"] = pd.DataFrame()

        # 2. Carregar dados da Pesquisa de Satisfação (URL_PESQUISA_SATISFACAO)
        excel_csat_bytes = self._fetch_excel_from_url(self.config.URL_PESQUISA_SATISFACAO)
        if excel_csat_bytes:
            try:
                df_csat_raw = pd.read_excel(excel_csat_bytes, sheet_name="Pesquisa de Satisfação") # Nome da aba CSAT
                dados_brutos["Pesquisa de Satisfação"] = df_csat_raw
                logger.info(f"Aba \'Pesquisa de Satisfação\' carregada com {len(df_csat_raw)} linhas")
            except Exception as e:
                st.error(f"Erro ao carregar a aba \'Pesquisa de Satisfação\': {e}")
                logger.error(f"Erro ao carregar a aba \'Pesquisa de Satisfação\': {e}")
                dados_brutos["Pesquisa de Satisfação"] = pd.DataFrame()

        # --- Processar e Calcular as Abas do Dashboard --- #
        df_chamados = dados_brutos.get("Relatório_Chamados_08-04-2024_1", pd.DataFrame())
        df_pesquisa_satisfacao = dados_brutos.get("Pesquisa de Satisfação", pd.DataFrame())

        # Processar CSAT
        if not df_pesquisa_satisfacao.empty:
            csat_processor = CSATProcessor()
            processed_csat_data = csat_processor.processar_planilha_satisfacao_df(df_pesquisa_satisfacao)
            dados_dashboard["CSAT"] = processed_csat_data.get("dados_processados", pd.DataFrame())
            dados_dashboard["CSAT_Metricas"] = processed_csat_data.get("metricas", {})
            dados_dashboard["CSAT_Relatorio"] = processed_csat_data.get("relatorio_deduplicacao", [])
        else:
            dados_dashboard["CSAT"] = pd.DataFrame()
            dados_dashboard["CSAT_Metricas"] = {}
            dados_dashboard["CSAT_Relatorio"] = []

        # Replicar lógica das abas de cálculo a partir de df_chamados e df_pesquisa_satisfacao
        if not df_chamados.empty:
            dados_dashboard["Metas Individuais"] = self._calcular_metas_individuais(df_chamados, dados_dashboard.get("CSAT"))
            dados_dashboard["Resultados área 1"] = self._calcular_resultados_area1(df_chamados)
            dados_dashboard["Resultados área 2"] = self._calcular_resultados_area2(df_chamados)
            dados_dashboard["Grafico-Individual_1"] = self._calcular_grafico_individual_1(df_chamados)
            dados_dashboard["Grafico-Individual_2"] = self._calcular_grafico_individual_2(df_chamados)
        else:
            for aba in self.config.ABAS_DASHBOARD:
                dados_dashboard[aba] = pd.DataFrame()

        if not dados_dashboard: 
            st.error("Nenhum dado foi carregado ou processado para o dashboard. Verifique as URLs e permissões.")
            return None

        logger.info(f"Dados do dashboard carregados e processados com sucesso. {len(dados_dashboard)} abas/itens processados")
        return dados_dashboard
    
    # --- Métodos para replicar a lógica das abas de cálculo --- #

    def _calcular_metas_individuais(self, df_chamados: pd.DataFrame, df_csat_processado: pd.DataFrame) -> pd.DataFrame:
        if df_chamados.empty:
            return pd.DataFrame()
        
        # Certificar-se de que \'Data de Abertura\' é datetime
        if \'Data de Abertura\' in df_chamados.columns:
            df_chamados[\'Data de Abertura\'] = pd.to_datetime(df_chamados[\'Data de Abertura\'], errors=\'coerce\')
            df_chamados = df_chamados.dropna(subset=[\'Data de Abertura\'])

        # 1. Total Atendimentos por Analista
        total_atendimentos = df_chamados.groupby(\'Analista\')[\'Código do Chamado\'].nunique().reset_index()
        total_atendimentos.columns = [\'Analista\', \'Total Atendimentos\']

        # 2. Média Atendimento (assumindo que é por analista, se for por dia, a lógica muda)
        # Se \'Tempo de Atendimento\' for uma coluna de tempo, converter para segundos para média
        # Assumindo que \'Tempo de Atendimento\' é string \'HH:MM:SS\' ou similar
        if \'Tempo de Atendimento\' in df_chamados.columns:
            def parse_time_to_seconds(time_str):
                if pd.isna(time_str): return np.nan
                parts = str(time_str).split(\':\')
                if len(parts) == 3:
                    h, m, s = map(int, parts)
                    return h * 3600 + m * 60 + s
                return np.nan
            
            df_chamados[\'Tempo de Atendimento_seg\'] = df_chamados[\'Tempo de Atendimento\'].apply(parse_time_to_seconds)
            media_atendimento_seg = df_chamados.groupby(\'Analista\')[\'Tempo de Atendimento_seg\'].mean().reset_index()
            media_atendimento_seg.columns = [\'Analista\', \'Media Atendimento Segundos\']
            
            # Converter de volta para formato HH:MM:SS para exibição, se necessário
            def format_seconds_to_time(seconds):
                if pd.isna(seconds): return np.nan
                h = int(seconds // 3600)
                m = int((seconds % 3600) // 60)
                s = int(seconds % 60)
                return f\'{h:02d}:{m:02d}:{s:02d}\'
            
            media_atendimento_seg[\'Media Atendimento\'] = media_atendimento_seg[\'Media Atendimento Segundos\'].apply(format_seconds_to_time)
            total_atendimentos = total_atendimentos.merge(media_atendimento_seg[[\'Analista\', \'Media Atendimento\']], on=\'Analista\', how=\'left\')
        else:
            total_atendimentos[\'Media Atendimento\'] = np.nan # Se a coluna não existe

        # 3. CSAT Obtido por Analista (usando df_csat_processado)
        if df_csat_processado is not None and not df_csat_processado.empty:
            # Assumindo que df_csat_processado tem \'Analista\' e \'Atendimento - CES e CSAT - [ANALISTA] Como você avalia a qualidade do atendimento prestado pelo analista neste chamado?\'
            col_avaliacao = "Atendimento - CES e CSAT - [ANALISTA] Como você avalia a qualidade do atendimento prestado pelo analista neste chamado?"
            
            # Calcular CSAT por analista
            csat_por_analista = df_csat_processado.groupby(\'Analista\').apply(lambda x:\n                (x[col_avaliacao].astype(str).str.lower().str.startswith((\'bom\', \'ótimo\')).sum() / len(x)) * 100\n                if len(x) > 0 else 0\n            ).reset_index(name=\'CSAT Obtido\')
            
            total_atendimentos = total_atendimentos.merge(csat_por_analista, on=\'Analista\', how=\'left\')
            total_atendimentos[\'CSAT Obtido\'] = total_atendimentos[\'CSAT Obtido\'].fillna(0).round(2) # Preencher NaN com 0
        else:
            total_atendimentos[\'CSAT Obtido\'] = 0.0

        # 4. % de Respostas Obtidas (se houver uma coluna para isso ou se puder ser calculada)
        # Assumindo que \'Total Atendimentos\' é o total de chamados e \'Total Respostas\' é o total de pesquisas respondidas
        # Se não houver \'Total Respostas\', esta coluna será NaN
        # Para este exemplo, vou simular um cálculo simples ou deixar como NaN
        total_atendimentos[\'\% de Respostas Obtidas\'] = np.nan # Placeholder

        # 5. TMA Obtido (se \'Tempo de Atendimento\' for o TMA)
        # Já calculado como \'Media Atendimento\'
        total_atendimentos[\'TMA Obtido\'] = total_atendimentos[\'Media Atendimento\']

        # Adicionar colunas de Meta (fixas ou de outra fonte)
        total_atendimentos[\'Meta CSAT\'] = 98 # Exemplo: 98%\n        total_atendimentos[\'Meta \% respostas\'] = 35 # Exemplo: 35%\n        total_atendimentos[\'Meta TMA\'] = 45 # Exemplo: 45 minutos (ou segundos, dependendo da unidade)\n
        # Colunas \'Indicador\', \'Meta\', \'Atingido\' (do Excel original)\n        # Estas são colunas de resumo, podem ser calculadas ou adicionadas separadamente\n        # Para replicar o formato do Excel, podemos adicionar placeholders\n        total_atendimentos[\'Indicador\'] = np.nan\n        total_atendimentos[\'Meta\'] = np.nan\n        total_atendimentos[\'Atingido\'] = np.nan\n
        return total_atendimentos

    def _calcular_resultados_area1(self, df_chamados: pd.DataFrame) -> pd.DataFrame:
        if df_chamados.empty:
            return pd.DataFrame()
        
        # Exemplo: Contagem de chamados por \'Área\' ou \'Tipo de Atendimento\'
        # Adapte as colunas conforme seu Excel
        if \'Área\' in df_chamados.columns:
            df_area1 = df_chamados.groupby(\'Área\')[\'Código do Chamado\'].nunique().reset_index()
            df_area1.columns = [\'Área\', \'Total Chamados\']
        else:
            df_area1 = pd.DataFrame(columns=[\'Área\', \'Total Chamados\'])
            st.warning("Coluna \'Área\' não encontrada em Relatório_Chamados para Resultados área 1.")
        return df_area1

    def _calcular_resultados_area2(self, df_chamados: pd.DataFrame) -> pd.DataFrame:
        if df_chamados.empty:
            return pd.DataFrame()
        
        # Exemplo: Contagem de chamados por \'Status\' ou \'Prioridade\'
        if \'Status\' in df_chamados.columns:
            df_area2 = df_chamados.groupby(\'Status\')[\'Código do Chamado\'].nunique().reset_index()
            df_area2.columns = [\'Status\', \'Total Chamados\']
        else:
            df_area2 = pd.DataFrame(columns=[\'Status\', \'Total Chamados\'])
            st.warning("Coluna \'Status\' não encontrada em Relatório_Chamados para Resultados área 2.")
        return df_area2

    def _calcular_grafico_individual_1(self, df_chamados: pd.DataFrame) -> pd.DataFrame:
        if df_chamados.empty:
            return pd.DataFrame()
        
        # Exemplo: Chamados abertos por dia/mês por analista
        if \'Data de Abertura\' in df_chamados.columns and \'Analista\' in df_chamados.columns:
            df_chamados[\'Data de Abertura\'] = pd.to_datetime(df_chamados[\'Data de Abertura\'], errors=\'coerce\')
            df_grafico1 = df_chamados.groupby([df_chamados[\'Data de Abertura\'].dt.to_period(\'M\'), \'Analista\'])[\'Código do Chamado\'].nunique().unstack(fill_value=0)
            df_grafico1.index = df_grafico1.index.astype(str) # Para Plotly
        else:
            df_grafico1 = pd.DataFrame()
            st.warning("Colunas \'Data de Abertura\' ou \'Analista\' não encontradas para Gráfico-Individual_1.")
        return df_grafico1

    def _calcular_grafico_individual_2(self, df_chamados: pd.DataFrame) -> pd.DataFrame:
        if df_chamados.empty:
            return pd.DataFrame()
        
        # Exemplo: Chamados por tipo de atendimento por analista
        if \'Tipo de Atendimento\' in df_chamados.columns and \'Analista\' in df_chamados.columns:
            df_grafico2 = df_chamados.groupby([\'Analista\', \'Tipo de Atendimento\'])[\'Código do Chamado\'].nunique().unstack(fill_value=0)
        else:
            df_grafico2 = pd.DataFrame()
            st.warning("Colunas \'Tipo de Atendimento\' ou \'Analista\' não encontradas para Gráfico-Individual_2.")
        return df_grafico2

    # --- Funções auxiliares (manter se ainda forem usadas) ---
    def obter_aba(self, nome_aba: str) -> Optional[pd.DataFrame]:
        # Esta função agora depende do cache em app_production.py
        # O load_data em app_production.py já retorna todos os dados
        # Para manter a compatibilidade com chamadas existentes:
        dados_completos = self.carregar_dados_completos() 
        if dados_completos and nome_aba in dados_completos:
            return dados_completos[nome_aba]
        return pd.DataFrame() # Retorna DataFrame vazio se não encontrar

    def validar_dados_aba(self, df: pd.DataFrame, nome_aba: str) -> bool:
        if df is None or df.empty:
            logger.warning(f"Aba \'{nome_aba}\' está vazia ou não foi carregada")
            return False
        return True
    
    def obter_resumo_dados(self) -> Dict[str, Dict]:
        dados_completos = self.carregar_dados_completos()
        resumo = {}
        
        if dados_completos:
            for nome_aba, df in dados_completos.items():
                if isinstance(df, pd.DataFrame) and not df.empty:
                    resumo[nome_aba] = {
                        "linhas": len(df),
                        "colunas": len(df.columns),
                        "colunas_numericas": len(df.select_dtypes(include=["number"]).columns),
                        "valores_nulos": df.isnull().sum().sum(),
                        "memoria_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
                    }
                else:
                    resumo[nome_aba] = {
                        "linhas": 0,
                        "colunas": 0,
                        "colunas_numericas": 0,
                        "valores_nulos": 0,
                        "memoria_mb": 0
                    }
                    
        return resumo
    
    def limpar_cache(self):
        logger.info("Solicitação de limpeza de cache. O cache será limpo na próxima execução do app_production.")
