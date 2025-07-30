"""
Gerador de dados de teste para CSAT
Cria dados simulados da Pesquisa de Satisfação para demonstração

Autor: Manus AI
Data: 30/07/2025
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def gerar_dados_csat_teste(num_registros: int = 50, num_duplicatas: int = 10) -> pd.DataFrame:
    """
    Gera dados de teste para CSAT com duplicatas intencionais
    
    Args:
        num_registros: Número total de registros
        num_duplicatas: Número de códigos que terão duplicatas
        
    Returns:
        DataFrame com dados de teste de CSAT
    """
    
    # Configurações
    avaliacoes = [
        "Ótimo - Superou minhas expectativas",
        "Bom - Atendeu minhas expectativas", 
        "Regular - Atendeu parcialmente",
        "Ruim - Não atendeu minhas expectativas",
        "Péssimo - Muito abaixo do esperado"
    ]
    
    analistas = [
        "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa",
        "Carlos Ferreira", "Lucia Almeida", "Roberto Lima", "Fernanda Souza"
    ]
    
    areas = ["Suporte Técnico", "Vendas", "Financeiro", "Atendimento"]
    
    # Gerar códigos de chamado únicos
    codigos_base = [f"CH{1000 + i:04d}" for i in range(num_registros - num_duplicatas)]
    
    # Adicionar códigos que serão duplicados
    codigos_duplicados = random.sample(codigos_base, num_duplicatas)
    todos_codigos = codigos_base + codigos_duplicados
    
    # Embaralhar para distribuir duplicatas
    random.shuffle(todos_codigos)
    
    dados = []
    
    for i, codigo in enumerate(todos_codigos):
        # Determinar se é uma duplicata e qual tipo de avaliação dar
        is_duplicata = codigo in codigos_duplicados and todos_codigos.count(codigo) > 1
        
        if is_duplicata:
            # Para duplicatas, criar cenários específicos
            ocorrencias_codigo = [j for j, c in enumerate(todos_codigos) if c == codigo]
            posicao_atual = ocorrencias_codigo.index(i)
            
            if posicao_atual == 0:
                # Primeira ocorrência - pode ser qualquer avaliação
                avaliacao = random.choice(avaliacoes)
            else:
                # Ocorrências subsequentes - criar cenários de teste
                if random.random() < 0.7:  # 70% chance de ter avaliação positiva
                    avaliacao = random.choice(avaliacoes[:2])  # Ótimo ou Bom
                else:
                    avaliacao = random.choice(avaliacoes[2:])  # Regular, Ruim ou Péssimo
        else:
            # Registro único - distribuição normal
            avaliacao = random.choice(avaliacoes)
        
        # Dados do registro
        registro = {
            "Código do Chamado": codigo,
            "Data da Pesquisa": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%d/%m/%Y"),
            "Analista Responsável": random.choice(analistas),
            "Área": random.choice(areas),
            "Atendimento - CES e CSAT - [ANALISTA] Como você avalia a qualidade do atendimento prestado pelo analista neste chamado?": avaliacao,
            "Tempo de Resolução (horas)": random.randint(1, 48),
            "Canal de Atendimento": random.choice(["Telefone", "Email", "Chat", "Presencial"]),
            "Tipo de Problema": random.choice(["Técnico", "Comercial", "Financeiro", "Informação"]),
            "Cliente Satisfeito": "Sim" if avaliacao.startswith(("Ótimo", "Bom")) else "Não",
            "Comentários Adicionais": f"Comentário sobre o atendimento {codigo}" if random.random() < 0.3 else "",
            "Score NPS": random.randint(0, 10),
            "Recomendaria o Serviço": random.choice(["Sim", "Não", "Talvez"])
        }
        
        dados.append(registro)
    
    return pd.DataFrame(dados)

def criar_planilha_satisfacao_teste(caminho_arquivo: str = None):
    """
    Cria arquivo Excel de teste da Pesquisa de Satisfação
    
    Args:
        caminho_arquivo: Caminho onde salvar o arquivo
    """
    if not caminho_arquivo:
        caminho_arquivo = os.path.join(os.getcwd(), 'pesquisa_satisfacao_teste.xlsx')
    
    # Gerar dados de teste
    df_csat = gerar_dados_csat_teste(num_registros=50, num_duplicatas=12)
    
    # Criar outras abas de exemplo
    df_resumo = pd.DataFrame({
        'Métrica': ['Total de Respostas', 'CSAT Score', 'NPS Score', 'Taxa de Resposta'],
        'Valor': [len(df_csat), '85%', '7.2', '78%'],
        'Meta': ['> 100', '> 80%', '> 7.0', '> 70%'],
        'Status': ['✅', '✅', '✅', '✅']
    })
    
    df_analistas = df_csat.groupby('Analista Responsável').agg({
        'Código do Chamado': 'count',
        'Score NPS': 'mean'
    }).round(2).reset_index()
    df_analistas.columns = ['Analista', 'Total_Atendimentos', 'NPS_Medio']
    
    # Salvar arquivo Excel com múltiplas abas
    with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
        df_csat.to_excel(writer, sheet_name='CSAT', index=False)
        df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
        df_analistas.to_excel(writer, sheet_name='Por Analista', index=False)
    
    print(f"Arquivo de teste criado: {caminho_arquivo}")
    print(f"Total de registros CSAT: {len(df_csat)}")
    print(f"Códigos únicos: {df_csat['Código do Chamado'].nunique()}")
    print(f"Códigos duplicados: {len(df_csat) - df_csat['Código do Chamado'].nunique()}")
    
    # Mostrar exemplos de duplicatas
    duplicatas = df_csat[df_csat.duplicated('Código do Chamado', keep=False)].sort_values('Código do Chamado')
    if not duplicatas.empty:
        print("\nExemplos de códigos duplicados:")
        for codigo in duplicatas['Código do Chamado'].unique()[:3]:
            registros_codigo = duplicatas[duplicatas['Código do Chamado'] == codigo]
            print(f"\nCódigo {codigo}:")
            for _, row in registros_codigo.iterrows():
                avaliacao = row['Atendimento - CES e CSAT - [ANALISTA] Como você avalia a qualidade do atendimento prestado pelo analista neste chamado?']
                print(f"  - {avaliacao}")
    
    return caminho_arquivo

if __name__ == "__main__":
    # Criar arquivo de teste
    arquivo = criar_planilha_satisfacao_teste()
    
    # Testar processamento
    from csat_processor import processar_planilha_satisfacao
    
    print("\n" + "="*50)
    print("TESTANDO PROCESSAMENTO DE CSAT")
    print("="*50)
    
    resultado = processar_planilha_satisfacao(arquivo)
    
    if resultado['sucesso']:
        print(f"✅ Processamento bem-sucedido!")
        print(f"📊 Métricas CSAT:")
        for chave, valor in resultado['metricas'].items():
            print(f"   {chave}: {valor}")
        
        print(f"\n📋 Relatório de Deduplicação:")
        for chave, valor in resultado['relatorio_deduplicacao'].items():
            print(f"   {chave}: {valor}")
    else:
        print(f"❌ Erro no processamento: {resultado['erro']}")

