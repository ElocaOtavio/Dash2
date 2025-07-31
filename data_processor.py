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
        
        # Certificar-se de que 'Data de Abertura' é datetime
        if 'Data de Abertura' in df_chamados.columns:
            df_chamados['Data de Abertura'] = pd.to_datetime(df_chamados['Data de Abertura'], errors='coerce')
            df_chamados = df_chamados.dropna(subset=['Data de Abertura'])

        # 1. Total Atendimentos por Analista
        total_atendimentos = df_chamados.groupby('Analista')['Código do Chamado'].nunique().reset_index()
        total_atendimentos.columns = ['Analista', 'Total Atendimentos']

        # 2. Média Atendimento (assumindo que é por dia ou período, aqui farei por analista)
        # Se 
