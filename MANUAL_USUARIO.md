# Manual do Usuário - Dashboard Eloca

## 📖 Guia Completo de Utilização

**Versão**: 1.0  
**Data**: 30 de Julho de 2025  
**Autor**: Manus AI  

---

## 🎯 Introdução

O Dashboard Eloca é uma aplicação web interativa desenvolvida especificamente para análise e visualização de dados de vendas da plataforma Eloca (Desk.ms). Este sistema permite aos usuários acompanhar metas individuais, resultados por área e gerar análises detalhadas através de gráficos interativos e relatórios dinâmicos.

### Principais Funcionalidades

O dashboard oferece cinco módulos principais de análise, cada um projetado para atender necessidades específicas de gestão de vendas. O sistema processa automaticamente dados de uma planilha Excel com cinco abas distintas, transformando informações brutas em visualizações compreensíveis e acionáveis.

A interface foi desenvolvida com foco na usabilidade, permitindo que usuários de diferentes níveis técnicos possam navegar facilmente entre as diferentes seções e extrair insights valiosos dos dados. O sistema utiliza cache inteligente para garantir performance otimizada, atualizando automaticamente as informações conforme configurado.

---

## 🚀 Primeiros Passos

### Acessando o Sistema

Para acessar o Dashboard Eloca, você precisará de um navegador web moderno (Chrome, Firefox, Safari ou Edge) e uma conexão com a internet. O sistema é totalmente baseado na web, não requerendo instalação de software adicional.

Ao acessar a URL fornecida pelo administrador do sistema, você será direcionado para a página principal do dashboard. O carregamento inicial pode levar alguns segundos, especialmente na primeira utilização, pois o sistema estará processando e organizando os dados mais recentes.

### Interface Principal

A interface do dashboard é dividida em três áreas principais: o cabeçalho com o título e banner informativo, o menu de navegação horizontal e a área de conteúdo principal. Na lateral esquerda, você encontrará a barra lateral (sidebar) com controles e informações do sistema.

O cabeçalho apresenta o título "Dashboard Eloca - Gestão de Vendas" e, em ambiente de teste, exibirá um banner amarelo indicando "MODO DE TESTE - Usando dados simulados para demonstração". Este banner garante que você saiba quando está trabalhando com dados reais ou simulados.

### Menu de Navegação

O menu horizontal oferece seis opções principais, cada uma representada por um ícone específico e texto descritivo:

- **📊 Resumo Geral**: Visão consolidada de todos os dados
- **🎯 Metas Individuais**: Acompanhamento de performance individual
- **📈 Resultados Área 1**: Análise específica da primeira área de vendas
- **📉 Resultados Área 2**: Análise específica da segunda área de vendas
- **📋 Gráfico Individual 1**: Visualizações customizadas de produtos
- **📊 Gráfico Individual 2**: Visualizações customizadas de vendedores

---

## 📊 Módulo Resumo Geral

### Visão Geral

O módulo Resumo Geral serve como ponto de entrada principal do dashboard, oferecendo uma visão consolidada de todos os dados disponíveis no sistema. Esta seção é especialmente útil para gestores que precisam de uma compreensão rápida do estado geral das operações de vendas.

### Métricas Principais

Na parte superior da página, você encontrará quatro cartões de métricas principais que fornecem informações essenciais sobre o volume de dados processados:

**Total de Linhas**: Indica o número total de registros processados em todas as abas da planilha. Este número representa a quantidade de dados individuais que o sistema está analisando, incluindo vendedores, transações, produtos e outros elementos relevantes.

**Total de Colunas**: Mostra a quantidade total de campos de dados disponíveis em todas as abas. Cada coluna representa um tipo diferente de informação, como nomes, valores, datas, percentuais e categorias.

**Abas com Dados**: Apresenta uma fração indicando quantas das cinco abas esperadas contêm dados válidos. Em condições normais, este valor deve ser 5/5, indicando que todas as abas foram carregadas com sucesso.

**Memória Total**: Exibe o uso de memória do sistema para processar todos os dados carregados. Este valor é útil para monitorar a performance do sistema e identificar possíveis problemas de capacidade.

### Gráficos de Resumo

Abaixo das métricas principais, o sistema apresenta dois gráficos de barras lado a lado que oferecem uma visualização comparativa entre as diferentes abas:

O gráfico da esquerda mostra o "Número de Linhas por Aba", permitindo identificar rapidamente quais seções contêm mais dados. Isso é útil para entender a distribuição de informações e identificar áreas que podem precisar de mais atenção ou análise.

O gráfico da direita apresenta o "Número de Colunas por Aba", indicando a complexidade de dados em cada seção. Abas com mais colunas geralmente contêm informações mais detalhadas e oferecem possibilidades de análise mais profundas.

### Tabela Detalhada

A seção inferior do Resumo Geral apresenta uma tabela detalhada com estatísticas específicas para cada aba. Esta tabela inclui as seguintes colunas:

**Aba**: Nome da seção de dados (Metas Individuais, Resultados área 1, etc.)
**Linhas**: Número exato de registros em cada aba
**Colunas**: Quantidade de campos de dados disponíveis
**Cols. Numéricas**: Número de colunas que contêm dados numéricos, importantes para cálculos e análises
**Valores Nulos**: Quantidade de campos vazios ou sem dados, útil para avaliar a qualidade dos dados
**Memória (MB)**: Uso específico de memória para cada aba

### Interpretação dos Dados

Para interpretar efetivamente as informações do Resumo Geral, considere os seguintes pontos:

Valores altos de "Valores Nulos" podem indicar problemas na coleta de dados ou campos opcionais que nem sempre são preenchidos. Isso não necessariamente representa um problema, mas pode afetar a precisão de algumas análises.

A distribuição de linhas entre as abas pode revelar padrões interessantes. Por exemplo, se "Metas Individuais" tem significativamente menos registros que "Resultados área 1", isso pode indicar que há mais dados de transações do que vendedores ativos.

O uso de memória deve permanecer em níveis razoáveis. Valores muito altos podem indicar a necessidade de otimização ou limitação na quantidade de dados processados simultaneamente.

---

## 🎯 Módulo Metas Individuais

### Funcionalidade Principal

O módulo Metas Individuais é projetado para acompanhar a performance de vendedores individuais em relação às suas metas estabelecidas. Esta seção é fundamental para gestores de vendas que precisam monitorar o desempenho da equipe e identificar oportunidades de melhoria ou reconhecimento.

