# Storage - WorkerAnalyzer

## Visão Geral
A seção de "Storage" da biblioteca WorkerAnalyzer fornece funcionalidades para o armazenamento dos dados de monitoramento. Essas classes auxiliares permitem salvar as métricas e relatórios coletados de forma eficiente e segura.

## Classe LocalStorage

### Descrição
A classe `LocalStorage` é projetada para gerenciar o armazenamento de dados de sessões e métricas em um sistema de arquivos local.

### Funcionalidades
- **Salvar Dados:** Permite salvar dados de sessões ou métricas em arquivos locais.
- **Flexibilidade de Caminhos:** Aceita caminhos de diretórios personalizados para o armazenamento de arquivos.
- **Formatação de Arquivos:** Gera nomes de arquivos com base na data e hora atuais e no identificador dos dados.

### Uso
Ideal para cenários onde os dados de monitoramento devem ser armazenados localmente para análise posterior ou para fins de arquivamento.

## Exemplo de Uso

```python
from workeranalyzer.storage import LocalStorage

# Criando um objeto LocalStorage
storage = LocalStorage(path="/path/to/storage")

# Dados a serem salvos
session_data = {"id": "123", "start_time": "2021-01-01T00:00:00", ...}

# Salvando os dados no sistema de arquivos local
storage.save(session_data)
