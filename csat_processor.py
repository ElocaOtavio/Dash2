import pandas as pd
import logging

logger = logging.getLogger(__name__)

class CSATProcessor:
    """Processador de dados de CSAT com regras de deduplicação."""

    def __init__(self):
        pass

    def processar_planilha_satisfacao_df(self, df: pd.DataFrame) -> dict:
        """
        Processa um DataFrame de pesquisa de satisfação aplicando regras de deduplicação.

        Args:
            df: DataFrame contendo os dados da pesquisa de satisfação.

        Returns:
            Dicionário com dados processados, métricas e relatório de deduplicação.
        """
        if df.empty:
            logger.warning("DataFrame de CSAT vazio. Retornando dados vazios.")
            return {
                'sucesso': True,
                'dados_processados': pd.DataFrame(),
                'metricas': {'total_registros': 0, 'registros_duplicados_removidos': 0, 'csat_score': 0.0},
                'relatorio_deduplicacao': []
            }

        df_processado = df.copy()
        relatorio_deduplicacao = []
        registros_removidos = 0

        # Colunas relevantes
        col_codigo_chamado = "Código do Chamado"
        col_avaliacao = "Atendimento - CES e CSAT - [ANALISTA] Como você avalia a qualidade do atendimento prestado pelo analista neste chamado?"

        if col_codigo_chamado not in df_processado.columns or col_avaliacao not in df_processado.columns:
            logger.error(f"Colunas '{col_codigo_chamado}' ou '{col_avaliacao}' não encontradas no DataFrame de CSAT.")
            return {
                'sucesso': False,
                'erro': f"Colunas essenciais não encontradas: {col_codigo_chamado}, {col_avaliacao}"
            }

        # Identificar duplicatas com base no 'Código do Chamado'
        duplicatas = df_processado[df_processado.duplicated(subset=[col_codigo_chamado], keep=False)]

        if not duplicatas.empty:
            for codigo_chamado, grupo in duplicatas.groupby(col_codigo_chamado):
                registros_validos = grupo[grupo[col_avaliacao].astype(str).str.lower().str.startswith(('bom', 'ótimo'))]

                if not registros_validos.empty:
                    # Se houver registros 'Bom' ou 'Ótimo', manter apenas o primeiro válido
                    manter = registros_validos.iloc[0]
                    remover = grupo.drop(manter.name)
                    df_processado = df_processado.drop(remover.index)
                    registros_removidos += len(remover)
                    relatorio_deduplicacao.append({
                        'codigo_chamado': codigo_chamado,
                        'acao': 'Mantido Bom/Ótimo, removido duplicatas',
                        'mantido_index': manter.name,
                        'removido_indices': remover.index.tolist()
                    })
                else:
                    # Se não houver 'Bom' ou 'Ótimo', manter apenas o primeiro registro do grupo
                    manter = grupo.iloc[0]
                    remover = grupo.drop(manter.name)
                    df_processado = df_processado.drop(remover.index)
                    registros_removidos += len(remover)
                    relatorio_deduplicacao.append({
                        'codigo_chamado': codigo_chamado,
                        'acao': 'Mantido primeiro, removido duplicatas (sem Bom/Ótimo)',
                        'mantido_index': manter.name,
                        'removido_indices': remover.index.tolist()
                    })

        # Calcular métricas CSAT
        total_avaliacoes = len(df_processado)
        avaliacoes_positivas = df_processado[df_processado[col_avaliacao].astype(str).str.lower().str.startswith(('bom', 'ótimo'))]
        csat_score = (len(avaliacoes_positivas) / total_avaliacoes * 100) if total_avaliacoes > 0 else 0.0

        metricas = {
            'total_registros_originais': len(df),
            'total_registros_processados': len(df_processado),
            'registros_duplicados_removidos': registros_removidos,
            'csat_score': round(csat_score, 2),
            'distribuicao_avaliacoes': df_processado[col_avaliacao].value_counts().to_dict()
        }

        logger.info(f"Processamento CSAT concluído. Registros removidos: {registros_removidos}, CSAT Score: {csat_score:.2f}%")

        return {
            'sucesso': True,
            'dados_processados': df_processado,
            'metricas': metricas,
            'relatorio_deduplicacao': relatorio_deduplicacao
        }

# Remover a função processar_planilha_satisfacao se ela existia e não for mais usada
# ou adaptá-la para chamar o método da classe se necessário
# def processar_planilha_satisfacao(caminho_arquivo: str) -> dict:
#    # ... código antigo ...
#    pass


