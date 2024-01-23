import pandas as pd
from collections import defaultdict
import pickle
from tqdm import tqdm
from get_features import get_features
import time

df1 = pd.read_csv('23-24.csv')
df2 = pd.read_csv('22-23.csv')
df3 = pd.read_csv('21-22.csv')
df4 = pd.read_csv('20-21.csv')
df5 = pd.read_csv('19-20.csv')
df6 = pd.read_csv('18-19.csv')

matches_data = pd.concat([df6, df5, df4, df3, df2, df1], ignore_index=True)[::-1]
cols_to_keep = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'Referee', 'B365H', 'B365A']

for c in matches_data.columns:
    if c not in cols_to_keep:
        matches_data.drop(c, axis=1, inplace=True)

matches_data['Date'] = pd.to_datetime(matches_data['Date'], dayfirst=True)

with open('matches_data.pickle', 'wb') as f:
    pickle.dump(matches_data, f, pickle.HIGHEST_PROTOCOL)

matches_data['Month'] = matches_data['Date'].apply(lambda x: x.month)
matches_data['Quarter'] = matches_data['Date'].apply(lambda x: x.quarter)

team_dfs = {}
for team in set(matches_data['HomeTeam']):
    temp_df = matches_data[(matches_data['HomeTeam'] == team) | (matches_data['AwayTeam'] == team)].reset_index()
    get_features(temp_df, team)
    team_dfs[team] = temp_df

with open('teamwise_matches.pickle', 'wb') as f:
    pickle.dump(team_dfs, f, pickle.HIGHEST_PROTOCOL)

streak_columns = ['Referee', 'Month', 'Quarter', 'AtHome', 'Opponent', 'Scored', 'Scored2Plus', 'Scored3Plus', 'CleanSheet', 'Conceded2Plus', 'Conceded3Plus', 'ScoredFirstHalf', 'Scored2PlusFirstHalf', 'CleanSheetFirstHalf', 'Conceded2PlusFirstHalf', 'ScoredSecondHalf',  'Scored2PlusSecondHalf', 'CleanSheetSecondHalf', 'Conceded2PlusSecondHalf', 'Won', 'Drew', 'Lost', 'WinningAtHalf', 'TiedAtHalf', 'LosingAtHalf', 'Favourites', 'Underdogs', 'OddsOnFavourites', 'OddsOnUnderdogs']
ref_vals = list(matches_data['Referee'].unique())
team_vals = list(matches_data['HomeTeam'].unique())
column_vals = dict([(name, [True, False]) for name in streak_columns])
column_vals['Referee'] = ref_vals
column_vals['Opponent'] = team_vals
column_vals['Month'] = [i for i in range(1, 13)]
column_vals['Quarter'] = [i for i in range(1, 5)]

with open('columnvals.pickle', 'wb') as f:
    pickle.dump(column_vals, f, pickle.HIGHEST_PROTOCOL)

def add_row_to_dict(team, name, val, cond1, cond1val, cond2, cond2val, streaks, indices, is_present, present_streak, present_index, key, out_dict):
    out_dict['Team'].append(team)

    out_dict['Tracking Stat'].append(name)
    out_dict['Tracking Value'].append(val)

    out_dict['Condition 1'].append(cond1)
    out_dict['Condition 1 Value'].append(cond1val)

    out_dict['Condition 2'].append(cond2)
    out_dict['Condition 2 Value'].append(cond2val)

    out_dict['Max Streak'].append(streaks['max1'])
    out_dict['Max Index'].append(indices['max1'])
    out_dict['Max Streak2'].append(streaks['max2'])
    out_dict['Max Index2'].append(indices['max2'])
    out_dict['Max Streak3'].append(streaks['max3'])
    out_dict['Max Index3'].append(indices['max3'])
    
    out_dict['key'].append(key)

    out_dict['Is Present Streak'].append(is_present)
    if is_present:
        out_dict['Present Streak'].append(present_streak)
        out_dict['Present Index'].append(present_index)
    else:
        out_dict['Present Streak'].append(None)
        out_dict['Present Index'].append(None)

