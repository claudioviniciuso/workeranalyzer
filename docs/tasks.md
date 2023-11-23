# Classe Task - WorkerAnalyzer

## Objetivo e Uso
A classe `Task` é uma parte crucial da biblioteca WorkerAnalyzer, destinada a gerenciar tarefas individuais dentro de uma sessão. Esta classe permite monitorar detalhadamente cada tarefa, incluindo seu início, duração, status e as subtarefas associadas.

## Propriedades
- `id` (string): Um identificador único para a tarefa.
- `name` (string): Nome da tarefa.
- `start_time` (datetime): Hora e data de início da tarefa.
- `end_time` (datetime): Hora e data de término da tarefa.
- `status` (string): Status atual da tarefa (por exemplo, "In Progress", "Done").
- `duration` (float): Duração total da tarefa em segundos.
- `subtasks` (list): Lista de subtarefas (`SubTask` objects) associadas à tarefa.

## Métodos Principais

### `start()`
Inicia a tarefa, registrando o horário de início e definindo o status como "In Progress".

### `add_subtask(subtask)`
Adiciona uma subtarefa à tarefa.
- `subtask` (dict): Dicionário representando a subtarefa a ser adicionada.

### `verify_status()`
Verifica e atualiza o status da tarefa com base no status das subtarefas.

### `end()`
Finaliza a tarefa, registrando o horário de término, calculando a duração e verificando o status final.

## Exemplo de Uso

```python
from workeranalyzer.analyzer import Task

# Criando uma nova tarefa
task = Task(task_name="Data Processing")
task.start()

# Adicionando subtarefas
subtask_data = {"name": "Load Data", "status": "In Progress", ...}
task.add_subtask(subtask_data)

# Finalizando a tarefa
task.end()