### Métricas de Performance

A página inicia com três métricas principais que fornecem uma visão geral da situação das metas:

**Total de Vendedores**: Indica quantos vendedores estão sendo monitorados no período atual. Este número representa o tamanho da equipe de vendas ativa e é fundamental para entender a escala das operações.

**Meta Total**: Apresenta a soma de todas as metas individuais estabelecidas para o período. Este valor representa o objetivo coletivo da equipe e serve como referência para avaliar o potencial total de vendas.

**Realizado Total**: Mostra o valor total efetivamente vendido por toda a equipe. A comparação entre este valor e a Meta Total fornece uma visão imediata da performance geral da equipe.

### Gráfico Meta vs Realizado

O gráfico principal desta seção apresenta uma comparação visual entre metas e resultados para cada vendedor individual. O gráfico utiliza barras agrupadas, onde:

- **Barras azuis claras** representam as metas estabelecidas para cada vendedor
- **Barras azuis escuras** mostram os valores efetivamente realizados

Esta visualização permite identificar rapidamente quais vendedores estão superando suas metas (barras escuras maiores que as claras) e quais estão abaixo do esperado. A diferença visual entre as barras facilita a identificação de padrões e outliers na performance da equipe.

### Análise de Performance Detalhada

A seção "Análise de Performance" oferece insights mais profundos sobre os dados de vendas:

**Vendedores Acima da Meta**: Apresenta uma fração indicando quantos vendedores superaram suas metas individuais. Por exemplo, "1/10" significa que apenas um vendedor de dez atingiu ou superou sua meta estabelecida.

**Melhor Performance**: Identifica o vendedor com o melhor percentual de atingimento de meta, incluindo o nome e o percentual exato. Esta informação é valiosa para reconhecimento e para identificar melhores práticas que podem ser compartilhadas com a equipe.

**Performance Média**: Calcula o percentual médio de atingimento de metas de toda a equipe. Este valor oferece uma perspectiva geral da performance coletiva e pode ser usado como benchmark para avaliações individuais.

### Distribuição de Performance

O histograma de "Distribuição de Performance" mostra como os percentuais de atingimento de meta estão distribuídos entre a equipe. Este gráfico ajuda a identificar:

- Se a maioria dos vendedores está concentrada em uma faixa específica de performance
- A existência de grupos distintos de performance (alto, médio, baixo)
- Outliers que podem precisar de atenção especial ou reconhecimento

### Dados Detalhados

A tabela de dados detalhados na parte inferior da página apresenta informações completas para cada vendedor, incluindo:

- **Nome**: Identificação do vendedor
- **Meta Mensal**: Valor da meta estabelecida
- **Realizado**: Valor efetivamente vendido
- **Área**: Região ou área de atuação do vendedor
- **Mês**: Período de referência dos dados
- **Percentual de Atingimento**: Cálculo automático da performance
- **Status**: Classificação automática (Acima da Meta / Abaixo da Meta)

### Utilizando os Insights

Para maximizar o valor das informações do módulo Metas Individuais:

**Identificação de Top Performers**: Use os dados para reconhecer vendedores que consistentemente superam suas metas. Considere estudar suas práticas para replicar o sucesso.

**Suporte a Vendedores em Dificuldade**: Identifique vendedores com performance abaixo da média e desenvolva planos de ação específicos para apoiá-los.

**Ajuste de Metas**: Analise se as metas estabelecidas são realistas com base na distribuição de performance. Metas muito altas ou muito baixas podem desmotivar a equipe.

**Análise por Área**: Compare a performance entre diferentes áreas para identificar fatores regionais que podem estar afetando os resultados.

---

## 📈 Módulos Resultados por Área

### Visão Geral dos Módulos

Os módulos "Resultados Área 1" e "Resultados Área 2" são projetados para analisar a performance de vendas em diferentes regiões, territórios ou divisões da empresa. Cada área é tratada independentemente, permitindo comparações e análises específicas que podem revelar padrões regionais, sazonais ou operacionais únicos.

### Estrutura Comum dos Módulos

Ambos os módulos seguem uma estrutura similar, facilitando a navegação e comparação entre áreas. Esta consistência na interface permite que os usuários desenvolvam familiaridade com o sistema e possam rapidamente extrair insights de qualquer área.

### Métricas Principais por Área

Cada módulo de área apresenta três métricas fundamentais:

**Dias de Dados**: Indica o período de tempo coberto pelos dados disponíveis. Normalmente, este valor representa os últimos 15 dias de operação, fornecendo uma visão recente e relevante da performance da área.

**Vendas Totais**: Apresenta a soma de todas as vendas realizadas na área durante o período analisado. Este valor é fundamental para entender o volume de negócios gerado e comparar a produtividade entre diferentes áreas.

**Ticket Médio**: Calcula o valor médio por transação na área. Esta métrica é crucial para entender o perfil de vendas da região - áreas com ticket médio alto podem indicar produtos premium ou clientes corporativos, enquanto ticket médio baixo pode sugerir vendas de volume ou mercado popular.

### Análise Temporal

Uma das características mais valiosas dos módulos de área é a capacidade de análise temporal. O sistema apresenta gráficos de evolução que mostram:

**Evolução das Vendas Diárias**: Um gráfico de linha que conecta os valores de vendas dia a dia, permitindo identificar tendências, picos de vendas, quedas significativas e padrões sazonais. Pontos acima da linha de tendência podem indicar dias excepcionalmente bons, enquanto pontos abaixo podem sinalizar problemas ou oportunidades perdidas.

**Comparação com Meta Diária**: O gráfico inclui uma linha tracejada vermelha que representa a meta diária estabelecida para a área. Esta referência visual permite avaliar rapidamente quantos dias a área superou ou ficou abaixo da meta, fornecendo uma perspectiva clara da consistência da performance.

### Interpretação dos Padrões Temporais

Ao analisar os gráficos temporais, considere os seguintes padrões:

**Tendências Ascendentes**: Indicam crescimento sustentado e podem sugerir efetividade de campanhas de marketing, melhoria na qualidade do atendimento ou expansão da base de clientes.

**Tendências Descendentes**: Podem sinalizar problemas operacionais, aumento da concorrência, mudanças no mercado ou necessidade de ajustes na estratégia de vendas.

**Volatilidade Alta**: Grandes variações entre dias consecutivos podem indicar dependência de fatores externos, sazonalidade extrema ou inconsistência nos processos de vendas.