# Function is defined so that ties are counted as losses for the newcomer. 
# This means that the max list will always have the most recent occurences in case of a tie
# This works because we are going in descending order of time
# Note that the current streak is not a part of the max streaks. 
# This is to allow comparison current streaks of all teams with historical streaks, current streaks, or both
def update_maxes(max_streaks_dict, max_indices_dict, streak, index):
    if streak <= max_streaks_dict['max2']:
        max_streaks_dict['max3'] = streak
        max_indices_dict['max3'] = index
    else:
        max_streaks_dict['max3'] = max_streaks_dict['max2']
        max_indices_dict['max3'] = max_indices_dict['max2']
        if streak <= max_streaks_dict['max1']:
            max_streaks_dict['max2'] = streak
            max_indices_dict['max2'] = index
        else:
            max_streaks_dict['max2'] = max_streaks_dict['max1']
            max_indices_dict['max2'] = max_indices_dict['max1']
            max_streaks_dict['max1'] = streak
            max_indices_dict['max1'] = index

# We only want to track streaks longer than 1, so the max are only replaced by streaks longer than 1
def streak_calculator(in_df, out_dict, overall_max_streaks_dict, overall_max_indices_dict, team_name, cond1 = None, cond1val = None, cond2 = None, cond2val = None):
    indices = in_df['index']
    for name, series in in_df.items():
        if name == 'index' or name==cond1 or name==cond2:
            continue
        vals_dict_streaks = dict([(v, {'max1': 1, 'max2': 1, 'max3': 1}) for v in column_vals[name]])
        vals_dict_indices = dict([(v, {'max1': None, 'max2': None, 'max3': None}) for v in column_vals[name]])
        present_streak = None
        present_val = None
        present_index = None
        if series.size > 0:
            present_streak = 1
            present_val = series[0]
            present_index = indices[0] 
            idx = 1
            skip = False
            while(True):
                if idx >= len(series):
                    skip = True
                    break
                if series[idx] == present_val:
                    present_streak += 1
                else:
                    present_index = indices[idx - 1]
                    break
                idx += 1

            if not skip:
                curr_streak = 1
                curr_val = series[idx]
                for i, s in enumerate(series[(idx + 1):], idx + 1):
                    if s == curr_val:
                        curr_streak += 1
                    else:
                        if curr_streak > vals_dict_streaks[curr_val]['max3']:
                            update_maxes(vals_dict_streaks[curr_val], vals_dict_indices[curr_val], curr_streak, indices[i-1])
                        curr_streak = 1
                        curr_val = s

                if curr_streak > vals_dict_streaks[curr_val]['max3']:
                    update_maxes(vals_dict_streaks[curr_val], vals_dict_indices[curr_val], curr_streak, indices[len(indices)-1])
    
        for val in column_vals[name]:
            key_items = [name, val, cond1, cond1val, cond2, cond2val]
            key = '_'.join([str(e) for e in key_items])
            if key in overall_max_streaks_dict:
                if vals_dict_streaks[val]['max1'] > overall_max_streaks_dict[key]['max3']:
                    update_maxes(overall_max_streaks_dict[key], overall_max_indices_dict[key], vals_dict_streaks[val]['max1'], vals_dict_indices[val]['max1'])
                    if vals_dict_streaks[val]['max2'] > overall_max_streaks_dict[key]['max3']:
                        update_maxes(overall_max_streaks_dict[key], overall_max_indices_dict[key], vals_dict_streaks[val]['max2'], vals_dict_indices[val]['max2'])
                        if vals_dict_streaks[val]['max3'] > overall_max_streaks_dict[key]['max3']:
                            update_maxes(overall_max_streaks_dict[key], overall_max_indices_dict[key], vals_dict_streaks[val]['max3'], vals_dict_indices[val]['max3'])
            else:
                overall_max_streaks_dict[key] = vals_dict_streaks[val]
                overall_max_indices_dict[key] = vals_dict_indices[val] 
            
            add_row_to_dict(team_name, name, val, cond1, cond1val, cond2, cond2val, 
                            vals_dict_streaks[val], vals_dict_indices[val], 
                            (present_val == val), present_streak, present_index, key, out_dict)

