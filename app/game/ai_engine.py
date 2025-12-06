import random
from .actions import AttackAction, DefendAction

class BaseAI:
    def select_action(self, enemy, battle):
        raise NotImplementedError

class RandomAI(BaseAI):
    def select_action(self, enemy, battle):
        if random.random() < 0.8:
            return AttackAction()
        return DefendAction()

class HeuristicAI(BaseAI):
    def select_action(self, enemy, battle):
        # If low HP, sometimes defend
        if enemy.current_hp < enemy.max_hp * 0.3 and random.random() < 0.6:
            return DefendAction()
        # Prefer attacking
        return AttackAction()
