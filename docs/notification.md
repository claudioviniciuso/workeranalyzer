# Classe SlackNotification - WorkerAnalyzer

## Objetivo e Uso
A classe `SlackNotification` é parte do pacote WorkerAnalyzer de comunicação rápida e eficiente de problemas ou resultados gerados. Ela deve ser usada para alertar erros graves ou notificar relatórios. 

## Propriedades
- `hook_url` (string): URL do Incoming Webhook Slack

## Métodos Principais

### `send(message)`
Envia notificação para o Slack com mensagem personalizada.

### `create_notification_report(data)`
Recebe como parâmetro `data`, dicionário emitido pela classe `DefaultReport`.
Cria notificação padrão para relatórios de resumo das tasks.

### `send_notification_report(data)`
Recebe como parâmetro `data`, dicionário emitido pela classe `DefaultReport`.
Envia a notificação padrão com informações do relatório.

## Exemplo de Uso

```python
from workeranalyzer.report import DefaultReport
from workeranalyzer.notification import SlackNotification

# Criando uma nova tarefa
slack = SlackNotification(hook_url)
slack.send("Hello world!")


# Gerando Report
report = DefaultReport(session)
data = report.generete_report()

# Adicionando subtarefas
slack.send_notification_report(data) 

