from utils.workflow_utils import get_sequential_workflow
from workflow.DeleteQuestWorkflow.GetQuestTask import GetQuestTask 
from workflow.DeleteQuestWorkflow.UpdatePlayerStatTask import UpdatePlayerStatTask 
from workflow.DeleteQuestWorkflow.UpdateHeatmapTask import UpdateHeatmapTask 
from workflow.DeleteQuestWorkflow.DeleteQuestTask import DeleteQuestTask 

DeleteQuestWorkflow = get_sequential_workflow(
    GetQuestTask,
    UpdatePlayerStatTask,
    UpdateHeatmapTask,
    DeleteQuestTask
)