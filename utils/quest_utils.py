from utils.randint import randint
from enums.quest_status import QuestStatus

difficulty_exp_map = {
    "Trivial": (1, 20),
    "Easy": (20, 100),
    "Normal": (100, 200),
    "Hard": (200, 300),
    "SuperHard": (450, 550)   
}

def get_exp_from_difficulty(difficulty, seed):
    return randint.get(seed, difficulty_exp_map[difficulty])

def get_money_from_difficulty(difficulty, seed):
    return randint.get(seed + 1, difficulty_exp_map[difficulty])*2

def isQuestMadeDone(old_status, new_status):
    return old_status != QuestStatus.Done and new_status == QuestStatus.Done

def isQuestMadeUndone(old_status, new_status):
    return old_status == QuestStatus.Done and new_status != QuestStatus.Done