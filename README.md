# Dashboard Eloca - Sistema de Gestão de Vendas

Um dashboard interativo desenvolvido em Streamlit para visualização e análise de dados de vendas da plataforma Eloca (Desk.ms).

## 🚀 Funcionalidades

### 📊 Visualizações Disponíveis
- **Resumo Geral**: Visão consolidada de todos os dados
- **Metas Individuais**: Acompanhamento de metas por pessoa
- **Resultados Área 1**: Análise de performance da primeira área
- **Resultados Área 2**: Análise de performance da segunda área
- **Gráfico Individual 1**: Visualização customizada específica
- **Gráfico Individual 2**: Visualização customizada específica

### ⚡ Características Técnicas
- **Cache Inteligente**: Dados atualizados automaticamente com TTL configurável
- **Validação de Dados**: Verificação automática da integridade dos dados
- **Interface Responsiva**: Design adaptável para diferentes dispositivos
- **Visualizações Interativas**: Gráficos dinâmicos com Plotly
- **Configuração Segura**: Credenciais protegidas via variáveis de ambiente

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Acesso à API da Eloca (Desk.ms)
- Token de autenticação válido

### Instalação Local

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd eloca-dashboard
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

4. **Execute a aplicação**
```bash
streamlit run app.py
```

### Deploy no Streamlit Cloud

1. **Faça upload dos arquivos para o GitHub**
   - `app.py`
   - `requirements.txt`
   - `config.py`
   - `data_processor.py`
   - `visualizations.py`

2. **Configure no Streamlit Cloud**
   - Acesse [streamlit.io/cloud](https://streamlit.io/cloud)
   - Conecte seu repositório GitHub
   - Configure os Secrets:

```toml
ELOCA_URL = "https://eloca.desk.ms/Relatorios/excel?token=SEU_TOKEN"
DESKMANAGER_TOKEN = "SEU_VALOR_DO_HEADER"
APP_TITLE = "Dashboard Eloca - Gestão de Vendas"
CACHE_TTL = "3600"
DEBUG_MODE = "False"
```

## 📋 Estrutura do Projeto

```
eloca-dashboard/
├── app.py                 # Aplicação principal Streamlit
├── config.py             # Configurações e variáveis de ambiente
├── data_processor.py     # Processamento e validação de dados
├── visualizations.py     # Criação de gráficos e visualizações
├── requirements.txt      # Dependências Python
├── .env.example         # Exemplo de configuração
└── README.md           # Documentação
```

## 🔧 Configuração Detalhada

### Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `ELOCA_URL` | URL completa da API com token | `https://eloca.desk.ms/Relatorios/excel?token=abc123` |
| `DESKMANAGER_TOKEN` | Token do header DeskManager | `seu_token_aqui` |
| `APP_TITLE` | Título da aplicação | `Dashboard Eloca` |
| `CACHE_TTL` | Tempo de cache em segundos | `3600` |
| `DEBUG_MODE` | Modo debug (true/false) | `false` |

### Abas da Planilha Processadas

O sistema processa automaticamente as seguintes abas:
- `Metas Individuais`
- `Resultados área 1`
- `Resultados área 2`
- `Grafico-Individual_1`
- `Grafico-Individual_2`

## 📊 Tipos de Visualizações

### Metas Individuais
- Gráfico de barras comparativo (Meta vs Realizado)
- Cálculo automático de percentual de atingimento
- Identificação automática de colunas relevantes

### Resultados por Área
- Gráficos temporais (se houver coluna de data)
- Gráficos de barras múltiplas
- Análise estatística descritiva

### Gráficos Individuais
- Gráficos de dispersão
- Histogramas
- Visualizações customizáveis pelo usuário

## 🔍 Funcionalidades Avançadas

### Cache Inteligente
- Dados são armazenados em cache por período configurável
- Atualização automática quando o cache expira
- Botão manual para forçar atualização

### Validação de Dados
- Verificação automática da estrutura dos dados
- Alertas para dados incompletos ou inconsistentes
- Logs detalhados para debugging

### Interface Adaptativa
- Design responsivo para desktop e mobile
- Temas customizáveis
- Navegação intuitiva com menu horizontal

## 🚨 Solução de Problemas

### Erro de Configuração
```
❌ Erro de configuração: ELOCA_URL não está definida
```
**Solução**: Verifique se as variáveis de ambiente estão configuradas corretamente.

### Erro de Conexão
```
❌ Erro de conexão com a API
```
**Solução**: 
1. Verifique sua conexão com a internet
2. Confirme se o token está válido
3. Teste a URL manualmente

### Dados Não Carregam
```
⚠️ Não há dados disponíveis para [Aba]
```
**Solução**:
1. Verifique se a aba existe na planilha
2. Confirme se há dados na aba
3. Verifique os logs de debug

## 📈 Performance

### Otimizações Implementadas
- Cache de dados com TTL configurável
- Carregamento lazy de visualizações
- Processamento otimizado de DataFrames
- Limitação automática de registros para gráficos

### Monitoramento
- Métricas de uso de memória
- Tempo de carregamento dos dados
- Status de saúde da aplicação

## 🔒 Segurança

### Boas Práticas Implementadas
- Credenciais armazenadas como variáveis de ambiente
- Validação de entrada de dados
- Logs de auditoria
- Headers de segurança customizados

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Changelog

### v1.0.0 (Atual)
- ✅ Implementação inicial do dashboard
- ✅ Processamento das 5 abas principais
- ✅ Sistema de cache inteligente
- ✅ Validação automática de dados
- ✅ Interface responsiva
- ✅ Deploy no Streamlit Cloud

## 📞 Suporte

Para suporte técnico ou dúvidas:
1. Verifique a documentação acima
2. Consulte os logs de debug
3. Abra uma issue no repositório

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

