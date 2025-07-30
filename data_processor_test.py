"""
Versão de teste do processador de dados que funciona com arquivos locais
"""
import pandas as pd
import streamlit as st
from typing import Dict, Optional
import logging
import os
from config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessorTest:
    """Classe para processar dados de teste locais"""
    
    def __init__(self):
        self.config = Config()
        self.dados_cache = {}
        
    @st.cache_data(ttl=Config.CACHE_TTL)
    def carregar_dados_completos(_self) -> Optional[Dict[str, pd.DataFrame]]:
        """
        Carrega dados de teste do arquivo Excel local
        
        Returns:
            Dict com DataFrames de cada aba ou None se houver erro
        """
        try:
            logger.info("Carregando dados de teste do arquivo local")
            
            # Caminho do arquivo de teste
            arquivo_teste = "/home/ubuntu/eloca-dashboard/dados_teste.xlsx"
            
            if not os.path.exists(arquivo_teste):
                logger.error(f"Arquivo de teste não encontrado: {arquivo_teste}")
                st.error("Arquivo de dados de teste não encontrado")
                return None
            
            # Carregar todas as abas
            dados_abas = {}
            
            try:
                # Ler todas as abas especificadas
                for aba in _self.config.ABAS_PLANILHA:
                    try:
                        df = pd.read_excel(arquivo_teste, sheet_name=aba)
                        dados_abas[aba] = df
                        logger.info(f"Aba '{aba}' carregada com {len(df)} linhas")
                    except Exception as e:
                        logger.warning(f"Não foi possível carregar a aba '{aba}': {e}")
                        # Criar DataFrame vazio se a aba não existir
                        dados_abas[aba] = pd.DataFrame()
                        
            except Exception as e:
                logger.error(f"Erro ao processar arquivo Excel: {e}")
                st.error(f"Erro ao processar planilha: {e}")
                return None
                
            logger.info(f"Dados de teste carregados com sucesso. {len(dados_abas)} abas processadas")
            return dados_abas
            
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            st.error(f"Erro inesperado: {e}")
            return None
    
    def obter_aba(self, nome_aba: str) -> Optional[pd.DataFrame]:
        """
        Obtém dados de uma aba específica
        
        Args:
            nome_aba: Nome da aba a ser obtida
            
        Returns:
            DataFrame da aba ou None se não encontrada
        """
        dados_completos = self.carregar_dados_completos()
        if dados_completos and nome_aba in dados_completos:
            return dados_completos[nome_aba]
        return None
    
    def validar_dados_aba(self, df: pd.DataFrame, nome_aba: str) -> bool:
        """
        Valida se os dados de uma aba estão em formato adequado
        
        Args:
            df: DataFrame a ser validado
            nome_aba: Nome da aba para contexto
            
        Returns:
            True se válido, False caso contrário
        """
        if df is None or df.empty:
            logger.warning(f"Aba '{nome_aba}' está vazia ou não foi carregada")
            return False
            
        # Validações específicas por tipo de aba
        if "Metas" in nome_aba:
            # Validar se tem colunas essenciais para metas
            colunas_esperadas = ["meta", "realizado", "percentual"]
            colunas_encontradas = [col for col in colunas_esperadas 
                                 if any(col.lower() in str(c).lower() for c in df.columns)]
            if len(colunas_encontradas) < 2:
                logger.warning(f"Aba '{nome_aba}' não possui colunas de meta adequadas")
                
        elif "Resultados" in nome_aba:
            # Validar se tem dados numéricos para resultados
            colunas_numericas = df.select_dtypes(include=['number']).columns
            if len(colunas_numericas) == 0:
                logger.warning(f"Aba '{nome_aba}' não possui colunas numéricas")
                
        elif "Grafico" in nome_aba:
            # Validar se tem dados adequados para gráficos
            if len(df.columns) < 2:
                logger.warning(f"Aba '{nome_aba}' possui poucas colunas para gráficos")
                
        return True
    
    def obter_resumo_dados(self) -> Dict[str, Dict]:
        """
        Obtém resumo estatístico de todas as abas
        
        Returns:
            Dicionário com resumos de cada aba
        """
        dados_completos = self.carregar_dados_completos()
        resumo = {}
        
        if dados_completos:
            for nome_aba, df in dados_completos.items():
                if not df.empty:
                    resumo[nome_aba] = {
                        "linhas": len(df),
                        "colunas": len(df.columns),
                        "colunas_numericas": len(df.select_dtypes(include=['number']).columns),
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
        """Limpa o cache de dados"""
        st.cache_data.clear()
        logger.info("Cache de dados limpo")

