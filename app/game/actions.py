from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self, actor, target, battle):
        pass

class AttackAction:
    def execute(self, attacker, defender, battle):
        dmg = max(1, attacker.attack - defender.defense)
        defender.current_hp -= dmg
        return {
            "actor": attacker.name,
            "type": "attack",
            "value": dmg,
            "text": f"{attacker.name} deals {dmg} damage to {defender.name}!"
        }

class DefendAction:
    def execute(self, attacker, defender, battle):
        attacker.temp_defense += 3
        return {
            "actor": attacker.name,
            "type": "defend",
            "value": 0,
            "text": f"{attacker.name} braces for impact (+3 defense next hit)"
        }

class HealAction:
    def __init__(self, heal_amount=10):
        self.heal_amount = heal_amount

    def execute(self, attacker, defender, battle):
        heal = min(self.heal_amount, attacker.max_hp - attacker.current_hp)
        attacker.current_hp += heal
        return {
            "actor": attacker.name,
            "type": "heal",
            "value": heal,
            "text": f"{attacker.name} heals for {heal} HP!"
        }

