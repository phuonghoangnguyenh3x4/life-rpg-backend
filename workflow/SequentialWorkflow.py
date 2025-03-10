from workflow.Workflow import Workflow

class SequentialWorkflow(Workflow):
    def execute(self, context):
        for workflow in self.workflow_queue:
            try:
                workflow.execute(context)
            except Exception as e:
                print(f"Workflow execution failed: {e}")
                #Potentially add error handling, logging, or break the loop.
                #You might want to store the error in the context.
                return #or raise the exception.