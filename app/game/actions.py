from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self, actor, target, battle):
        pass

class AttackAction(Action):
    def execute(self, actor, target, battle):
        damage = actor.attack
        dealt = target.take_damage(damage)
        return {'type': 'attack', 'actor': actor.name, 'target': target.name, 'damage': dealt}

class DefendAction(Action):
    def execute(self, actor, target, battle):
        # temporary defense buff: add 2 to defense for one enemy attack
        actor.defense += 2
        # mark buff so it can be removed after next hit
        if not hasattr(actor, '_temp_defend'):
            actor._temp_defend = 0
        actor._temp_defend += 2
        return {'type': 'defend', 'actor': actor.name}
