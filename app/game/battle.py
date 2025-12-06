from .actions import AttackAction, DefendAction

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 'player'
        self.log = []

    def perform_action(self, actor_side, action):
        actor = self.player if actor_side == 'player' else self.enemy
        target = self.enemy if actor is self.player else self.player

        result = action.execute(actor, target, self)
        self.log.append(result)

        # remove any temp defend after they've been used (if target has _temp_defend)
        # Here we only remove when a character takes damage (handled in take_damage)
        # switch turn
        self.turn = 'enemy' if self.turn == 'player' else 'player'
        return result

    def is_over(self):
        return not self.player.is_alive() or not self.enemy.is_alive()

    def winner(self):
        if self.player.is_alive() and not self.enemy.is_alive():
            return 'player'
        if self.enemy.is_alive() and not self.player.is_alive():
            return 'enemy'
        return None