**Estabilidade**: Vendas consistentes próximas à meta podem indicar operações maduras e previsíveis, mas também podem sugerir falta de crescimento ou inovação.

### Dados Detalhados por Área

A tabela de dados detalhados em cada módulo de área inclui informações diárias específicas:

- **Data**: Dia específico da análise
- **Vendas Diárias**: Valor total vendido no dia
- **Número de Clientes**: Quantidade de clientes atendidos
- **Ticket Médio**: Valor médio por cliente no dia
- **Meta Diária**: Objetivo estabelecido para o dia
- **Percentual da Meta**: Performance do dia em relação à meta
- **Acumulado**: Soma progressiva das vendas desde o início do período

### Análise Comparativa Entre Áreas

Embora cada módulo seja independente, a análise comparativa entre Área 1 e Área 2 pode revelar insights valiosos:

**Performance Relativa**: Compare as vendas totais e médias entre as áreas para identificar qual está performando melhor e por quê.

**Padrões Temporais**: Verifique se ambas as áreas seguem padrões similares ou se há diferenças significativas que podem indicar fatores locais específicos.

**Eficiência Operacional**: Compare o número de clientes atendidos com o valor total de vendas para avaliar a eficiência de cada área.

**Consistência**: Analise qual área tem performance mais estável e previsível versus qual tem maior volatilidade.

### Utilizando os Insights para Ação

Os dados dos módulos de área podem ser utilizados para:

**Alocação de Recursos**: Direcionar mais recursos (pessoal, marketing, estoque) para áreas com maior potencial ou necessidade de suporte.

**Benchmarking Interno**: Usar a área de melhor performance como modelo para implementar melhorias na área de menor performance.

**Planejamento Estratégico**: Identificar oportunidades de expansão em áreas de alto desempenho ou necessidade de reestruturação em áreas problemáticas.

**Ajuste de Metas**: Revisar metas diárias com base na capacidade real demonstrada por cada área.

---

## 📊 Módulos Gráficos Individuais

### Propósito e Funcionalidade

Os módulos "Gráfico Individual 1" e "Gráfico Individual 2" são projetados para fornecer análises especializadas e visualizações customizadas que complementam as visões gerais oferecidas pelos outros módulos. Estas seções permitem mergulhar em aspectos específicos dos dados que requerem análise mais detalhada ou perspectivas únicas.

### Gráfico Individual 1 - Análise de Produtos

O primeiro módulo de gráfico individual foca na análise detalhada de produtos e vendas, oferecendo insights sobre o portfólio de produtos da empresa:

**Métricas Básicas**: O módulo apresenta informações fundamentais como total de registros (normalmente 20 produtos), número de colunas de dados (7 campos) e quantidade de colunas numéricas (5 campos), fornecendo uma visão da complexidade e riqueza dos dados de produtos.

**Gráfico de Correlação Principal**: A visualização principal é um gráfico de dispersão que mostra a correlação entre quantidade vendida e valor unitário dos produtos. Esta análise é fundamental para entender:
- Produtos de alto volume e baixo valor (quadrante inferior direito)
- Produtos premium de baixo volume e alto valor (quadrante superior esquerdo)  
- Produtos balanceados (centro do gráfico)
- Outliers que podem representar oportunidades ou problemas

### Análise de Vendas por Produto

A seção "Análise de Vendas por Produto" oferece duas visualizações complementares:

**Top 5 Produtos por Valor**: Um gráfico de barras que identifica os produtos mais lucrativos em termos de valor total de vendas. Esta informação é crucial para:
- Identificar os produtos que mais contribuem para a receita
- Focar esforços de marketing e vendas nos itens mais rentáveis
- Garantir disponibilidade adequada dos produtos principais
- Desenvolver estratégias de cross-selling baseadas nos produtos populares

**Vendas por Categoria**: Um gráfico de pizza que mostra a distribuição de vendas entre diferentes categorias de produtos (Eletrônicos, Roupas, Casa, Esporte). Esta visualização permite:
- Entender quais categorias dominam o portfólio
- Identificar oportunidades de diversificação
- Avaliar o equilíbrio do mix de produtos
- Planejar estratégias específicas por categoria

### Gráfico Individual 2 - Análise de Vendedores

O segundo módulo individual concentra-se na análise detalhada da performance e características dos vendedores:

**Métricas de Performance**: Similar ao primeiro módulo, apresenta estatísticas básicas sobre os dados de vendedores, incluindo número de registros, colunas disponíveis e campos numéricos para análise.

**Gráfico de Correlação de Vendedores**: A visualização principal correlaciona diferentes aspectos da performance dos vendedores, como vendas mensais versus experiência, ou comissão versus performance score.

### Análise de Performance de Vendedores

Esta seção oferece insights específicos sobre a equipe de vendas:

**Top 5 Vendedores por Performance**: Identifica os vendedores com melhor performance score, considerando não apenas vendas, mas também fatores como experiência e consistência. Esta análise ajuda a:
- Reconhecer top performers para programas de incentivo
- Identificar mentores potenciais para novos vendedores
- Entender características comuns dos melhores vendedores
- Desenvolver programas de desenvolvimento baseados em sucessos comprovados

**Performance Média por Região**: Analisa como diferentes regiões (Norte, Sul, Centro, Online) performam em média, revelando:
- Diferenças regionais na efetividade de vendas
- Oportunidades de expansão em regiões de alta performance
- Necessidades de suporte em regiões de baixa performance
- Impacto de fatores geográficos ou demográficos nas vendas

### Dados Detalhados dos Gráficos Individuais

Ambos os módulos incluem tabelas detalhadas com todos os dados utilizados nas análises:

**Gráfico Individual 1 - Dados de Produtos**:
- Produto: Nome ou código do produto
- Quantidade Vendida: Volume de unidades vendidas
- Valor Unitário: Preço por unidade
- Margem de Lucro: Percentual de lucro sobre o preço
- Categoria: Classificação do produto
- Valor Total: Receita total gerada pelo produto
- Lucro: Valor absoluto do lucro gerado

**Gráfico Individual 2 - Dados de Vendedores**:
- Vendedor: Nome do vendedor
- Vendas do Mês: Valor total vendido no período
- Comissão: Percentual de comissão do vendedor
- Experiência (Anos): Tempo de experiência em vendas
- Região: Área de atuação do vendedor
- Valor da Comissão: Valor absoluto da comissão
- Performance Score: Métrica composta de performance

