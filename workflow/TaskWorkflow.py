from workflow.Workflow import Workflow
from workflow.Task import Task

class TaskWorkflow(Workflow): 
    def __init__(self, task: Task):
        self.task = task
    
    def execute(self, context):
        try:
            print(f"Executing task: {self.task.name}")
            self.task.execute(context)
        except Exception as e:
            print(f"Task {self.task.name} failed: {e}")
            raise   
