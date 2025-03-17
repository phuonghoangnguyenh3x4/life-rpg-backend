from utils.workflow_utils import get_sequential_workflow
from workflow.AddQuestWorkflow.CreateQuestTask import CreateQuestTask
from workflow.AddQuestWorkflow.UpdatePlayerStatTask import UpdatePlayerStatTask
from workflow.AddQuestWorkflow.UpdateHeatmapTask import UpdateHeatmapTask

AddQuestWorkflow = get_sequential_workflow(
    CreateQuestTask,
    UpdatePlayerStatTask,
    UpdateHeatmapTask
)