import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
pd.set_option('display.max_columns', None)
from utils.updateELO import createStats, updateELO, getStats
cleaned_data = pd.read_csv("./data/clean_dataset.csv")

stats = createStats()
final_dataset = []

for i, row in tqdm(cleaned_data.iterrows(), total = len(cleaned_data)):
    player1 = {
        "ID" : row["p1_id"],
        "ATP_RANK":row["p1_rank"],
        "ATP_POINTS":row["p1_rank_points"],
        "AGE":row["p1_age"],
        "HEIGHT":row["p1_ht"],
    }
    player2 = {
        "ID" : row["p2_id"],
        "ATP_RANK":row["p2_rank"],
        "ATP_POINTS":row["p2_rank_points"],
        "AGE":row["p2_age"],
        "HEIGHT":row["p2_ht"],
    }
    match = {
        "BEST_OF":row["best_of"],
        "DRAW_SIZE":row["draw_size"],
        "SURFACE": row["surface"],
    }

    result = getStats(player1, player2, match, stats)
    match_data = dict(sorted(result.items()))
    match_data["RESULT"] = row["result"]

    final_dataset.append(match_data)

    stats = updateELO(row, stats)

final_dataset = pd.DataFrame(final_dataset)
print(final_dataset.head())