### Utilizando as Análises Individuais

Os insights dos gráficos individuais podem ser aplicados em diversas estratégias:

**Otimização de Portfólio**: Use os dados de produtos para ajustar o mix de produtos, descontinuar itens de baixa performance e investir em categorias promissoras.

**Desenvolvimento de Equipe**: Aplique os insights de performance dos vendedores para criar programas de treinamento personalizados e estratégias de desenvolvimento de carreira.

**Estratégias Regionais**: Desenvolva abordagens específicas para cada região baseadas nas diferenças de performance identificadas.

**Planejamento de Incentivos**: Crie programas de incentivo que considerem tanto volume de vendas quanto outros fatores de performance identificados nas análises.

---

## ⚙️ Controles e Configurações

### Barra Lateral (Sidebar)

A barra lateral esquerda do dashboard contém controles essenciais e informações do sistema que permitem aos usuários gerenciar sua experiência e monitorar o status da aplicação.

### Controles de Teste

**Botão Regenerar Dados de Teste**: Este botão vermelho permite aos usuários em ambiente de teste gerar novos dados simulados. Quando clicado, o sistema:
- Cria novos dados aleatórios para todas as cinco abas
- Limpa o cache existente para forçar o recarregamento
- Atualiza automaticamente todas as visualizações
- Mantém a estrutura de dados consistente para garantir compatibilidade

Este controle é especialmente útil durante demonstrações ou testes, permitindo mostrar como o sistema responde a diferentes cenários de dados.

### Status do Sistema

A seção de status fornece informações em tempo real sobre o funcionamento do dashboard:

**Modo de Teste Ativo**: Indica quando o sistema está operando com dados simulados, garantindo que os usuários não confundam dados de teste com informações reais de produção.

**Dados Simulados OK**: Confirma que os dados de teste foram carregados com sucesso e estão prontos para análise.

**Última Atualização**: Mostra o timestamp da última vez que os dados foram processados, permitindo aos usuários entender a atualidade das informações apresentadas.

### Informações Técnicas

**Fonte de Dados**: Especifica de onde os dados estão sendo obtidos (arquivo Excel local em modo de teste, ou API da Eloca em produção).

**Cache**: Indica o tempo de vida do cache (normalmente 60 segundos em teste, 1 hora em produção), informando aos usuários com que frequência os dados são atualizados automaticamente.

**Debug**: Mostra se o modo de debug está habilitado, fornecendo informações adicionais para solução de problemas quando necessário.

### Dados de Teste - Resumo

A sidebar também apresenta um resumo rápido dos dados disponíveis:
- Metas Individuais (10 registros)
- Resultados área 1 (15 registros)  
- Resultados área 2 (15 registros)
- Gráfico Individual 1 (20 registros)
- Gráfico Individual 2 (20 registros)

Esta informação permite aos usuários entender rapidamente o volume de dados disponível em cada seção antes de navegar para análises específicas.

### Atualização Manual

Embora o sistema tenha cache automático, o botão "🔄 Regenerar Dados de Teste" permite forçar uma atualização manual quando necessário. Isso é útil quando:
- Você suspeita que os dados podem estar desatualizados
- Houve mudanças na fonte de dados que precisam ser refletidas imediatamente
- Você está demonstrando o sistema e quer mostrar dados diferentes

### Interpretação dos Indicadores de Status

**Indicadores Verdes (✅)**: Mostram que os sistemas estão funcionando corretamente e os dados estão disponíveis.

**Indicadores Amarelos (⚠️)**: Podem aparecer para avisos não críticos, como dados parcialmente carregados ou configurações não otimizadas.

**Indicadores Vermelhos (❌)**: Indicam problemas que impedem o funcionamento normal do sistema e requerem atenção imediata.

---

## 🔧 Solução de Problemas

### Problemas Comuns e Soluções

**Página Não Carrega ou Carrega Lentamente**

Se o dashboard não carregar adequadamente ou apresentar lentidão excessiva:

Primeiro, verifique sua conexão com a internet. O dashboard requer uma conexão estável para carregar dados e renderizar visualizações. Teste acessando outros sites para confirmar que sua conexão está funcionando adequadamente.

Segundo, limpe o cache do seu navegador. Dados antigos em cache podem interferir com o carregamento de versões atualizadas do dashboard. No Chrome, use Ctrl+Shift+R (Windows) ou Cmd+Shift+R (Mac) para forçar uma atualização completa.

Terceiro, verifique se você está usando um navegador suportado. O dashboard funciona melhor em versões recentes do Chrome, Firefox, Safari ou Edge. Navegadores muito antigos podem não suportar todas as funcionalidades.

**Dados Não Aparecem ou Aparecem Incorretamente**

Quando os dados não são exibidos ou parecem incorretos:

Verifique o status do sistema na barra lateral. Se houver indicadores vermelhos ou mensagens de erro, isso pode indicar problemas na fonte de dados ou conectividade.

Tente usar o botão "Regenerar Dados" na barra lateral para forçar uma atualização. Em ambiente de teste, isso criará novos dados simulados. Em produção, isso forçará uma nova consulta à fonte de dados.

Observe se há mensagens de erro na parte superior da página. O sistema fornece feedback específico sobre problemas de carregamento de dados, incluindo códigos de erro HTTP e descrições do problema.

**Gráficos Não Renderizam**

Se os gráficos aparecem em branco ou não carregam:

Aguarde alguns segundos adicionais, pois gráficos complexos podem levar tempo para renderizar, especialmente com grandes volumes de dados.

Verifique se o JavaScript está habilitado em seu navegador. O dashboard depende de JavaScript para funcionar adequadamente, e navegadores com JavaScript desabilitado não conseguirão exibir as visualizações.

Tente reduzir o zoom da página. Alguns gráficos podem não renderizar corretamente em níveis de zoom muito altos ou muito baixos.

**Navegação Entre Abas Não Funciona**

Se clicar nas abas do menu não muda o conteúdo:

Aguarde que a página atual termine de carregar completamente antes de tentar navegar para outra seção.

Verifique se não há mensagens de erro JavaScript no console do navegador (pressione F12 para abrir as ferramentas de desenvolvedor).

Tente recarregar a página completamente e navegar novamente.

### Problemas de Performance

**Sistema Lento ou Travando**

Para melhorar a performance do dashboard:

Feche outras abas do navegador que possam estar consumindo recursos do sistema, especialmente outras aplicações web pesadas.

