import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
pd.set_option('display.max_columns', None)

df = pd.read_csv("./data/singles_match_data/atp_matches_2024.csv")

# print(df.info())

match_data = pd.read_csv("./data/singles_match_data/atp_matches_2002.csv")
for i in range(2003, 2025):
    file = "./data/singles_match_data/atp_matches_"+ str(i)+ ".csv"
    curr = pd.read_csv(file)
    match_data = pd.concat([match_data, curr], axis=0)

# print(len(match_data))

# id, height, age, ace, double faults, service points, # of 1st serves, # of 1st serve Won,
#  # of 2nd serve Won, # of serve game, # of break points faced, break points saved

match_data_filter = match_data.dropna(subset=[
    'winner_id', 'loser_id', 'winner_ht', 'loser_ht', 'winner_age', 'loser_age', 'w_ace', 'l_ace', 'w_df', 
    'l_df', 'w_svpt', 'l_svpt', 'w_1stIn', 'l_1stIn', 'w_1stWon', 'l_1stWon', 'w_2ndWon', 'l_2ndWon', 'w_SvGms', 
    'l_SvGms', 'w_bpFaced', 'l_bpFaced', 'w_bpSaved', 'l_bpSaved', 'winner_rank_points', 'loser_rank_points', 
    'winner_rank', 'loser_rank'
]).reset_index(drop=True)


# for model training remapping winner and losers as p1 and p2

winner_column_names= [
    "winner_id","winner_seed", "winner_entry", "winner_name", "winner_hand", "winner_ht", "winner_ioc", "winner_age", 
    "w_ace", "w_df", "w_svpt", "w_1stIn", "w_1stWon", "w_2ndWon", "w_SvGms", "w_bpSaved", "w_bpFaced", "winner_rank",
    "winner_rank_points"
]
loser_column_names = [
    "loser_id","loser_seed", "loser_entry", "loser_name", "loser_hand", "loser_ht", "loser_ioc", "loser_age", "l_ace", 
    "l_df", "l_svpt", "l_1stIn", "l_1stWon", "l_2ndWon", "l_SvGms", "l_bpSaved", "l_bpFaced", "loser_rank",
    "loser_rank_points"
]

remap_dict = {col:col.replace("winner", "p1").replace("w_", "p1_") for col in winner_column_names}
remap_dict.update({col:col.replace("loser", "p2").replace("l_", "p2_") for col in loser_column_names})

match_data_filter = match_data_filter.rename(columns=remap_dict)

# interchanging p1 and p2 between the winners and losers

p1_columns = [col for col in match_data_filter if "p1" in col or "p1_" in col]
p2_columns = [col for col in match_data_filter if "p2" in col or "p2_" in col]

boolean_mask = np.random.rand(len(match_data_filter)) < 0.5

match_data_filter["result"] = np.where(boolean_mask, 0, 1)
match_data_filter.loc[boolean_mask, p1_columns], match_data_filter.loc[boolean_mask, p2_columns] = match_data_filter.loc[boolean_mask, p2_columns].values, match_data_filter.loc[boolean_mask, p1_columns].values

match_data_filter.to_csv("./data/clean_dataset.csv", index=False)
# print(match_data_filter)

