import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import requests
from typing import Dict, Optional, Any
import logging
from io import BytesIO

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
            logger.error(f"Erro ao buscar arquivo Excel da URL {url}: {e}")
            return None

    def carregar_dados_completos(self) -> Dict[str, pd.DataFrame]:
        """
        Carrega todos os dados das URLs configuradas e processa as abas.
        Retorna um dicionário com DataFrames processados para cada aba do dashboard e CSAT.
        """
        dados_dashboard = {}
        df_chamados = pd.DataFrame()
        df_pesquisa_satisfacao = pd.DataFrame()

        # 1. Carregar Relatório de Chamados
        excel_chamados_bytes = self._fetch_excel_from_url(self.config.URL_RELATORIO_CHAMADOS)
        if excel_chamados_bytes:
            try:
                # Apenas a aba 'Relatório_Chamados_08-04-2024_1' será lida deste arquivo
                df_chamados = pd.read_excel(excel_chamados_bytes, sheet_name="Relatório_Chamados_08-04-2024_1")
                logger.info(f"Aba 'Relatório_Chamados_08-04-2024_1' carregada com {len(df_chamados)} linhas.")
            except Exception as e:
                logger.error(f"Erro ao ler aba 'Relatório_Chamados_08-04-2024_1' do URL_RELATORIO_CHAMADOS: {e}")
        else:
            logger.warning("Não foi possível carregar o arquivo de Relatório de Chamados da URL.")

        # 2. Carregar Pesquisa de Satisfação (CSAT)
        excel_pesquisa_bytes = self._fetch_excel_from_url(self.config.URL_PESQUISA_SATISFACAO)
        if excel_pesquisa_bytes:
            try:
                # Apenas a aba 'Pesquisa de Satisfação' será lida deste arquivo
                df_pesquisa_satisfacao = pd.read_excel(excel_pesquisa_bytes, sheet_name="Pesquisa de Satisfação")
                logger.info(f"Aba 'Pesquisa de Satisfação' carregada com {len(df_pesquisa_satisfacao)} linhas.")
                # Processar CSAT imediatamente
                csat_processor = CSATProcessor()
                dados_dashboard["CSAT"] = csat_processor.processar_planilha_satisfacao_df(df_pesquisa_satisfacao)
                logger.info(f"Dados CSAT processados com {len(dados_dashboard['CSAT'])} linhas.")
            except Exception as e:
                logger.error(f"Erro ao ler aba 'Pesquisa de Satisfação' do URL_PESQUISA_SATISFACAO: {e}")
        else:
            logger.warning("Não foi possível carregar o arquivo de Pesquisa de Satisfação da URL.")

        # 3. Calcular as abas do dashboard a partir dos dados brutos
        if not df_chamados.empty:
            dados_dashboard["Metas Individuais"] = self._calcular_metas_individuais(df_chamados, dados_dashboard.get("CSAT", pd.DataFrame()))
            dados_dashboard["Resultados área 1"] = self._calcular_resultados_area1(df_chamados)
            dados_dashboard["Resultados área 2"] = self._calcular_resultados_area2(df_chamados)
            dados_dashboard["Grafico-Individual_1"] = self._calcular_grafico_individual_1(df_chamados)
            dados_dashboard["Grafico-Individual_2"] = self._calcular_grafico_individual_2(df_chamados)
        else:
            logger.warning("DataFrame de chamados vazio. Não foi possível calcular as abas do dashboard.")
            for aba in self.config.ABAS_DASHBOARD:
                dados_dashboard[aba] = pd.DataFrame()

        if not dados_dashboard: 
            logger.error("Nenhum dado foi carregado ou processado para o dashboard. Verifique as URLs e permissões.")
            return {}

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

        # 2. Média Atendimento (assumindo que é por período, aqui farei por analista)
        # Para TMA, TME, TMR, preciso das colunas de tempo. Vou assumir que existem ou calcular a partir de datas.
        # Se 'Tempo de Atendimento' existe e é numérico
        if 'Tempo de Atendimento' in df_chamados.columns and pd.api.types.is_numeric_dtype(df_chamados['Tempo de Atendimento']):
            media_atendimento = df_chamados.groupby('Analista')['Tempo de Atendimento'].mean().reset_index()
            media_atendimento.columns = ['Analista', 'Media Atendimento']
        else:
            media_atendimento = pd.DataFrame({'Analista': df_chamados['Analista'].unique(), 'Media Atendimento': 'N/A'})

        # 3. CSAT Obtido (usar o df_csat_processado)
        if not df_csat_processado.empty and 'Analista' in df_csat_processado.columns and 'CSAT' in df_csat_processado.columns:
            csat_obtido = df_csat_processado.groupby('Analista')['CSAT'].mean().reset_index()
            csat_obtido.columns = ['Analista', 'CSAT Obtido']
        else:
            csat_obtido = pd.DataFrame({'Analista': df_chamados['Analista'].unique(), 'CSAT Obtido': 'N/A'})

        # 4. % Resposta Pesquisa (assumindo que df_csat_processado tem 'Total Pesquisas' e 'Respostas')
        if not df_csat_processado.empty and 'Analista' in df_csat_processado.columns and 'Total Pesquisas' in df_csat_processado.columns and 'Respostas' in df_csat_processado.columns:
            respostas_pesquisa = df_csat_processado.groupby('Analista').agg(
                Total_Pesquisas=('Total Pesquisas', 'sum'),
                Respostas=('Respostas', 'sum')
            ).reset_index()
            respostas_pesquisa['Percentual_Resposta_Pesquisa'] = (respostas_pesquisa['Respostas'] / respostas_pesquisa['Total_Pesquisas']) * 100
            respostas_pesquisa = respostas_pesquisa[['Analista', 'Percentual_Resposta_Pesquisa']]
        else:
            respostas_pesquisa = pd.DataFrame({'Analista': df_chamados['Analista'].unique(), 'Percentual_Resposta_Pesquisa': 'N/A'})

        # 5. SLA 1º Atendimento e SLA Resolução (assumindo colunas de SLA no df_chamados)
        # Se 'SLA 1º Atendimento' e 'SLA Resolução' existem e são numéricas (representando %)
        if 'SLA 1º Atendimento' in df_chamados.columns and pd.api.types.is_numeric_dtype(df_chamados['SLA 1º Atendimento']):
            sla_primeiro = df_chamados.groupby('Analista')['SLA 1º Atendimento'].mean().reset_index()
            sla_primeiro.columns = ['Analista', 'SLA 1º Atendimento']
        else:
            sla_primeiro = pd.DataFrame({'Analista': df_chamados['Analista'].unique(), 'SLA 1º Atendimento': 'N/A'})

        if 'SLA Resolução' in df_chamados.columns and pd.api.types.is_numeric_dtype(df_chamados['SLA Resolução']):
            sla_resolucao = df_chamados.groupby('Analista')['SLA Resolução'].mean().reset_index()
            sla_resolucao.columns = ['Analista', 'SLA Resolução']
        else:
            sla_resolucao = pd.DataFrame({'Analista': df_chamados['Analista'].unique(), 'SLA Resolução': 'N/A'})

        # Juntar tudo
        df_metas = total_atendimentos.merge(media_atendimento, on='Analista', how='left')
        df_metas = df_metas.merge(csat_obtido, on='Analista', how='left')
        df_metas = df_metas.merge(respostas_pesquisa, on='Analista', how='left')
        df_metas = df_metas.merge(sla_primeiro, on='Analista', how='left')
        df_metas = df_metas.merge(sla_resolucao, on='Analista', how='left')

        return df_metas

    def _calcular_resultados_area1(self, df_chamados: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        if df_chamados.empty:
            return {}

        # Assumindo que 'Data de Abertura' é a coluna de data
        df_chamados['Data de Abertura'] = pd.to_datetime(df_chamados['Data de Abertura'], errors='coerce')
        df_chamados = df_chamados.dropna(subset=['Data de Abertura'])
        df_chamados['Data'] = df_chamados['Data de Abertura'].dt.date

        # Gráfico de CSAT por Data (assumindo que CSAT já está no df_chamados ou pode ser calculado)
        # Para replicar a imagem, preciso de 'CSAT do Analista' e 'CSAT da Ferramenta'
        # Vou usar um placeholder aqui, idealmente viria do CSAT processado
        # Se não tiver CSAT no df_chamados, este gráfico será vazio ou com N/A
        csat_por_data = df_chamados.groupby('Data').agg(
            CSAT_Analista=('CSAT', 'mean'), # Assumindo que 'CSAT' é uma coluna no df_chamados
            CSAT_Ferramenta=('CSAT_Ferramenta', 'mean') # Assumindo que 'CSAT_Ferramenta' é uma coluna
        ).reset_index()
        csat_por_data = csat_por_data.fillna(0) # Preencher N/A com 0 para visualização

        # Gráfico de TMA, TME, TMR por Data
        # Assumindo que 'TMA', 'TME', 'TMR' são colunas numéricas no df_chamados
        tma_tme_tmr_por_data = df_chamados.groupby('Data').agg(
            TMA=('TMA', 'mean'),
            TME=('TME', 'mean'),
            TMR=('TMR', 'mean')
        ).reset_index()
        tma_tme_tmr_por_data = tma_tme_tmr_por_data.fillna(0)

        return {
            "csat_por_data": csat_por_data,
            "tma_tme_tmr_por_data": tma_tme_tmr_por_data
        }

    def _calcular_resultados_area2(self, df_chamados: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        if df_chamados.empty:
            return {}

        df_chamados['Data de Abertura'] = pd.to_datetime(df_chamados['Data de Abertura'], errors='coerce')
        df_chamados = df_chamados.dropna(subset=['Data de Abertura'])
        df_chamados['Data'] = df_chamados['Data de Abertura'].dt.date

        # Gráfico de SLA 1º Atendimento e SLA Resolução por Data
        # Assumindo que 'SLA 1º Atendimento' e 'SLA Resolução' são colunas numéricas no df_chamados
        sla_por_data = df_chamados.groupby('Data').agg(
            SLA_1_Atendimento=('SLA 1º Atendimento', 'mean'),
            SLA_Resolucao=('SLA Resolução', 'mean')
        ).reset_index()
        sla_por_data = sla_por_data.fillna(0)

        # Gráfico de Total de Chamados por Data
        total_chamados_por_data = df_chamados.groupby('Data')['Código do Chamado'].nunique().reset_index()
        total_chamados_por_data.columns = ['Data', 'Total']

        return {
            "sla_por_data": sla_por_data,
            "total_chamados_por_data": total_chamados_por_data
        }

    def _calcular_grafico_individual_1(self, df_chamados: pd.DataFrame) -> Dict[str, Any]:
        if df_chamados.empty:
            return {}

        # Cards de resumo geral (Total de Chamados)
        total_chamados_geral = df_chamados['Código do Chamado'].nunique()

        # Cards por analista (Elô, Kauan, Pedro, Mateus) - Replicar a estrutura da imagem
        # Assumindo que 'Analista' é a coluna de analistas
        analistas_especificos = ['Elô', 'Kauan', 'Pedro', 'Mateus']
        analista_data = {}

        for analista in analistas_especificos:
            df_analista = df_chamados[df_chamados['Analista'] == analista]
            
            atendimentos_dia = df_analista['Código do Chamado'].nunique() # Contagem única de chamados
            tma = df_analista['TMA'].mean() if 'TMA' in df_analista.columns and pd.api.types.is_numeric_dtype(df_analista['TMA']) else 'N/A'
            csat = df_analista['CSAT'].mean() if 'CSAT' in df_analista.columns and pd.api.types.is_numeric_dtype(df_analista['CSAT']) else 'N/A'
            percentual_resposta_pesquisa = df_analista['Percentual_Resposta_Pesquisa'].mean() if 'Percentual_Resposta_Pesquisa' in df_analista.columns and pd.api.types.is_numeric_dtype(df_analista['Percentual_Resposta_Pesquisa']) else 'N/A'
            sla_primeiro_atendimento = df_analista['SLA 1º Atendimento'].mean() if 'SLA 1º Atendimento' in df_analista.columns and pd.api.types.is_numeric_dtype(df_analista['SLA 1º Atendimento']) else 'N/A'
            sla_resolucao = df_analista['SLA Resolução'].mean() if 'SLA Resolução' in df_analista.columns and pd.api.types.is_numeric_dtype(df_analista['SLA Resolução']) else 'N/A'

            analista_data[analista] = {
                'Atendimentos dia': atendimentos_dia,
                'TMA': str(timedelta(minutes=int(tma))) if isinstance(tma, (int, float)) else tma, # Formatar como tempo
                'CSAT': f"{csat:.0f}%" if isinstance(csat, (int, float)) else csat,
                '% Resposta Pesquisa': f"{percentual_resposta_pesquisa:.0f}%" if isinstance(percentual_resposta_pesquisa, (int, float)) else percentual_resposta_pesquisa,
                'SLA 1º Atendimento': f"{sla_primeiro_atendimento:.0f}%" if isinstance(sla_primeiro_atendimento, (int, float)) else sla_primeiro_atendimento,
                'SLA Resolução': f"{sla_resolucao:.0f}%" if isinstance(sla_resolucao, (int, float)) else sla_resolucao,
            }
        
        return {
            "total_chamados": total_chamados_geral,
            "analista_data": analista_data
        }

    def _calcular_grafico_individual_2(self, df_chamados: pd.DataFrame) -> Dict[str, Any]:
        if df_chamados.empty:
            return {}

        # Cards por analista (Jonielson, Rosana, Marcos, Sarah, Graziele, Virgilio) - Replicar a estrutura da imagem
        analistas_especificos = ['Jonielson', 'Rosana', 'Marcos', 'Sarah', 'Graziele', 'Virgilio']
        analista_data = {}

        for analista in analistas_especificos:
            df_analista = df_chamados[df_chamados['Analista'] == analista]
            
            atendimentos_dia = df_analista['Código do Chamado'].nunique()
            tma = df_analista['TMA'].mean() if 'TMA' in df_analista.columns and pd.api.types.is_numeric_dtype(df_analista['TMA']) else 'N/A'
            csat = df_analista['CSAT'].mean() if 'CSAT' in df_analista.columns and pd.api.types.is_numeric_dtype(df_analista['CSAT']) else 'N/A'
            percentual_resposta_pesquisa = df_analista['Percentual_Resposta_Pesquisa'].mean() if 'Percentual_Resposta_Pesquisa' in df_analista.columns and pd.api.types.is_numeric_dtype(df_analista['Percentual_Resposta_Pesquisa']) else 'N/A'

            analista_data[analista] = {
                'Atendimentos dia': atendimentos_dia,
                'TMA': str(timedelta(minutes=int(tma))) if isinstance(tma, (int, float)) else tma,
                'CSAT': f"{csat:.0f}%" if isinstance(csat, (int, float)) else csat,
                '% Resposta Pesquisa': f"{percentual_resposta_pesquisa:.0f}%" if isinstance(percentual_resposta_pesquisa, (int, float)) else percentual_resposta_pesquisa,
            }
        
        return {
            "analista_data": analista_data
        }

    def obter_resumo_dados(self) -> Dict[str, Dict]:
        # Este método agora é mais para depuração, pois os dados são calculados
        # diretamente nas funções _calcular_...
        return {"info": "Dados processados dinamicamente. Use as abas específicas para ver os resultados."}

    def limpar_cache(self):
        logger.info("Solicitação de limpeza de cache. O cache será limpo na próxima execução do app_production.")