Verifique se seu computador tem recursos suficientes disponíveis. O dashboard pode consumir memória significativa ao processar grandes volumes de dados.

Em dispositivos móveis ou tablets, considere usar o modo paisagem para melhor visualização e performance.

**Gráficos Demoram para Carregar**

Se as visualizações estão lentas:

Verifique sua conexão com a internet, pois gráficos interativos podem requerer transferência de dados adicional.

Considere que a primeira visualização de cada tipo de gráfico pode ser mais lenta, pois o sistema precisa carregar bibliotecas específicas.

Em casos de lentidão persistente, tente acessar o dashboard em horários de menor uso da rede.

### Problemas de Visualização

**Texto Muito Pequeno ou Grande**

Para ajustar o tamanho do texto:

Use os controles de zoom do navegador (Ctrl + ou Ctrl - no Windows, Cmd + ou Cmd - no Mac) para ajustar o tamanho geral da página.

Verifique as configurações de acessibilidade do seu sistema operacional se você tem necessidades específicas de visualização.

**Cores Difíceis de Distinguir**

Se você tem dificuldade para distinguir cores nos gráficos:

O dashboard usa uma paleta de cores projetada para ser acessível, mas configurações de acessibilidade do sistema operacional podem ajudar.

Considere usar as tabelas de dados detalhados como alternativa às visualizações gráficas quando necessário.

### Obtendo Suporte Adicional

**Informações para Suporte Técnico**

Quando precisar de suporte técnico, tenha as seguintes informações disponíveis:

- Navegador e versão que você está usando
- Sistema operacional (Windows, Mac, Linux, iOS, Android)
- Mensagens de erro específicas que aparecem na tela
- Passos exatos que levaram ao problema
- Screenshot da tela quando o problema ocorre

**Logs de Debug**

Se o modo debug estiver habilitado (visível na barra lateral), informações adicionais de diagnóstico estarão disponíveis no console do navegador. Para acessar:

1. Pressione F12 para abrir as ferramentas de desenvolvedor
2. Clique na aba "Console"
3. Procure por mensagens de erro em vermelho ou avisos em amarelo
4. Copie essas mensagens para incluir em solicitações de suporte

**Verificação de Status do Sistema**

Antes de reportar problemas, verifique:

- Se outros usuários estão enfrentando problemas similares
- Se há manutenção programada do sistema
- Se sua organização tem políticas de firewall que podem estar bloqueando o acesso
- Se você tem as permissões necessárias para acessar o dashboard

---

## 📱 Compatibilidade e Requisitos

### Navegadores Suportados

O Dashboard Eloca foi desenvolvido para funcionar em navegadores web modernos que suportam tecnologias web atuais. A compatibilidade foi testada e otimizada para os seguintes navegadores:

**Google Chrome**: Versão 90 ou superior. Chrome oferece a melhor experiência com o dashboard, incluindo performance otimizada para gráficos interativos e suporte completo a todas as funcionalidades. Recomendamos manter o Chrome atualizado para a versão mais recente.

**Mozilla Firefox**: Versão 88 ou superior. Firefox oferece excelente compatibilidade com todas as funcionalidades do dashboard. Usuários do Firefox podem experimentar pequenas diferenças na renderização de gráficos, mas todas as funcionalidades permanecem totalmente operacionais.

**Safari**: Versão 14 ou superior (macOS e iOS). Safari em dispositivos Apple oferece boa compatibilidade, especialmente em dispositivos móveis. Algumas animações podem ser ligeiramente diferentes, mas a funcionalidade core permanece intacta.

**Microsoft Edge**: Versão 90 ou superior. A versão moderna do Edge (baseada em Chromium) oferece excelente compatibilidade, similar ao Chrome. Versões antigas do Edge (EdgeHTML) não são suportadas.

### Dispositivos e Plataformas

**Computadores Desktop e Laptop**:
- Windows 10 ou superior
- macOS 10.15 (Catalina) ou superior  
- Linux (distribuições modernas com navegadores atualizados)
- Resolução mínima recomendada: 1366x768
- Resolução otimizada: 1920x1080 ou superior

**Tablets**:
- iPad (iOS 14 ou superior)
- Tablets Android (Android 8.0 ou superior)
- Tablets Windows (Windows 10 ou superior)
- Orientação recomendada: paisagem para melhor visualização de gráficos

**Smartphones**:
- iPhone (iOS 14 ou superior)
- Android (versão 8.0 ou superior)
- O dashboard é responsivo, mas a experiência é otimizada para telas maiores

### Requisitos de Sistema

**Conexão com Internet**:
- Conexão banda larga recomendada (mínimo 5 Mbps)
- Conexão estável para carregamento de dados em tempo real
- Latência baixa para melhor responsividade da interface

**Hardware Mínimo**:
- RAM: 4GB (8GB recomendado para melhor performance)
- Processador: Dual-core 2.0 GHz ou superior
- Espaço em disco: 100MB livres para cache do navegador

**Hardware Recomendado**:
- RAM: 8GB ou superior
- Processador: Quad-core 2.5 GHz ou superior
- Placa gráfica dedicada (opcional, mas melhora performance de visualizações)

### Configurações de Rede

**Portas e Protocolos**:
- HTTPS (porta 443) para acesso seguro
- WebSocket support para atualizações em tempo real
- JavaScript habilitado (essencial para funcionamento)

**Firewall e Proxy**:
- Acesso liberado para domínios do Streamlit Cloud
- Suporte a conexões WebSocket
- Cookies habilitados para manter sessão

### Limitações Conhecidas

**Navegadores Não Suportados**:
- Internet Explorer (todas as versões)
- Versões muito antigas de qualquer navegador (anterior a 2020)
- Navegadores com JavaScript desabilitado

**Funcionalidades Limitadas**:
- Impressão de gráficos pode ter qualidade reduzida em alguns navegadores
- Exportação de dados não está disponível na versão atual
- Modo offline não é suportado

### Otimização por Dispositivo

**Desktop/Laptop**:
- Interface completa com todas as funcionalidades
- Gráficos em tamanho completo
- Sidebar sempre visível
- Suporte a atalhos de teclado

**Tablet**:
- Interface adaptada para toque
- Gráficos otimizados para tela média
- Sidebar colapsível para economizar espaço
- Gestos de toque para navegação

**Smartphone**:
- Interface compacta e otimizada
- Gráficos simplificados quando necessário
- Menu de navegação adaptado para toque
- Orientação automática suportada

