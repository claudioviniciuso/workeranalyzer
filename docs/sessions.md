# Classe Session - WorkerAnalyzer

## Objetivo e Uso
A classe `Session` é um componente central da biblioteca WorkerAnalyzer, responsável por gerenciar uma sessão de execução de processo ou pipeline de dados. Ela fornece funcionalidades para iniciar, monitorar e concluir uma sessão, armazenando informações sobre todas as `Tasks` e `SubTasks` associadas.

## Propriedades
- `id` (string): Um identificador único para a sessão.
- `start_time` (datetime): A hora e data de início da sessão.
- `end_time` (datetime): A hora e data de término da sessão.
- `duration` (float): Duração total da sessão em segundos.
- `status` (string): Status atual da sessão (por exemplo, "Running", "Done").
- `custom_attributes` (dict): Atributos personalizados adicionados à sessão.
- `tasks` (list): Lista de tarefas (`Task` objects) associadas à sessão.

## Métodos Principais

### `start()`
Inicia a sessão, registrando o horário de início e definindo o status como "Running".

### `add_attribute(key, value)`
Adiciona um atributo personalizado à sessão.
- `key` (string): Nome do atributo.
- `value`: Valor do atributo.

### `add_task(task)`
Adiciona uma tarefa à sessão.
- `task` (dict): Dicionário representando a tarefa a ser adicionada.

### `end(status="Done")`
Finaliza a sessão, registrando o horário de término e calculando a duração.
- `status` (string): Status final da sessão.

## Exemplo de Uso

```python
from workeranalyzer.analyzer import Session

# Criando uma nova sessão
session = Session()
session.start()

# Adicionando atributos personalizados
session.add_attribute("env", "production")
session.add_attribute("description", "Daily data processing")

# Adicionando tarefas
task_data = {"name": "Data Extraction", "status": "In Progress", ...}
session.add_task(task_data)

# Finalizando a sessão
session.end("Done")
