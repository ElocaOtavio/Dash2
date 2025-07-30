"""
Gerador de dados de teste para o Dashboard Eloca
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class TestDataGenerator:
    """Gera dados de teste para simular as abas da planilha Eloca"""
    
    def __init__(self):
        self.nomes = [
            "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa", "Carlos Ferreira",
            "Lucia Almeida", "Roberto Lima", "Fernanda Souza", "Marcos Pereira", "Julia Rodrigues"
        ]
        
        self.areas = ["Vendas Norte", "Vendas Sul", "Vendas Centro", "Vendas Online"]
        self.produtos = ["Produto A", "Produto B", "Produto C", "Produto D", "Produto E"]
        
    def gerar_metas_individuais(self, num_registros=10):
        """Gera dados para a aba Metas Individuais"""
        data = {
            "Nome": random.sample(self.nomes, min(num_registros, len(self.nomes))),
            "Meta_Mensal": np.random.randint(50000, 150000, num_registros),
            "Realizado": np.random.randint(30000, 180000, num_registros),
            "Area": [random.choice(self.areas) for _ in range(num_registros)],
            "Mes": ["Janeiro 2024"] * num_registros
        }
        
        df = pd.DataFrame(data)
        df["Percentual_Atingimento"] = (df["Realizado"] / df["Meta_Mensal"] * 100).round(2)
        df["Status"] = df["Percentual_Atingimento"].apply(
            lambda x: "Acima da Meta" if x >= 100 else "Abaixo da Meta"
        )
        
        return df
    
    def gerar_resultados_area(self, area_num, num_registros=15):
        """Gera dados para as abas de Resultados por Área"""
        # Gerar datas dos últimos 15 dias
        datas = [datetime.now() - timedelta(days=i) for i in range(num_registros)]
        datas.reverse()
        
        data = {
            "Data": datas,
            "Vendas_Diarias": np.random.randint(5000, 25000, num_registros),
            "Numero_Clientes": np.random.randint(10, 50, num_registros),
            "Ticket_Medio": np.random.randint(200, 800, num_registros),
            "Meta_Diaria": [15000] * num_registros,
            "Area": [f"Área {area_num}"] * num_registros
        }
        
        df = pd.DataFrame(data)
        df["Percentual_Meta"] = (df["Vendas_Diarias"] / df["Meta_Diaria"] * 100).round(2)
        df["Acumulado"] = df["Vendas_Diarias"].cumsum()
        
        return df
    
    def gerar_grafico_individual(self, grafico_num, num_registros=20):
        """Gera dados para os gráficos individuais"""
        if grafico_num == "1":
            # Gráfico de vendas por produto
            data = {
                "Produto": random.choices(self.produtos, k=num_registros),
                "Quantidade_Vendida": np.random.randint(1, 100, num_registros),
                "Valor_Unitario": np.random.randint(50, 500, num_registros),
                "Margem_Lucro": np.random.uniform(0.1, 0.4, num_registros).round(3),
                "Categoria": [random.choice(["Eletrônicos", "Roupas", "Casa", "Esporte"]) 
                             for _ in range(num_registros)]
            }
            
            df = pd.DataFrame(data)
            df["Valor_Total"] = df["Quantidade_Vendida"] * df["Valor_Unitario"]
            df["Lucro"] = df["Valor_Total"] * df["Margem_Lucro"]
            
        else:  # grafico_num == "2"
            # Gráfico de performance por vendedor
            data = {
                "Vendedor": random.choices(self.nomes, k=num_registros),
                "Vendas_Mes": np.random.randint(20000, 120000, num_registros),
                "Comissao": np.random.uniform(0.02, 0.08, num_registros).round(4),
                "Experiencia_Anos": np.random.randint(1, 15, num_registros),
                "Regiao": [random.choice(["Norte", "Sul", "Centro", "Online"]) 
                          for _ in range(num_registros)]
            }
            
            df = pd.DataFrame(data)
            df["Valor_Comissao"] = df["Vendas_Mes"] * df["Comissao"]
            df["Performance_Score"] = (df["Vendas_Mes"] / 1000 + df["Experiencia_Anos"] * 2).round(2)
        
        return df
    
    def gerar_todas_abas(self):
        """Gera dados para todas as abas"""
        dados = {
            "Metas Individuais": self.gerar_metas_individuais(),
            "Resultados área 1": self.gerar_resultados_area("1"),
            "Resultados área 2": self.gerar_resultados_area("2"),
            "Grafico-Individual_1": self.gerar_grafico_individual("1"),
            "Grafico-Individual_2": self.gerar_grafico_individual("2")
        }
        
        return dados
    
    def salvar_excel_teste(self, caminho="dados_teste.xlsx"):
        """Salva dados de teste em arquivo Excel"""
        dados = self.gerar_todas_abas()
        
        with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
            for nome_aba, df in dados.items():
                df.to_excel(writer, sheet_name=nome_aba, index=False)
        
        print(f"Arquivo de teste salvo em: {caminho}")
        return caminho

if __name__ == "__main__":
    generator = TestDataGenerator()
    
    # Gerar e salvar dados de teste
    caminho_arquivo = "/home/ubuntu/eloca-dashboard/dados_teste.xlsx"
    generator.salvar_excel_teste(caminho_arquivo)
    
    # Mostrar resumo dos dados gerados
    dados = generator.gerar_todas_abas()
    print("\n📊 Resumo dos dados de teste gerados:")
    for nome_aba, df in dados.items():
        print(f"  {nome_aba}: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"    Colunas: {', '.join(df.columns.tolist())}")
        print()