### Verificação de Compatibilidade

Para verificar se seu dispositivo é compatível:

1. **Teste de Navegador**: Acesse a página inicial do dashboard. Se carregar corretamente, seu navegador é compatível.

2. **Teste de JavaScript**: O dashboard exibirá uma mensagem de erro se JavaScript estiver desabilitado.

3. **Teste de Performance**: Navegue entre diferentes abas. Se a transição for suave, seu dispositivo tem performance adequada.

4. **Teste de Gráficos**: Verifique se os gráficos carregam e são interativos (zoom, hover, etc.).

### Atualizações e Manutenção

**Atualizações Automáticas**:
- O dashboard é atualizado automaticamente quando você recarrega a página
- Não há necessidade de instalar atualizações manualmente
- Novas funcionalidades são disponibilizadas automaticamente

**Cache do Navegador**:
- Limpe o cache periodicamente para garantir que está usando a versão mais recente
- Use Ctrl+F5 (Windows) ou Cmd+Shift+R (Mac) para forçar atualização completa

**Manutenção Programada**:
- Manutenções são normalmente realizadas fora do horário comercial
- Usuários são notificados com antecedência sobre manutenções programadas
- Durante manutenção, uma página de status será exibida

---

## 🔒 Segurança e Privacidade

### Proteção de Dados

O Dashboard Eloca foi desenvolvido com foco na segurança e proteção dos dados empresariais. Todas as informações processadas pelo sistema são tratadas com o mais alto nível de confidencialidade e proteção técnica.

**Criptografia de Dados**: Todas as comunicações entre seu navegador e o servidor do dashboard utilizam criptografia HTTPS com certificados SSL/TLS atualizados. Isso garante que os dados transmitidos não possam ser interceptados ou modificados durante o transporte.

**Autenticação Segura**: O acesso aos dados da Eloca é protegido por tokens de autenticação específicos que são validados a cada requisição. Estes tokens têm validade limitada e são renovados automaticamente para manter a segurança contínua.

**Isolamento de Dados**: Cada instância do dashboard opera de forma isolada, garantindo que os dados de uma organização não sejam acessíveis por outras. O sistema utiliza identificadores únicos para manter a separação completa entre diferentes clientes.

### Privacidade dos Usuários

**Coleta de Dados Mínima**: O dashboard coleta apenas as informações estritamente necessárias para seu funcionamento. Não são coletados dados pessoais dos usuários além daqueles já presentes nos dados de vendas da Eloca.

**Não Rastreamento**: O sistema não utiliza cookies de rastreamento, analytics de terceiros ou qualquer forma de monitoramento de comportamento do usuário para fins comerciais ou publicitários.

**Logs de Acesso**: Logs de acesso são mantidos apenas para fins de segurança e diagnóstico técnico, contendo informações básicas como horário de acesso e endereço IP, sem identificação pessoal.

### Configurações de Segurança

**Variáveis de Ambiente**: Todas as credenciais e configurações sensíveis são armazenadas como variáveis de ambiente criptografadas, nunca expostas no código fonte ou interface do usuário.

**Validação de Entrada**: Todos os dados recebidos pelo sistema passam por validação rigorosa para prevenir ataques de injeção ou manipulação maliciosa.

**Timeout de Sessão**: Sessões inativas são automaticamente encerradas após um período determinado para prevenir acesso não autorizado em caso de dispositivo desatendido.

### Boas Práticas para Usuários

**Acesso Seguro**: Sempre acesse o dashboard através da URL oficial fornecida pelo administrador do sistema. Evite clicar em links suspeitos ou acessar através de sites de terceiros.

**Logout Adequado**: Embora o sistema tenha timeout automático, sempre feche o navegador ou aba quando terminar de usar o dashboard, especialmente em computadores compartilhados.

**Senhas Seguras**: Se sua organização implementar autenticação adicional, use senhas fortes e únicas para o acesso ao sistema.

**Atualizações de Navegador**: Mantenha seu navegador sempre atualizado para garantir que você tenha as últimas correções de segurança.

### Conformidade e Regulamentações

**LGPD (Lei Geral de Proteção de Dados)**: O sistema foi desenvolvido em conformidade com os princípios da LGPD, processando apenas dados necessários para a finalidade específica de análise de vendas.

**Retenção de Dados**: Os dados são mantidos em cache apenas pelo tempo necessário para performance do sistema (configurável, normalmente 1 hora), sendo descartados automaticamente após este período.

**Direitos dos Titulares**: Usuários têm direito de solicitar informações sobre como seus dados são processados, bem como solicitar correções ou exclusões quando aplicável.

### Monitoramento de Segurança

**Detecção de Anomalias**: O sistema monitora padrões de acesso anômalos que possam indicar tentativas de acesso não autorizado ou uso inadequado.

**Logs de Auditoria**: Todas as ações significativas no sistema são registradas em logs de auditoria para permitir investigação em caso de incidentes de segurança.

**Atualizações de Segurança**: O sistema é regularmente atualizado com as últimas correções de segurança e patches de vulnerabilidades conhecidas.

### Incidentes de Segurança

**Procedimentos de Resposta**: Em caso de suspeita de incidente de segurança, o sistema possui procedimentos estabelecidos para contenção, investigação e notificação apropriada.

**Contato de Emergência**: Para reportar problemas de segurança, entre em contato imediatamente com o administrador do sistema ou equipe de TI da sua organização.

**Backup e Recuperação**: Embora o dashboard não armazene dados permanentemente, existem procedimentos de backup para configurações e logs críticos do sistema.

### Responsabilidades Compartilhadas

**Responsabilidade do Sistema**: O dashboard é responsável por manter a segurança técnica, criptografia, validação de dados e proteção da infraestrutura.

**Responsabilidade do Usuário**: Usuários são responsáveis por manter a segurança de seus dispositivos, usar o sistema adequadamente e reportar problemas de segurança quando identificados.

**Responsabilidade Organizacional**: A organização é responsável por definir políticas de acesso, treinar usuários e manter a segurança dos dados na fonte (sistema Eloca).

---

## 📞 Suporte e Contato

### Canais de Suporte

O suporte ao Dashboard Eloca está disponível através de múltiplos canais para garantir que você receba a assistência necessária de forma rápida e eficiente.

**Suporte Técnico Interno**: Para questões relacionadas ao funcionamento do dashboard, problemas de acesso ou dúvidas sobre funcionalidades, entre em contato com a equipe de TI da sua organização. Eles têm acesso direto aos logs do sistema e podem resolver a maioria dos problemas técnicos rapidamente.

