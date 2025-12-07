from .models import db, MatchResult, User
from flask import render_template

def compute_leaderboard():
    users = User.query.all()
    board = []
    for u in users:
        wins = MatchResult.query.filter_by(player_id=u.id, result='win').count()
        losses = MatchResult.query.filter_by(player_id=u.id, result='loss').count()
        board.append({'username': u.username, 'wins': wins, 'losses': losses})
    return board

