from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, name, hp, attack, defense, level=1):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, amount):
        dmg = max(0, amount - self.defense)
        self.current_hp = max(0, self.current_hp - dmg)
        return dmg

    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    @abstractmethod
    def choose_action(self, battle):
        pass

class PlayerCharacterObj(Character):
    def __init__(self, name, hp, attack, defense, level=1):
        super().__init__(name, hp, attack, defense, level)

    def choose_action(self, battle):
        raise NotImplementedError('Player actions are provided by client')

class EnemyCharacter(Character):
    def __init__(self, name, hp, attack, defense, level=1, ai_strategy=None):
        super().__init__(name, hp, attack, defense, level)
        self.ai_strategy = ai_strategy

    def choose_action(self, battle):
        return self.ai_strategy.select_action(self, battle)
