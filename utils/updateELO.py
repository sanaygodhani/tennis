import numpy as np
from collections import defaultdict, deque
from utils.common import mean, getWinLose
def createStats():
    stats = {}
    stats["elo_players"] = defaultdict(int)
    stats["elo_surface_players"] = defaultdict(lambda:defaultdict(int))
    stats["elo_grad_players"] = defaultdict(lambda: deque(maxlen=1000))
    stats["last_k_matches"] = defaultdict(lambda: deque(maxlen=1000))
    stats["last_k_matches_stats"] = defaultdict(lambda:defaultdict(lambda:deque(maxlen=1000)))
    stats["matches_played"] =defaultdict(int)
    stats["h2h"] = defaultdict(int)
    stats["h2h_surface"] = defaultdict(lambda:defaultdict(int))

    return stats

def updateELO(match, stats):
    p1_id, p2_id, surface, result = match.p1_id, match.p2_id, match.surface, match.result
    winner_id, loser_id = getWinLose(p1_id, p2_id, result)

    winner_elo = stats["elo_players"].get("winner_id", 1500) #average elo is 1500
    loser_elo = stats["elo_players"].get("loser_id", 1500)
    winner_surface_elo = stats["elo_surface_players"][surface].get("winner_id", 1500)
    loser_surface_elo = stats["elo_surface_players"][surface].get("loser_id", 1500)

    k=32
    exp_winner = 1/(1+10**((loser_elo-winner_elo)/400))
    exp_loser = 1/(1+10**((winner_elo-loser_elo)/400))
    exp_surface_winner = 1/(1+10**((loser_surface_elo-winner_surface_elo)/400))
    exp_surface_loser = 1/(1+10**((winner_surface_elo-loser_surface_elo)/400))

    update_winner_elo += k*(1-exp_winner)
    update_loser_elo +=  k*(1-exp_loser)
    update_winner_surface_elo += k*(1-exp_surface_winner)
    update_loser_surface_elo += k*(1-exp_surface_loser)

    stats["elo_players"][winner_id] = update_winner_elo
    stats["elo_players"][loser_id] = update_loser_elo
    stats["elo_surface_players"][surface][winner_id] = update_winner_surface_elo
    stats["elo_surface_players"][surface][loser_id] = update_loser_surface_elo

    stats["elo_grad_players"][winner_id].append(update_winner_elo)
    stats["elo_grad_players"][loser_id].append(update_loser_elo)

    stats["matches_played"][winner_id] += 1
    stats["matches_played"][loser_id] += 1

    stats["last_k_matches"][winner_id].append(1)
    stats["last_k_matches"][loser_id].append(0)

    stats["h2h"][(winner_id, loser_id)]+=1
    stats["h2h_surface"][surface][(winner_id, loser_id)]+=1


    if p1_id==winner_id:
        w_ace, l_ace = match.p1_ace, match.p2_ace
        w_df, l_df = match.p1_df, match.p2_df
        w_svpt, l_svpt = match.p1_svpt, match.p2_svpt
        w_1stIn, l_1stIn = match.p1_1stIn, match.p2_1stIn
        w_1stWon, l_1stWon = match.p1_1stWon, match.p2_1stWon
        w_2ndWon, l_2ndWon = match.p1_2ndWon, match.p2_2ndWon
        w_bpSaved, l_bpSaved = match.p1_bpSaved, match.p2_bpSaved
        w_bpFaced, l_bpFaced = match.p1_bpFaced, match.p2_bpFaced
    else:
        w_ace, l_ace = match.p2_ace, match.p1_ace
        w_df, l_df = match.p2_df, match.p1_df
        w_svpt, l_svpt = match.p2_svpt, match.p1_svpt
        w_1stIn, l_1stIn = match.p2_1stIn, match.p1_1stIn
        w_1stWon, l_1stWon = match.p2_1stWon, match.p1_1stWon
        w_2ndWon, l_2ndWon = match.p2_2ndWon, match.p1_2ndWon
        w_bpSaved, l_bpSaved = match.p2_bpSaved, match.p1_bpSaved
        w_bpFaced, l_bpFaced = match.p2_bpFaced, match.p1_bpFaced

    if (w_svpt!=0) and (w_svpt!=w_1stIn):
        stats["last_k_matches_stats"][winner_id]["player_ace"].append(100*(w_ace/w_svpt))
        stats["last_k_matches_stats"][winner_id]["player_df"].append(100*(w_df/w_svpt))
        stats["last_k_matches_stats"][winner_id]["player_1stIn"].append(100*(w_1stIn/w_svpt))
        stats["last_k_matches_stats"][winner_id]["player_2ndWon"].append(100*(w_2ndWon/(w_svpt-w_1stIn)))
    if(l_svpt!=0) and (l_svpt!=l_1stIn):
        stats["last_k_matches_stats"][loser_id]["player_ace"].append(100*(l_ace/l_svpt))
        stats["last_k_matches_stats"][loser_id]["player_df"].append(100*(l_df/l_svpt))
        stats["last_k_matches_stats"][loser_id]["player_1stIn"].append(100*(l_1stIn/l_svpt))
        stats["last_k_matches_stats"][loser_id]["player_2ndWon"].append(100*(l_2ndWon/(l_svpt-l_1stIn)))

    if (w_1stIn!=0):
        stats["last_k_matches"][winner_id]["player_1stWon"].append(100(w_1stWon/w_1stIn))
    if (l_1stIn!=0):
        stats["last_k_matches"][loser_id]["player_1stWon"].append(100(l_1stWon/l_1stIn))

    if (w_bpFaced !=0):
        stats["last_k_matches"][winner_id]["player_bpSaved"].append(100(w_bpSaved/w_bpFaced))
    if (l_bpFaced!=0):
        stats["last_k_matches"][loser_id]["player_bpSaved"].append(100(l_bpSaved/l_bpFaced))

    return stats

