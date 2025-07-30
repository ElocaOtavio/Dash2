"""
Processador de dados CSAT - Dashboard Eloca
Módulo específico para processar dados da Pesquisa de Satisfação

Autor: Manus AI
Data: 30/07/2025
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class CSATProcessor:
    """Processador especializado para dados de CSAT"""
    
    def __init__(self):
        self.coluna_codigo_chamado = "Código do Chamado"
        self.coluna_avaliacao = "Atendimento - CES e CSAT - [ANALISTA] Como você avalia a qualidade do atendimento prestado pelo analista neste chamado?"
        self.avaliacoes_positivas = ["Bom", "Ótimo"]
        self.avaliacoes_negativas = ["Regular", "Ruim", "Péssimo"]
    
    def processar_dados_csat(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa dados de CSAT aplicando regras de deduplicação
        
        Args:
            df: DataFrame com dados brutos de CSAT
            
        Returns:
            DataFrame processado com duplicatas removidas
        """
        if df.empty:
            logger.warning("DataFrame CSAT vazio")
            return df
        
        # Verificar se as colunas necessárias existem
        if not self._validar_colunas(df):
            logger.error("Colunas necessárias não encontradas no DataFrame CSAT")
            return df
        
        # Aplicar regras de deduplicação
        df_processado = self._aplicar_regras_deduplicacao(df)
        
        # Log do resultado
        registros_originais = len(df)
        registros_finais = len(df_processado)
        registros_removidos = registros_originais - registros_finais
        
        logger.info(f"CSAT processado: {registros_originais} → {registros_finais} registros ({registros_removidos} removidos)")
        
        return df_processado
    
    def _validar_colunas(self, df: pd.DataFrame) -> bool:
        """Valida se as colunas necessárias existem no DataFrame"""
        colunas_necessarias = [self.coluna_codigo_chamado, self.coluna_avaliacao]
        
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                # Tentar encontrar coluna similar
                coluna_similar = self._encontrar_coluna_similar(df.columns, coluna)
                if coluna_similar:
                    logger.info(f"Usando coluna '{coluna_similar}' para '{coluna}'")
                    if coluna == self.coluna_codigo_chamado:
                        self.coluna_codigo_chamado = coluna_similar
                    elif coluna == self.coluna_avaliacao:
                        self.coluna_avaliacao = coluna_similar
                else:
                    logger.error(f"Coluna '{coluna}' não encontrada")
                    return False
        
        return True
    
    def _encontrar_coluna_similar(self, colunas: List[str], coluna_procurada: str) -> Optional[str]:
        """Encontra coluna com nome similar"""
        coluna_lower = coluna_procurada.lower()
        
        # Busca exata (case insensitive)
        for coluna in colunas:
            if coluna.lower() == coluna_lower:
                return coluna
        
        # Busca por palavras-chave
        if "código" in coluna_lower and "chamado" in coluna_lower:
            for coluna in colunas:
                if "código" in coluna.lower() and "chamado" in coluna.lower():
                    return coluna
        
        if "analista" in coluna_lower and "atendimento" in coluna_lower:
            for coluna in colunas:
                if "analista" in coluna.lower() and ("atendimento" in coluna.lower() or "qualidade" in coluna.lower()):
                    return coluna
        
        return None
    
    def _aplicar_regras_deduplicacao(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica regras de deduplicação para códigos de chamado
        
        Regras:
        1. Se código se repete e há avaliações "Bom" ou "Ótimo", manter apenas essas
        2. Se código se repete e não há "Bom/Ótimo", manter apenas um registro
        3. Se código é único, manter o registro
        """
        df_resultado = pd.DataFrame()
        
        # Agrupar por código de chamado
        grupos = df.groupby(self.coluna_codigo_chamado)
        
        for codigo_chamado, grupo in grupos:
            if len(grupo) == 1:
                # Código único - manter registro
                df_resultado = pd.concat([df_resultado, grupo], ignore_index=True)
            else:
                # Código duplicado - aplicar regras
                grupo_processado = self._processar_grupo_duplicado(grupo, codigo_chamado)
                df_resultado = pd.concat([df_resultado, grupo_processado], ignore_index=True)
        
        return df_resultado
    
    def _processar_grupo_duplicado(self, grupo: pd.DataFrame, codigo_chamado: str) -> pd.DataFrame:
        """
        Processa grupo de registros com código de chamado duplicado
        
        Args:
            grupo: DataFrame com registros do mesmo código
            codigo_chamado: Código do chamado sendo processado
            
        Returns:
            DataFrame com registros filtrados conforme regras
        """
        # Verificar se há avaliações positivas
        avaliacoes_positivas = grupo[
            grupo[self.coluna_avaliacao].str.startswith(tuple(self.avaliacoes_positivas), na=False)
        ]
        
        if not avaliacoes_positivas.empty:
            # Há avaliações "Bom" ou "Ótimo" - manter apenas essas
            logger.debug(f"Código {codigo_chamado}: mantendo {len(avaliacoes_positivas)} avaliações positivas de {len(grupo)} total")
            return avaliacoes_positivas
        else:
            # Não há avaliações positivas - manter apenas o primeiro registro
            logger.debug(f"Código {codigo_chamado}: sem avaliações positivas, mantendo apenas 1 de {len(grupo)} registros")
            return grupo.iloc[[0]]
    
    def calcular_metricas_csat(self, df: pd.DataFrame) -> Dict:
        """
        Calcula métricas de CSAT a partir dos dados processados
        
        Args:
            df: DataFrame processado de CSAT
            
        Returns:
            Dicionário com métricas calculadas
        """
        if df.empty:
            return {
                'total_respostas': 0,
                'csat_score': 0,
                'distribuicao_avaliacoes': {},
                'avaliacoes_positivas': 0,
                'avaliacoes_negativas': 0
            }
        
        total_respostas = len(df)
        
        # Contar avaliações por tipo
        distribuicao = {}
        avaliacoes_positivas = 0
        avaliacoes_negativas = 0
        
        for _, row in df.iterrows():
            avaliacao = str(row[self.coluna_avaliacao])
            
            # Classificar avaliação
            if any(avaliacao.startswith(pos) for pos in self.avaliacoes_positivas):
                avaliacoes_positivas += 1
                categoria = "Positiva"
            elif any(avaliacao.startswith(neg) for neg in self.avaliacoes_negativas):
                avaliacoes_negativas += 1
                categoria = "Negativa"
            else:
                categoria = "Neutra"
            
            # Contar na distribuição
            if avaliacao not in distribuicao:
                distribuicao[avaliacao] = 0
            distribuicao[avaliacao] += 1
        
        # Calcular CSAT Score (% de avaliações positivas)
        csat_score = (avaliacoes_positivas / total_respostas * 100) if total_respostas > 0 else 0
        
        return {
            'total_respostas': total_respostas,
            'csat_score': round(csat_score, 2),
            'distribuicao_avaliacoes': distribuicao,
            'avaliacoes_positivas': avaliacoes_positivas,
            'avaliacoes_negativas': avaliacoes_negativas,
            'avaliacoes_neutras': total_respostas - avaliacoes_positivas - avaliacoes_negativas
        }
    
    def gerar_relatorio_deduplicacao(self, df_original: pd.DataFrame, df_processado: pd.DataFrame) -> Dict:
        """
        Gera relatório detalhado do processo de deduplicação
        
        Args:
            df_original: DataFrame original
            df_processado: DataFrame após processamento
            
        Returns:
            Dicionário com estatísticas do processo
        """
        if df_original.empty:
            return {'erro': 'DataFrame original vazio'}
        
        # Estatísticas básicas
        registros_originais = len(df_original)
        registros_finais = len(df_processado)
        registros_removidos = registros_originais - registros_finais
        
        # Análise de códigos duplicados
        codigos_originais = df_original[self.coluna_codigo_chamado].value_counts()
        codigos_duplicados = codigos_originais[codigos_originais > 1]
        
        # Análise de avaliações removidas
        avaliacoes_removidas = {}
        if not df_original.empty and not df_processado.empty:
            avaliacoes_orig = df_original[self.coluna_avaliacao].value_counts()
            avaliacoes_final = df_processado[self.coluna_avaliacao].value_counts()
            
            for avaliacao in avaliacoes_orig.index:
                removidas = avaliacoes_orig[avaliacao] - avaliacoes_final.get(avaliacao, 0)
                if removidas > 0:
                    avaliacoes_removidas[avaliacao] = removidas
        
        return {
            'registros_originais': registros_originais,
            'registros_finais': registros_finais,
            'registros_removidos': registros_removidos,
            'percentual_removido': round((registros_removidos / registros_originais * 100), 2) if registros_originais > 0 else 0,
            'codigos_duplicados': len(codigos_duplicados),
            'codigos_unicos_originais': len(codigos_originais),
            'codigos_unicos_finais': df_processado[self.coluna_codigo_chamado].nunique() if not df_processado.empty else 0,
            'avaliacoes_removidas': avaliacoes_removidas
        }
    
    def validar_integridade_dados(self, df: pd.DataFrame) -> Dict:
        """
        Valida integridade dos dados de CSAT
        
        Args:
            df: DataFrame para validar
            
        Returns:
            Dicionário com resultado da validação
        """
        problemas = []
        warnings = []
        
        if df.empty:
            problemas.append("DataFrame está vazio")
            return {'valido': False, 'problemas': problemas, 'warnings': warnings}
        
        # Verificar colunas obrigatórias
        if self.coluna_codigo_chamado not in df.columns:
            problemas.append(f"Coluna '{self.coluna_codigo_chamado}' não encontrada")
        
        if self.coluna_avaliacao not in df.columns:
            problemas.append(f"Coluna '{self.coluna_avaliacao}' não encontrada")
        
        if problemas:
            return {'valido': False, 'problemas': problemas, 'warnings': warnings}
        
        # Verificar dados faltantes
        codigos_nulos = df[self.coluna_codigo_chamado].isnull().sum()
        if codigos_nulos > 0:
            warnings.append(f"{codigos_nulos} códigos de chamado nulos encontrados")
        
        avaliacoes_nulas = df[self.coluna_avaliacao].isnull().sum()
        if avaliacoes_nulas > 0:
            warnings.append(f"{avaliacoes_nulas} avaliações nulas encontradas")
        
        # Verificar padrões de avaliação
        avaliacoes_unicas = df[self.coluna_avaliacao].dropna().unique()
        avaliacoes_reconhecidas = 0
        
        for avaliacao in avaliacoes_unicas:
            if any(str(avaliacao).startswith(padrao) for padrao in self.avaliacoes_positivas + self.avaliacoes_negativas):
                avaliacoes_reconhecidas += 1
        
        if avaliacoes_reconhecidas < len(avaliacoes_unicas):
            warnings.append(f"Algumas avaliações podem não seguir o padrão esperado")
        
        return {
            'valido': True,
            'problemas': problemas,
            'warnings': warnings,
            'total_registros': len(df),
            'codigos_unicos': df[self.coluna_codigo_chamado].nunique(),
            'avaliacoes_unicas': len(avaliacoes_unicas)
        }

def processar_planilha_satisfacao(caminho_arquivo: str) -> Dict:
    """
    Função principal para processar planilha de Pesquisa de Satisfação
    
    Args:
        caminho_arquivo: Caminho para o arquivo Excel
        
    Returns:
        Dicionário com dados processados e métricas
    """
    try:
        # Carregar aba CSAT
        df_csat = pd.read_excel(caminho_arquivo, sheet_name='CSAT')
        
        # Inicializar processador
        processor = CSATProcessor()
        
        # Validar dados
        validacao = processor.validar_integridade_dados(df_csat)
        if not validacao['valido']:
            return {
                'sucesso': False,
                'erro': 'Dados inválidos',
                'detalhes': validacao
            }
        
        # Processar dados
        df_processado = processor.processar_dados_csat(df_csat)
        
        # Calcular métricas
        metricas = processor.calcular_metricas_csat(df_processado)
        
        # Gerar relatório
        relatorio = processor.gerar_relatorio_deduplicacao(df_csat, df_processado)
        
        return {
            'sucesso': True,
            'dados_originais': df_csat,
            'dados_processados': df_processado,
            'metricas': metricas,
            'relatorio_deduplicacao': relatorio,
            'validacao': validacao
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar planilha de satisfação: {str(e)}")
        return {
            'sucesso': False,
            'erro': str(e)
        }

