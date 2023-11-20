
# WorkerAnalyzer

## Descrição

WorkerAnalyzer é uma biblioteca Python projetada para facilitar a construção de métricas e monitoramento em pipelines de dados. Ela oferece ferramentas para rastrear a execução de sessões, tarefas e subtarefas, fornecendo insights detalhados sobre o desempenho e resultados de processos de dados.

## Funcionalidades

- **Sessão (`Session`)**: Representa uma execução completa do pipeline de dados, permitindo o rastreamento de várias tarefas e subtarefas.
- **Tarefa (`Task`)**: Monitora tarefas individuais dentro de uma sessão, com suporte a múltiplas subtarefas.
- **Subtarefa (`SubTask`)**: Componentes mais granulares de uma tarefa, cada um com suas próprias métricas e status.
- **Construtores de Métricas (`MetricsBuilder`)**: Ferramentas para criar métricas customizadas para tarefas e subtarefas.
- **Relatório (`Report`)**: Geração de relatórios detalhados sobre o desempenho e resultados das sessões.
- **Armazenamento Local (`LocalStorage`)**: Facilita o armazenamento e recuperação de dados de sessões em ambientes locais.

## Instalação

```bash
pip install worker_analyzer
```

## Uso Básico

### Criando uma Sessão

```python
from worker_analyzer import Session

session = Session()
session.start()
# Adicione tarefas e subtarefas...
session.end()
```

### Trabalhando com Tarefas e Subtarefas

```python
from worker_analyzer import Task, SubTask

task = Task('Nome da Tarefa')
task.start()
# Processamento da tarefa
task.end()

subtask = SubTask('Nome da Subtarefa', 'Tipo')
subtask.start()
# Processamento da subtarefa
subtask.end()
```

### Gerando um Relatório

```python
from worker_analyzer import Report

report = Report(session_data)
print(report.generate_report())
```

## Contribuição

Contribuições para o `worker_analyzer` são bem-vindas! Por favor, leia as diretrizes de contribuição para mais informações.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