# player object consists: id, atp_points, atp_rank, age, height, match

def getStats(player1, player2, match, stats):
    result = {}
    PLAYER1_ID = player1["ID"]
    PLAYER2_ID =player2["ID"]
    SURFACE = match["SURFACE"]

    result["BEST_OF "] = match["BEST_OF"]
    result["DRAW_SIZE"] = match["DRAW_SIZE"]
    result["AGE_diff"] = player1["AGE"] - player2["AGE"]
    result["HEIGHT_diff"] = player1["HEIGHT"] - player2["HEIGHT"]
    result["ATP_RANK_diff"] = player1["ATP_RANK"] - player2["ATP_RANK"]
    result["ATP_POINTS_diff"] = player1["ATP_POINTS"] - player2["ATP_POINTS"]

    elo_players = stats["elo_players"]
    elo_surface_players = stats["elo_surface_players"]
    elo_grad_players = stats["elo_grad_players"]
    last_k_matches = stats["last_k_matches"]
    last_k_matches_stats = stats["last_k_matches_stats"]
    matches_played = stats["matches_played"]
    h2h = stats["h2h"]
    h2h_surface = stats["h2h_surface"] 

    result["ELO_diff"] = elo_players[PLAYER1_ID] = elo_players[PLAYER2_ID]
    result["ELO_SURFACE_diff"] = elo_surface_players[PLAYER1_ID] - elo_surface_players[PLAYER2_ID]
    result["ELO_GRAD_diff"] = elo_grad_players[PLAYER1_ID] - elo_grad_players[PLAYER2_ID]
    result["# OF MATCHES_diff"] = matches_played[PLAYER1_ID] - matches_played[PLAYER2_ID]
    result["H2H_diff"] = h2h[(PLAYER1_ID, PLAYER2_ID)] - h2h[(PLAYER2_ID, PLAYER1_ID)]
    result["H2H_SURFACE_diff"] = h2h_surface[(PLAYER1_ID, PLAYER2_ID)] - h2h_surface[(PLAYER2_ID, PLAYER1_ID)]
    for k in [3, 5, 10, 25, 50, 100, 200]:
        if(len(last_k_matches[PLAYER1_ID])>=k) and (len(last_k_matches[PLAYER2_ID])>=k):
            result[f"LAST_{k}_WIN_diff"] = sum(list(last_k_matches[PLAYER1_ID])[-k:]) - sum(list(last_k_matches[PLAYER2_ID])[-k:])
        else:
            result[f"LAST_{k}_WIN_diff"] = 0

        if (len(last_k_matches[PLAYER1_ID])>=k) and (len(last_k_matches[PLAYER2_ID])>=k):
            player1_slope = np.polyfit(np.arange(len(list(last_k_matches[PLAYER1_ID])[-k:])), np.array(list(last_k_matches[PLAYER1_ID])[-k:]), 1)[0]
            player2_slope = np.polyfit(np.arange(len(list(last_k_matches[PLAYER2_ID])[-k:])), np.array(list(last_k_matches[PLAYER2_ID])[-k:]), 1)[0]
            result[f"LAST_{k}_GRAD_diff"] = player1_slope-player2_slope
        else:
            result[f"LAST_{k}_GRAD_diff"] = 0

        result[f"LAST_{k}_ACE_diff"] = mean(list(last_k_matches_stats[PLAYER1_ID]["player_ace"])[-k:]) - mean(list(last_k_matches_stats[PLAYER2_ID]["player_ace"])[-k:])
        result[f"LAST_{k}_DF_diff"] = mean(list(last_k_matches_stats[PLAYER1_ID]["player_df"])[-k:]) - mean(list(last_k_matches_stats[PLAYER2_ID]["player_df"])[-k:])
        result[f"LAST_{k}_1STIN_diff"] = mean(list(last_k_matches_stats[PLAYER1_ID]["player_1stIn"])[-k:]) - mean(list(last_k_matches_stats[PLAYER2_ID]["player_1stIn"])[-k:])
        result[f"LAST_{k}_1STWON_diff"] = mean(list(last_k_matches_stats[PLAYER1_ID]["player_1stWon"])[-k:]) - mean(list(last_k_matches_stats[PLAYER2_ID]["player_1stWon"])[-k:])
        result[f"LAST_{k}_2NDWON_diff"] = mean(list(last_k_matches_stats[PLAYER1_ID]["player_2ndWon"])[-k:]) - mean(list(last_k_matches_stats[PLAYER2_ID]["player_2ndWon"])[-k:])
        result[f"LAST_{k}_BPSAVED_diff"] = mean(list(last_k_matches_stats[PLAYER1_ID]["player_bpSaved"])[-k:]) - mean(list(last_k_matches_stats[PLAYER2_ID]["player_bpSaved"])[-k:])

    return result


    