**Administrador do Sistema**: Para questões sobre configurações, permissões de acesso ou solicitações de novas funcionalidades, contate o administrador designado do dashboard em sua organização. Esta pessoa tem autoridade para fazer alterações nas configurações e pode coordenar atualizações ou melhorias.

**Suporte da Eloca**: Para problemas relacionados aos dados fonte ou à integração com a plataforma Eloca, utilize os canais de suporte oficiais da Eloca (Desk.ms). Eles podem ajudar com questões sobre a qualidade dos dados, configuração de tokens de acesso ou problemas na fonte de dados.

### Informações Necessárias para Suporte

Quando solicitar suporte, forneça as seguintes informações para acelerar o processo de resolução:

**Informações do Sistema**:
- URL exata que você está acessando
- Navegador e versão (ex: Chrome 91.0.4472.124)
- Sistema operacional (ex: Windows 10, macOS Big Sur)
- Dispositivo utilizado (desktop, laptop, tablet, smartphone)

**Descrição do Problema**:
- Descrição detalhada do que você estava tentando fazer
- Passos exatos que levaram ao problema
- Mensagens de erro específicas (copie o texto exato)
- Horário aproximado quando o problema ocorreu

**Screenshots e Evidências**:
- Capture screenshots da tela quando o problema ocorre
- Se possível, grave um vídeo curto mostrando o problema
- Inclua a barra lateral para mostrar informações de status
- Capture qualquer mensagem de erro que apareça

### Problemas Comuns e Soluções Rápidas

Antes de entrar em contato com o suporte, tente estas soluções para problemas comuns:

**Dashboard Não Carrega**:
1. Verifique sua conexão com a internet
2. Tente acessar em uma aba privada/incógnita do navegador
3. Limpe o cache e cookies do navegador
4. Tente usar um navegador diferente
5. Verifique se JavaScript está habilitado

**Dados Não Aparecem**:
1. Aguarde alguns minutos para o carregamento completo
2. Clique no botão "Regenerar Dados" na barra lateral
3. Verifique se há mensagens de erro na parte superior da página
4. Recarregue a página completamente (Ctrl+F5 ou Cmd+Shift+R)

**Gráficos Não Funcionam**:
1. Aguarde o carregamento completo da página
2. Verifique se o zoom da página está em 100%
3. Tente redimensionar a janela do navegador
4. Desabilite extensões do navegador temporariamente

### Horários de Suporte

**Suporte Técnico Interno**: Disponível durante o horário comercial da sua organização, normalmente das 8h às 18h em dias úteis.

**Suporte de Emergência**: Para problemas críticos que impedem o funcionamento do negócio, pode haver suporte fora do horário comercial. Consulte as políticas da sua organização.

**Suporte da Eloca**: Siga os horários e canais oficiais de suporte da plataforma Eloca conforme documentado em seus termos de serviço.

### Atualizações e Melhorias

**Solicitações de Funcionalidades**: Se você tem sugestões para melhorias ou novas funcionalidades, documente detalhadamente sua necessidade e envie para o administrador do sistema. Inclua:
- Descrição da funcionalidade desejada
- Justificativa de negócio para a implementação
- Exemplos de como seria utilizada
- Prioridade em relação a outras necessidades

**Feedback sobre Usabilidade**: Comentários sobre a experiência do usuário são sempre bem-vindos e ajudam a melhorar o sistema. Inclua:
- Aspectos que funcionam bem
- Pontos de dificuldade ou confusão
- Sugestões específicas de melhoria
- Comparações com outras ferramentas que você usa

### Treinamento e Capacitação

**Sessões de Treinamento**: Sua organização pode organizar sessões de treinamento para novos usuários ou quando novas funcionalidades são implementadas. Consulte o administrador do sistema sobre disponibilidade.

**Documentação Adicional**: Este manual é atualizado regularmente. Verifique se você tem a versão mais recente e consulte-o antes de solicitar suporte para dúvidas básicas.

**Recursos de Aprendizado**: Para usuários que desejam se aprofundar em análise de dados, considere treinamentos em ferramentas de BI, Excel avançado ou conceitos de análise de vendas.

### Manutenção e Atualizações

**Notificações de Manutenção**: Usuários são notificados com antecedência sobre manutenções programadas que possam afetar o acesso ao dashboard.

**Atualizações de Funcionalidades**: Quando novas funcionalidades são implementadas, os usuários recebem comunicação sobre as mudanças e como utilizá-las.

**Histórico de Versões**: Mantenha-se informado sobre as atualizações do sistema através dos canais de comunicação da sua organização.

### Escalação de Problemas

**Nível 1 - Suporte Básico**: Problemas simples de navegação, dúvidas sobre funcionalidades básicas, questões de acesso.

**Nível 2 - Suporte Técnico**: Problemas de performance, erros de sistema, questões de integração de dados.

**Nível 3 - Suporte Especializado**: Problemas complexos de infraestrutura, desenvolvimento de novas funcionalidades, questões de segurança.

### Qualidade do Suporte

**Tempo de Resposta**: 
- Problemas críticos: 2 horas durante horário comercial
- Problemas importantes: 24 horas
- Dúvidas gerais: 48 horas
- Solicitações de melhoria: 1 semana

**Resolução de Problemas**:
- Problemas simples: Resolução imediata
- Problemas técnicos: 1-3 dias úteis
- Problemas complexos: 1-2 semanas
- Novas funcionalidades: Conforme cronograma de desenvolvimento

**Satisfação do Cliente**: Após a resolução de problemas, você pode ser contatado para avaliar a qualidade do suporte recebido e sugerir melhorias no processo.

---

## 📚 Glossário de Termos

### Termos Técnicos

**API (Application Programming Interface)**: Interface de programação que permite a comunicação entre diferentes sistemas. No contexto do Dashboard Eloca, refere-se à conexão com a plataforma Eloca para obter dados de vendas.

**Cache**: Armazenamento temporário de dados para melhorar a performance do sistema. O dashboard utiliza cache para evitar recarregar dados desnecessariamente, com tempo de vida configurável (TTL).

**CSV (Comma-Separated Values)**: Formato de arquivo que armazena dados tabulares usando vírgulas para separar valores. Embora o dashboard processe arquivos Excel, alguns dados podem ser exportados ou importados em formato CSV.

