from app.game.character import PlayerCharacterObj, EnemyCharacter
from app.game.battle import Battle
from app.game.actions import AttackAction

def test_attack_reduces_hp():
    p = PlayerCharacterObj('Hero', 50, 10, 2)
    e = EnemyCharacter('Goblin', 30, 5, 1, ai_strategy=None)
    b = Battle(p, e)
    b.perform_action('player', AttackAction())
    assert e.current_hp < e.max_hp
