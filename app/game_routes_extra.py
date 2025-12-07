from flask import Blueprint, render_template
from .game_routes_leaderboard import compute_leaderboard

extra_bp = Blueprint('extra', __name__)

@extra_bp.route('/leaderboard')
def leaderboard():
    board = compute_leaderboard()
    return render_template('leaderboard.html', board=board)
