from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db, PlayerCharacter as PlayerCharacterModel, MatchResult
from .game.character import PlayerCharacterObj, EnemyCharacter
from .game.battle import Battle
from .game.actions import AttackAction, DefendAction, HealAction
from .game.ai_engine import HeuristicAI
from .game_routes_leaderboard import compute_leaderboard
import time

game_bp = Blueprint('game', __name__)

# In-memory store for battles
ongoing_battles = {}

# -----------------------------
# HOME PAGE
# -----------------------------
@game_bp.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# LOBBY PAGE
# -----------------------------
@game_bp.route("/lobby")
@login_required
def lobby():
    pc = PlayerCharacterModel.query.filter_by(owner_id=current_user.id).first()
    return render_template("lobby.html", pc=pc)

# -----------------------------
# LEADERBOARD PAGE
# -----------------------------
@game_bp.route("/leaderboard")
@login_required
def leaderboard():
    board = compute_leaderboard()
    return render_template("leaderboard.html", board=board)

# -----------------------------
# START NEW BATTLE (WITH ENEMY SELECTION)
# -----------------------------
@game_bp.route("/battle/start")
@login_required
def battle_start():
    enemy_type = request.args.get("enemy", "goblin")

    enemies = {
        "goblin": {"name": "Goblin", "hp": 30, "attack": 6, "defense": 1, "xp": 10},
        "orc": {"name": "Orc", "hp": 50, "attack": 8, "defense": 3, "xp": 20},
        "dragon": {"name": "Dragon", "hp": 120, "attack": 15, "defense": 6, "xp": 50}
    }

    selected = enemies.get(enemy_type, enemies["goblin"])

    pc = PlayerCharacterModel.query.filter_by(owner_id=current_user.id).first()
    if not pc:
        flash("Create a character first.", "danger")
        return redirect(url_for("game.lobby"))

    player_obj = PlayerCharacterObj(pc.name, pc.max_hp, pc.attack, pc.defense, level=pc.level)
    enemy_obj = EnemyCharacter(selected["name"], selected["hp"], selected["attack"], selected["defense"], level=1, ai_strategy=HeuristicAI())

    battle = Battle(player_obj, enemy_obj)
    battle_id = f"{current_user.id}-{pc.id}-{int(time.time())}"
    ongoing_battles[battle_id] = battle

    return redirect(url_for("game.battle_screen", battle_id=battle_id))

# -----------------------------
# BATTLE SCREEN
# -----------------------------
@game_bp.route("/battle/<battle_id>")
@login_required
def battle_screen(battle_id):
    battle = ongoing_battles.get(battle_id)
    if not battle:
        flash("Battle not found.", "danger")
        return redirect(url_for("game.lobby"))
    return render_template("battle.html", battle=battle, battle_id=battle_id)

# -----------------------------
# AJAX BATTLE ACTION
# -----------------------------
@game_bp.route("/battle/<battle_id>/action", methods=["POST"])
@login_required
def battle_action(battle_id):
    battle = ongoing_battles.get(battle_id)
    if not battle:
        return jsonify({"error": "battle not found"}), 404

    if battle.is_over():
        return jsonify({"error": "battle finished", "winner": battle.winner()}), 400

    if battle.turn != "player":
        return jsonify({"error": "not your turn"}), 400

    data = request.get_json() or {}
    move = data.get("move")

    # ---------------- PLAYER ACTION ----------------
    if move == "attack":
        battle.perform_action("player", AttackAction())
    elif move == "defend":
        battle.perform_action("player", DefendAction())
    elif move == "heal":
        battle.perform_action("player", HealAction())
    else:
        return jsonify({"error": "invalid move"}), 400

    # ---------------- ENEMY ACTION ----------------
    if not battle.is_over():
        ai_action = battle.enemy.choose_action(battle)
        battle.perform_action("enemy", ai_action)

    # ---------------- PERSIST RESULTS ----------------
    xp_gained = 0
    level_up = False
    new_level = None

    if battle.is_over():
        winner = battle.winner()
        xp_gained = 20 if winner == "player" else 5
        mr = MatchResult(
            player_id=current_user.id,
            enemy_type=battle.enemy.name,
            result='win' if winner == 'player' else 'loss',
            xp_gained=xp_gained
        )
        db.session.add(mr)

        # Level-up logic
        pc = PlayerCharacterModel.query.filter_by(owner_id=current_user.id).first()
        if winner == "player":
            pc.xp += xp_gained
            while pc.xp >= pc.level * 50:
                pc.xp -= pc.level * 50
                pc.level += 1
                pc.max_hp += 5
                pc.attack += 1
                pc.defense += 1
                pc.current_hp = pc.max_hp
                level_up = True
                new_level = pc.level
        db.session.commit()

    # ---------------- FORMAT LOG FOR FRONT-END ----------------
    return jsonify({
        "log": battle.log[-6:],
        "player_hp": battle.player.current_hp,
        "enemy_hp": battle.enemy.current_hp,
        "is_over": battle.is_over(),
        "winner": battle.winner(),
        "player_name": battle.player.name,
        "xp_gained": xp_gained,
        "level_up": level_up,
        "new_level": new_level
    })

# -----------------------------
# CHARACTER PAGE
# -----------------------------
@game_bp.route("/character")
@login_required
def character():
    pc = PlayerCharacterModel.query.filter_by(owner_id=current_user.id).first()
    return render_template("character.html", pc=pc)

# -----------------------------
# ARENA PAGE
# -----------------------------
@game_bp.route("/arena")
@login_required
def arena():
    return render_template("arena.html")
