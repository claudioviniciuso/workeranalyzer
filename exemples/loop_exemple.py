from worker_analyzer.analyzer import Session, Task, SubTask
from worker_analyzer.builders import DefaultMetricsBuilder
from worker_analyzer.storage import LocalStorage
from worker_analyzer.report import DefaultReport
import random


tasks_list = ["Bar", "Foo", "Baz"]
subtask_by_task = {
    "Bar": ["TaskBar A", "TaskBar B"],
    "Foo": ["TaskFoo B", "TaskFoo B"],
    "Baz": ["TaskBaz A", "TaskBaz A"]
}

session = Session()
session.start()
session.add_attribute("user", "user1")
session.add_attribute("env", "teste")
session.add_attribute("version", "1.0.0")

for task_n in tasks_list:
    task = Task(task_n)
    task.start()
    print(task_n)

    for subtask_n in subtask_by_task[task_n]:
        subtask = SubTask(subtask_n,subtask_type="Task Type")
        subtask.start()
        
        # Simulação de uma Páginação de um Request
        # Para cada Endpoint pode ter de 1 a 10 páginas e elas são monitaradas pelo Metrics
        metrics = DefaultMetricsBuilder("Metrics for subtask {}".format(subtask_n))
        metrics.start()
        for request_n in range(random.randint(1, 10)):
            print(request_n)
    
            if random.randint(0, 10) in (2,5,7):
                status = "failure"
                error = "Error {}".format(random.randint(1, 10))
                metrics.log(status=status, error_content=error)
            else:
                status = "success"
                metrics.log(status=status)
        
        metrics.end()
        subtask.add_metrics(metrics.metrics)
        subtask.end("success")

        task.add_subtask(subtask.subtask)
    task.end()
    session.add_task(task.task)

session.end()

storage = LocalStorage(path=".")
storage.save(session.session)

report = DefaultReport(session.session)
print(report.generate_report())
print(session.session)


