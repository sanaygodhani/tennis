import numpy as np
from collections import defaultdict, deque
from utils.common import mean, getWinLose
def createStats():
    prev_stats = {}
    prev_stats["elo_players"] = defaultdict(int)
    prev_stats["elo_surface_players"] = defaultdict(lambda:defaultdict(int))
    prev_stats["elo_grad_players"] = defaultdict(lambda: deque(maxlen=1000))
    prev_stats["last_k_matches"] = defaultdict(lambda: deque(maxlen=1000))
    prev_stats["last_k_matches_stats"] = defaultdict(lambda:defaultdict(lambda:deque(maxlen=1000)))
    prev_stats["matches_played"] =defaultdict(int)
    prev_stats["h2h"] = defaultdict(int)
    prev_stats["h2h_on_surface"] = defaultdict(lambda:defaultdict(int))

    return prev_stats

def updateELO(match, prev_stats):
    p1_id, p2_id, surface, result = match.p1_id, match.p2_id, match.surface, match.result
    winner_id, loser_id = getWinLose(p1_id, p2_id, result)

    winner_elo = prev_stats["elo_players"].get("winner_id", 1500) #average elo is 1500
    loser_elo = prev_stats["elo_players"].get("loser_id", 1500)
    winner_surface_elo = prev_stats["elo_surface_players"][surface].get("winner_id", 1500)
    loser_surface_elo = prev_stats["elo_surface_players"][surface].get("loser_id", 1500)

    k=24
    exp_winner = 1/(1+10**((loser_elo-winner_elo)/400))




