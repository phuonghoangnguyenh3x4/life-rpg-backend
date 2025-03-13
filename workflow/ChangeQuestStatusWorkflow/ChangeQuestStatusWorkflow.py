from workflow.ChangeQuestStatusWorkflow.ChangeQuestStatusTask import ChangeQuestStatusTask 
from workflow.ChangeQuestStatusWorkflow.GetQuestTask import GetQuestTask 
from workflow.ChangeQuestStatusWorkflow.GetOldStatusTask import GetOldStatusTask 
from workflow.ChangeQuestStatusWorkflow.UpdatePlayerStatTask import UpdatePlayerStatTask 
from workflow.ChangeQuestStatusWorkflow.UpdateQuestDoneDate import UpdateQuestDoneDate 
from workflow.ChangeQuestStatusWorkflow.UpdateHeatmap import UpdateHeatmap 
from utils.workflow_utils import get_sequential_workflow

ChangeQuestStatusWorkflow = get_sequential_workflow(
    GetQuestTask, 
    GetOldStatusTask, 
    ChangeQuestStatusTask,
    UpdatePlayerStatTask,
    UpdateQuestDoneDate,
    UpdateHeatmap
)