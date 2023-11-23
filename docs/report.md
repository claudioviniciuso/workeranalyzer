# Report - WorkerAnalyzer

## Visão Geral
A seção "Report" da biblioteca WorkerAnalyzer é responsável por gerar relatórios detalhados a partir dos dados coletados durante as sessões de monitoramento. A classe `DefaultReport` transforma esses dados em insights compreensíveis e úteis.

## Classe DefaultReport

### Descrição
A classe `DefaultReport` é utilizada para criar relatórios abrangentes sobre as sessões de monitoramento. Ela analisa dados de sessões, tarefas e subtarefas, fornecendo um resumo detalhado do processo de execução.

### Funcionalidades
- **Geração de Relatório:** Cria um relatório estruturado com informações como ID da sessão, horários de início e término, duração, e detalhes das tarefas.
- **Formatação de Dados de Tarefas:** Processa e formata os dados das tarefas para inclusão no relatório final.
- **Análise Detalhada:** Fornece análises sobre o número de tarefas e subtarefas, bem como o percentual de falhas e execuções parciais.

### Uso
Ideal para gerar relatórios pós-execução que ajudam na análise e no entendimento do desempenho de processos ou pipelines de dados.

## Exemplo de Uso

```python
from workeranalyzer.report import DefaultReport

# Dados de uma sessão exemplo
session_data = {"id": "123", "tasks": [...], "start_time": "2021-01-01T00:00:00", ...}

# Criando um relatório a partir dos dados da sessão
report = DefaultReport(session_data)
report_content = report.generate_report()

# O `report_content` contém o relatório estruturado
