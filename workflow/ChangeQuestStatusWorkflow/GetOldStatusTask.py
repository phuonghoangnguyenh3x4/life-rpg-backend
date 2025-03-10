from workflow.Task import Task

class GetOldStatusTask(Task):     
    def execute(self, context):
        quest = context['quest']
        old_status = quest['status']
        context['old_status'] = old_status