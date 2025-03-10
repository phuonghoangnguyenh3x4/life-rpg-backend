from workflow.SequentialWorkflow import SequentialWorkflow
from workflow.Task import Task
from utils.workflow_utils import get_sequential_workflow

class task1(Task):
    def execute(self, context):
        print("Task 1 executed.")
        context["task1_result"] = "task1_success"

class task2(Task):
    def execute(self, context):
        print("Task 2 executed.")
        context["task2_result"] = "task2_success"

class task3(Task):
    def execute(self, context):
        print("Task 3 executed.")
        context["task3_result"] = "task3_success"

class task4(Task):
    def execute(self, context):
        raise ValueError("Self error")

sequential_workflow = get_sequential_workflow(task1, task2, task3, task4)

context = {} # Shared context
sequential_workflow.execute(context)

print("Final context:", context)