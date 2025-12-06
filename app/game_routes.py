from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask import render_template
from flask_login import login_required, current_user
from .models import db, PlayerCharacter as PlayerCharacterModel, MatchResult
from .game.character import PlayerCharacterObj, EnemyCharacter
from .game.battle import Battle
from .game.actions import AttackAction, DefendAction
from .game.ai_engine import HeuristicAI
import time

game_bp = Blueprint('game', __name__)

# simple in-memory battle store for demo purposes
ongoing_battles = {}

@game_bp.route("/")
def home():
    return render_template("index.html")

@game_bp.route('/lobby')
@login_required
def lobby():
    # show user's character and actions
    pc = PlayerCharacterModel.query.filter_by(owner_id=current_user.id).first()
    return render_template('lobby.html', pc=pc)

@game_bp.route('/start_battle', methods=['POST'])
@login_required
def start_battle():
    pc = PlayerCharacterModel.query.filter_by(owner_id=current_user.id).first()
    if not pc:
        flash('Create a character first.', 'danger')
        return redirect(url_for('game.lobby'))
    player_obj = PlayerCharacterObj(pc.name, pc.max_hp, pc.attack, pc.defense, level=pc.level)
    enemy_obj = EnemyCharacter('Goblin', 30, 6, 1, level=1, ai_strategy=HeuristicAI())
    battle = Battle(player_obj, enemy_obj)
    battle_id = f"{current_user.id}-{pc.id}-{int(time.time())}"
    ongoing_battles[battle_id] = battle
    return redirect(url_for('game.battle_screen', battle_id=battle_id))

@game_bp.route('/battle/<battle_id>')
@login_required
def battle_screen(battle_id):
    battle = ongoing_battles.get(battle_id)
    if not battle:
        flash('Battle not found.', 'danger')
        return redirect(url_for('game.lobby'))
    return render_template('battle.html', battle=battle, battle_id=battle_id)

@game_bp.route('/battle/<battle_id>/action', methods=['POST'])
@login_required
def battle_action(battle_id):
    battle = ongoing_battles.get(battle_id)
    if not battle:
        return jsonify({'error':'battle not found'}), 404
    if battle.is_over():
        return jsonify({'error':'battle finished', 'winner': battle.winner()}), 400
    if battle.turn != 'player':
        return jsonify({'error':'not your turn'}), 400

    data = request.get_json() or {}
    move = data.get('move')
    if move == 'attack':
        res = battle.perform_action('player', AttackAction())
    elif move == 'defend':
        res = battle.perform_action('player', DefendAction())
    else:
        return jsonify({'error':'invalid move'}), 400

    # enemy turn if not over
    if not battle.is_over():
        ai_action = battle.enemy.choose_action(battle)
        aires = battle.perform_action('enemy', ai_action)

    # persist result if finished
    if battle.is_over():
        winner = battle.winner()
        mr = MatchResult(player_id=current_user.id,
                         enemy_type=battle.enemy.name,
                         result='win' if winner=='player' else 'loss',
                         xp_gained=20 if winner=='player' else 5)
        db.session.add(mr)
        db.session.commit()

    return jsonify({
        'log': battle.log[-6:],
        'player_hp': battle.player.current_hp,
        'enemy_hp': battle.enemy.current_hp,
        'is_over': battle.is_over(),
        'winner': battle.winner()
    })
