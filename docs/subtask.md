# Classe SubTask - WorkerAnalyzer

## Objetivo e Uso
A classe `SubTask` é um componente essencial da biblioteca WorkerAnalyzer, utilizada para representar e gerenciar subtarefas dentro de uma tarefa maior. Esta classe facilita o monitoramento detalhado de operações específicas ou componentes menores de uma tarefa.

## Propriedades
- `id` (string): Identificador único para a subtarefa.
- `name` (string): Nome da subtarefa.
- `subtask_type` (string): Tipo ou categoria da subtarefa.
- `start_time` (datetime): Hora e data de início da subtarefa.
- `end_time` (datetime): Hora e data de término da subtarefa.
- `duration` (float): Duração total da subtarefa em segundos.
- `status` (string): Status atual da subtarefa (por exemplo, "In Progress", "Done").
- `metrics` (list): Lista de métricas associadas à subtarefa.

## Métodos Principais

### `start()`
Inicia a subtarefa, registrando o horário de início e definindo o status como "In Progress".

### `add_metrics(metrics)`
Adiciona métricas à subtarefa.
- `metrics` (dict): Dicionário representando as métricas a serem adicionadas.

### `get_status_by_metrics()`
Determina o status da subtarefa com base nas métricas coletadas.

### `end(status)`
Finaliza a subtarefa, registrando o horário de término e definindo o status final.
- `status` (string): Status final da subtarefa.

## Exemplo de Uso

```python
from workeranalyzer.analyzer import SubTask

# Criando uma nova subtarefa
subtask = SubTask(name="Data Validation", subtask_type="Validation")
subtask.start()

# Adicionando métricas
metrics_data = {"processed_items": 100, "errors": 2, ...}
subtask.add_metrics(metrics_data)

# Finalizando a subtarefa
subtask.end("success")
