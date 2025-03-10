from abc import ABC, abstractmethod
from typing import List, TypeVar, Union
from workflow.Task import Task

TWorkflow = TypeVar('TWorkflow', bound='Workflow')

class Workflow(ABC):
    def __init__(self, workflow_queue: Union[List[TWorkflow], None] = None):
        if workflow_queue is None:
            self.workflow_queue: List[TWorkflow] = []
        else:
            self.workflow_queue = workflow_queue

    @abstractmethod
    def execute(self, context):
        pass

    def add_workflow(self, workflow: TWorkflow):
        if isinstance(workflow, Workflow):
            self.workflow_queue.append(workflow)
        else:
            raise TypeError("Added workflow must be an instance of Workflow or its subclasses.")