**Dashboard**: Painel de controle visual que apresenta informações importantes de forma organizada e fácil de entender. O Dashboard Eloca é especificamente projetado para dados de vendas.

**Eloca (Desk.ms)**: Plataforma de gestão empresarial que fornece os dados fonte para o dashboard. É o sistema onde as informações de vendas são originalmente registradas e mantidas.

**Excel (.xlsx)**: Formato de arquivo de planilha da Microsoft que o dashboard processa para extrair dados das cinco abas especificadas.

**HTTPS**: Protocolo de comunicação seguro que criptografa dados transmitidos entre o navegador e o servidor, garantindo segurança das informações.

**JavaScript**: Linguagem de programação utilizada para criar interatividade no dashboard. Deve estar habilitado no navegador para o funcionamento adequado.

**JSON (JavaScript Object Notation)**: Formato de dados utilizado para comunicação entre sistemas. O dashboard pode processar dados em formato JSON quando necessário.

**Plotly**: Biblioteca de visualização de dados utilizada para criar os gráficos interativos do dashboard. Permite zoom, hover e outras interações com os gráficos.

**Streamlit**: Framework utilizado para desenvolver o dashboard. Permite criar aplicações web interativas usando Python.

**TTL (Time To Live)**: Tempo de vida do cache, determinando por quanto tempo os dados ficam armazenados antes de serem atualizados automaticamente.

**Token de Autenticação**: Código único utilizado para autenticar e autorizar o acesso aos dados da Eloca. Funciona como uma "chave" digital para acessar informações específicas.

**URL (Uniform Resource Locator)**: Endereço web utilizado para acessar o dashboard. Cada instalação tem sua URL específica.

### Termos de Vendas e Negócios

**Atingimento de Meta**: Percentual que indica quanto da meta estabelecida foi efetivamente realizado. Calculado como (Realizado / Meta) × 100.

**Comissão**: Percentual ou valor pago aos vendedores baseado em suas vendas. Pode variar conforme experiência, região ou tipo de produto.

**Meta Diária**: Objetivo de vendas estabelecido para cada dia, normalmente calculado dividindo a meta mensal pelo número de dias úteis.

**Meta Individual**: Objetivo de vendas estabelecido especificamente para cada vendedor, considerando fatores como experiência, território e histórico.

**Meta Mensal**: Objetivo de vendas estabelecido para um período de um mês, podendo ser individual ou por área/região.

**Performance Score**: Métrica composta que considera múltiplos fatores além do volume de vendas, como consistência, experiência e outros indicadores de qualidade.

**Realizado**: Valor efetivamente vendido em um período específico, contrastando com a meta estabelecida.

**Ticket Médio**: Valor médio por transação ou cliente, calculado dividindo o valor total de vendas pelo número de transações ou clientes.

**Top Performer**: Vendedor ou área com melhor performance em um período específico, normalmente identificado pelo maior percentual de atingimento de meta.

**Vendas Acumuladas**: Soma progressiva das vendas desde o início de um período específico, útil para acompanhar evolução ao longo do tempo.

### Termos de Interface e Usabilidade

**Aba**: Seção específica do dashboard que apresenta um tipo particular de análise (Metas Individuais, Resultados por Área, etc.).

**Barra Lateral (Sidebar)**: Área lateral da interface que contém controles, informações de status e configurações do sistema.

**Gráfico de Barras**: Visualização que usa barras retangulares para representar valores, facilitando comparações entre diferentes categorias.

**Gráfico de Dispersão**: Visualização que mostra a relação entre duas variáveis numéricas, útil para identificar correlações.

**Gráfico de Linha**: Visualização que conecta pontos de dados para mostrar tendências ao longo do tempo.

**Gráfico de Pizza**: Visualização circular que mostra proporções de um todo, útil para mostrar distribuições percentuais.

**Hover**: Ação de posicionar o cursor sobre um elemento da interface para ver informações adicionais sem clicar.

**Menu Horizontal**: Barra de navegação na parte superior da interface que permite alternar entre diferentes seções do dashboard.

**Métrica**: Valor numérico específico que mede um aspecto particular do negócio, como total de vendas ou número de clientes.

**Responsivo**: Característica da interface que se adapta automaticamente a diferentes tamanhos de tela e dispositivos.

**Zoom**: Funcionalidade que permite ampliar ou reduzir a visualização de gráficos para melhor análise de detalhes.

### Termos de Análise de Dados

**Correlação**: Relação estatística entre duas variáveis, indicando se elas tendem a variar juntas de forma positiva ou negativa.

**Distribuição**: Forma como os valores de uma variável estão espalhados ou concentrados em diferentes faixas.

**Histograma**: Gráfico que mostra a distribuição de frequência de uma variável numérica, dividindo os dados em intervalos.

**Outlier**: Valor que se destaca significativamente dos demais em um conjunto de dados, podendo indicar casos excepcionais.

**Percentil**: Valor abaixo do qual uma determinada porcentagem dos dados se encontra. Por exemplo, o percentil 90 indica que 90% dos dados estão abaixo desse valor.

**Tendência**: Direção geral que os dados seguem ao longo do tempo, podendo ser ascendente, descendente ou estável.

**Variabilidade**: Medida de quanto os dados se dispersam em relação à média, indicando consistência ou volatilidade.

**Visualização**: Representação gráfica de dados que facilita a compreensão de padrões, tendências e insights.

### Termos de Sistema e Configuração

**Ambiente de Produção**: Versão do sistema que utiliza dados reais e é usada para operações normais do negócio.

**Ambiente de Teste**: Versão do sistema que utiliza dados simulados para demonstrações, treinamentos ou testes de funcionalidades.

**Debug**: Modo de operação que fornece informações técnicas adicionais para identificação e correção de problemas.

**Deploy**: Processo de disponibilizar o sistema para uso, incluindo configuração de servidores e ambientes.

**Log**: Registro de eventos e atividades do sistema, útil para monitoramento e solução de problemas.

**Modo de Teste**: Estado do sistema quando está operando com dados simulados, claramente identificado na interface.

**Regenerar Dados**: Ação que força a criação de novos dados de teste ou atualização dos dados reais, limpando o cache existente.

**Status do Sistema**: Informações sobre o funcionamento atual do dashboard, incluindo conectividade, carregamento de dados e possíveis problemas.

Este glossário serve como referência rápida para termos utilizados no dashboard e em discussões relacionadas à análise de vendas e uso do sistema.

