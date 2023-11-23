# Builders - WorkerAnalyzer

## Visão Geral
A seção de "Builders" da biblioteca WorkerAnalyzer consiste em classes auxiliares projetadas para facilitar a construção e o gerenciamento de métricas de monitoramento. Estas classes permitem aos usuários criar métricas detalhadas com menos esforço e maior precisão.

## Classes de Builders

### DefaultMetricsBuilder
- **Descrição:** Constrói métricas com base na contagem de diferentes estados (sucesso, falha, em branco).
- **Funcionalidades:**
  - Iniciar e encerrar a coleta de métricas.
  - Registrar diferentes estados e conteúdos de erro.
  - Gerar um dicionário de métricas com contagens e durações.
  - Adicionar atributos adicionais às métricas.
- **Uso:** Ideal para situações onde a contagem de eventos específicos e a análise de erros são essenciais.

### SimpleMetricsBuilder
- **Descrição:** Semelhante ao `DefaultMetricsBuilder`, mas focado apenas no estado geral, sem contar eventos individuais.
- **Funcionalidades:**
  - Métodos para iniciar e encerrar a coleta, similares ao `DefaultMetricsBuilder`.
  - Permite adicionar métricas adicionais e definir o estado final baseado no status fornecido.
- **Uso:** Útil quando apenas o estado final é necessário, sem a necessidade de contagem detalhada de eventos.

### UnionMetrics
- **Descrição:** Combina métricas de diferentes fontes em uma lista única.
- **Funcionalidades:**
  - Adicionar métricas a uma lista.
  - Limpar a lista de métricas.
  - Definir o estado geral com base nas métricas coletadas.
- **Uso:** Perfeito para consolidar métricas de várias fontes e obter uma visão agregada.

## Vantagens do Uso dos Builders
- **Redução de Complexidade:** Diminui a complexidade de codificação ao gerar métricas, abstraindo detalhes técnicos.
- **Flexibilidade:** Oferece flexibilidade para personalizar métricas e adaptar-se a diferentes cenários de monitoramento.
- **Precisão de Dados:** Assegura a precisão dos dados coletados e facilita a análise posterior.

## Exemplo de Uso

```python
from workeranalyzer.builders import DefaultMetricsBuilder

# Criando um objeto DefaultMetricsBuilder
metrics_builder = DefaultMetricsBuilder("Data Load Metrics")
metrics_builder.start()

# Registrando eventos
metrics_builder.log("success")
metrics_builder.log("failure", error_content="Timeout Error")

# Finalizando a coleta de métricas
metrics_builder.end()

# Obtendo as métricas coletadas
metrics = metrics_builder.metrics
