import pandas as pd
import numpy as np

#======= Owners ====================
owner_df = pd.read_csv("data/files/teams_2023 (1).csv")
py_owner_df = pd.read_csv("data/files/teams_2022.csv")
owner_name_list = owner_df["manager_name"].tolist()

#======= Transactions ==============
transactions_df = pd.read_csv("data/files/transactions_2023.csv")

#======= Draft Results =============
draft_results_df = pd.read_csv("data/files/draft_results_2023.csv")
py_draft_results_df = pd.read_csv("data/files/draft_results_2022.csv")
draft_keepers_df = pd.read_csv('data/files/draft_keepers_2023.csv')
draft_results_df = draft_results_df.merge(draft_keepers_df,how='left',on='player_key')
draft_results_df = draft_results_df.rename(columns={'team_key_x':'team_key','keeper_flag':'kept_prev_year'})
draft_results_df = draft_results_df.drop(columns=['team_key_y','manager_name','player_name'])

#======= Player Data ===============
players_df = pd.read_csv("data/files/players_2023 (1).csv")
py_players_df = pd.read_csv("data/files/players_2022.csv")

def filter_df(df,col,val):
    df = df.loc[df[col] == val]
    return df

def df_cols(df,cols):
    df = df[cols]
    return df

def df_rename_cols(df,col_dict):
    df = df.rename(columns=col_dict)
    return df

def merge_df(df1, df2, lkey, rkey, how="left"):
    merged_df = df1.merge(df2,how=how,left_on=lkey,right_on=rkey)
    return merged_df

def keeper_eligible(row):
    if row['round'] <= 2 or row['dropped'] == True or row['dropped_after_trade'] == 'drop' or row['kept_prev_year'] == 1:
        return 'ineligible'
    else:
        return 'eligible'

def keeper_round(row):
    if row['keeper'] == 'eligible':
        return round(row['round'] - 2,0)

def owner_keepers(df,owner_name):
    df = filter_df(df,'keeper_owner',owner_name)
    df = df_cols(df,['round','pick','player_name','team','position','keeper','keeper_round','dropped','kept_prev_year','dropped_after_trade'])
    df = df_rename_cols(df,{'round':'Round','pick':'Pick','player_name':'Player','team':'Team','position':'Position',
                           'keeper':'Keeper','keeper_round':'Keeper Round'})
    return df

#======= Dropped Players ===========
col_filter = 'transaction_type'
val_filter = 'drop'
col_rename_dict = {0:'dropped_player_key'}
dropped = filter_df(transactions_df,col_filter,val_filter)
dropped = df_rename_cols(pd.DataFrame(dropped.player_key.unique()),col_rename_dict)

#======= Traded Players ============
col_filter = 'transaction_type'
val_filter = 'trade'

cols_1 = ['player_key','destination_team_key']
cols_2 = ["player_key","destination_team_key_x","transaction_type"]
cols_3 = ['traded_player_key','traded_to_team_key','dropped_after_trade','manager_name']

rename_1 = {"player_key":"traded_player_key","destination_team_key_x":"traded_to_team_key","transaction_type":"dropped_after_trade"}
rename_2 = {'manager_name':'traded_to_manager_name'}

traded = filter_df(transactions_df,col_filter,val_filter)
traded = df_cols(traded,cols_1)
traded = merge_df(traded,transactions_df,["player_key","destination_team_key"],["player_key","source_team_key"])
traded = df_cols(traded,cols_2)
traded = df_rename_cols(traded,rename_1)
traded = merge_df(traded,owner_df,'traded_to_team_key','team_key')
traded = df_cols(traded,cols_3)
traded = df_rename_cols(traded,rename_2)

""" #======= Kept Previous Year ========
ly_draft = draft_results_df.merge(owner_df,on='team_key')
ly_draft = ly_draft.merge(players_df,on='player_key')
py_draft = py_draft_results_df.merge(py_owner_df,on='team_key')
py_draft = py_draft.merge(py_players_df,on='player_key')
kept_py = ly_draft.merge(py_draft,on=['manager_name','player_id'])
kept_py = kept_py[kept_py['round_x'] == kept_py['round_y'] - 2]
kept_py = kept_py[['team_key_x','player_key_x']]
kept_py = kept_py.rename(columns={'team_key_x': 'team_key', 'player_key_x': 'player_key'})
kept_py['kept_prev_year'] = 1 """

#======= Keeper Eligibility ========
keeper_eval = merge_df(draft_results_df,owner_df,'team_key','team_key')
keeper_eval = merge_df(keeper_eval,players_df,"player_key",'player_key')
keeper_eval = merge_df(keeper_eval,dropped,'player_key','dropped_player_key')
keeper_eval = merge_df(keeper_eval,traded,'player_key','traded_player_key')
#keeper_eval = keeper_eval.merge(kept_py, how="left", on=['team_key','player_key'])

#col_list = ['round','pick','player_key','manager_name','team_key','player_name','team','position','dropped_player_key','traded_player_key','traded_to_manager_name','dropped_after_trade','kept_prev_year']
#keeper_eval = df_cols(keeper_eval,col_list)

#calculated columns
keeper_eval['dropped'] = keeper_eval['dropped_player_key'].isnull() == False
keeper_eval['keeper_owner'] = keeper_eval.traded_to_manager_name.combine_first(keeper_eval.manager_name)
keeper_eval['keeper'] = keeper_eval.apply(keeper_eligible, axis=1) 
keeper_eval['keeper_round'] = keeper_eval.apply(keeper_round, axis=1)

#col_list = ['round','pick','player_name','team','position','keeper_owner','keeper','keeper_round','kept_prev_year']
#keeper_eval = df_cols(keeper_eval,col_list)

