from typing import Type, TypeVar, List
from workflow.TaskWorkflow import TaskWorkflow
from workflow.SequentialWorkflow import SequentialWorkflow
from workflow.Task import Task  

T = TypeVar('T', bound=Task)  # T must be a subclass of Task

def get_sequential_workflow(*arg: Type[T]) -> SequentialWorkflow:
    """
    Parameters
    ----------
    *arg : Task class
    """
    workflow_queue = get_workflow_queue(*arg)
    return SequentialWorkflow(workflow_queue)

def get_workflow_queue(*arg: Type[T]) -> List[TaskWorkflow]:
    """
    Parameters
    ----------
    *arg : Task class
    """
    return [get_task_workflow(task_class) for task_class in arg]

def get_task_workflow(task_class: Type[T]) -> TaskWorkflow:
    """
    Parameters
    ----------
    task_class : Task class
    """
    return TaskWorkflow(task_class())