streaks_dict = defaultdict(list)
overall_max_streaks_dict = dict()
overall_max_indices_dict = dict()
for team, team_df in team_dfs.items():
    streak_calculator(team_df, streaks_dict, overall_max_streaks_dict, overall_max_indices_dict, team)

for team, team_df in team_dfs.items():
    for cond_name in team_df.keys():
        if cond_name == 'index':
            continue

        for cond_val in column_vals[cond_name]:
            filtered_df = team_df.loc[team_df[cond_name] == cond_val].reset_index(drop=True)
            streak_calculator(filtered_df, streaks_dict, overall_max_streaks_dict, overall_max_indices_dict, team, cond1=cond_name, cond1val=cond_val)

for team, team_df in tqdm(team_dfs.items()):

    for cond_one_name in team_df.keys():
        if cond_one_name == 'index':
            continue
    
        for cond_one_val in column_vals[cond_one_name]:
            for cond_two_name in team_df.keys():
                if cond_two_name == 'index' or cond_two_name == cond_one_name:
                    continue

                for cond_two_val in column_vals[cond_two_name]:
                    filtered_df = team_df.loc[(team_df[cond_one_name] == cond_one_val) & (team_df[cond_two_name] == cond_two_val)].reset_index(drop=True)
                    streak_calculator(filtered_df, streaks_dict, overall_max_streaks_dict, overall_max_indices_dict, team, 
                                      cond_one_name, cond_one_val, cond_two_name, cond_two_val)

streaks_df = pd.DataFrame.from_dict(streaks_dict)
streaks_df['Team'] = streaks_df['Team'].astype("category")
streaks_df['Tracking Stat'] = streaks_df['Tracking Stat'].astype("category")
streaks_df['Tracking Value'] = streaks_df['Tracking Value'].astype("category")
streaks_df['Condition 1'] = streaks_df['Condition 1'].astype("category")
streaks_df['Condition 1 Value'] = streaks_df['Condition 1 Value'].astype("category")
streaks_df['Condition 2'] = streaks_df['Condition 2'].astype("category")
streaks_df['Condition 2 Value'] = streaks_df['Condition 2 Value'].astype("category")

overall_maxes_dict = defaultdict(list)
for k in overall_max_indices_dict.keys():
    overall_maxes_dict['key'].append(k)
    streaks = overall_max_streaks_dict[k]
    indices = overall_max_indices_dict[k]
    overall_maxes_dict['Max Overall Streak'].append(streaks['max1'])
    overall_maxes_dict['Max Overall Index'].append(indices['max1'])
    overall_maxes_dict['Max Overall Streak2'].append(streaks['max2'])
    overall_maxes_dict['Max Overall Index2'].append(indices['max2'])
    overall_maxes_dict['Max Overall Streak3'].append(streaks['max3'])
    overall_maxes_dict['Max Overall Index3'].append(indices['max3'])
overall_maxes_df = pd.DataFrame.from_dict(overall_maxes_dict)

streaks_df = pd.merge(streaks_df, overall_maxes_df, on='key')
streaks_df.drop('key', axis=1, inplace=True)

streaks_df.loc[streaks_df['Is Present Streak'], 'Team Top 3'] = (streaks_df['Present Streak'] > streaks_df['Max Streak3']) & (streaks_df['Max Overall Streak'] > 1)
streaks_df.loc[streaks_df['Is Present Streak'], 'Overall Top 3'] = (streaks_df['Present Streak'] > streaks_df['Max Overall Streak3']) & (streaks_df['Max Overall Streak'] > 1)

with open('maxstreaks.pickle', 'wb') as f:
    pickle.dump(streaks_df, f, pickle.HIGHEST_PROTOCOL)

with open('overallmaxes.pickle', 'wb') as f:
    pickle.dump(overall_maxes_df, f, pickle.HIGHEST_PROTOCOL)