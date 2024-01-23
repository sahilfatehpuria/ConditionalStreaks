'''
THIS IS NOT USABLE CODE. 
IT IS COMPLETELY UNOPTIMIZED AND WILL TAKE HOURS TO RUN. 
IT IS INCLUDED AS REFERENCE OF WHAT AN UPDATE FUCNTION NEEDS TO DO. 
FOR NOW EASIEST WAY TO UPDATE IS TO RERUN PROCESSING
'''

# import pandas as pd
# from tqdm import tqdm

# def append_row(team, update_row, streaks_df, column_vals):
#     def update_df_maxes(streak, index, row_bool, overall_bool):
#         if streak > streaks_df.loc[row_bool, 'Max Streak'].item():
#                 streaks_df.loc[row_bool, 'Max Streak3'] = streaks_df.loc[row_bool, 'Max Streak2']
#                 streaks_df.loc[row_bool, 'Max Index3'] = streaks_df.loc[row_bool, 'Max Index2']
#                 streaks_df.loc[row_bool, 'Max Streak2'] = streaks_df.loc[row_bool, 'Max Streak']
#                 streaks_df.loc[row_bool, 'Max Index2'] = streaks_df.loc[row_bool, 'Max Index']
#                 streaks_df.loc[row_bool, 'Max Streak'] = streak
#                 streaks_df.loc[row_bool, 'Max Index'] = index
#         elif streak > streaks_df.loc[row_bool, 'Max Streak2'].item():
#             streaks_df.loc[row_bool, 'Max Streak3'] = streaks_df.loc[row_bool, 'Max Streak2']
#             streaks_df.loc[row_bool, 'Max Index3'] = streaks_df.loc[row_bool, 'Max Index2']
#             streaks_df.loc[row_bool, 'Max Streak2'] = streak
#             streaks_df.loc[row_bool, 'Max Index2'] = index
#         elif streak > streaks_df.loc[row_bool, 'Max Streak3'].item():
#             streaks_df.loc[row_bool, 'Max Streak3'] = streak
#             streaks_df.loc[row_bool, 'Max Index3'] = index
            
#         if streak > streaks_df.loc[row_bool, 'Max Overall Streak'].item():
#             streaks_df.loc[overall_bool, 'Max Overall Streak3'] = streaks_df.loc[overall_bool, 'Max Overall Streak2']
#             streaks_df.loc[overall_bool, 'Max Overall Index3'] = streaks_df.loc[overall_bool, 'Max Overall Index2']
#             streaks_df.loc[overall_bool, 'Max Overall Streak2'] = streaks_df.loc[overall_bool, 'Max Overall Streak']
#             streaks_df.loc[overall_bool, 'Max Overall Index2'] = streaks_df.loc[overall_bool, 'Max Overall Index']
#             streaks_df.loc[overall_bool, 'Max Overall Streak'] = streak
#             streaks_df.loc[overall_bool, 'Max Overall Index'] = index
#         elif streak > streaks_df.loc[row_bool, 'Max Overall Streak2'].item():
#             streaks_df.loc[overall_bool, 'Max Overall Streak3'] = streaks_df.loc[overall_bool, 'Max Overall Streak2']
#             streaks_df.loc[overall_bool, 'Max Overall Index3'] = streaks_df.loc[overall_bool, 'Max Overall Index2']
#             streaks_df.loc[overall_bool, 'Max Overall Streak2'] = streak
#             streaks_df.loc[overall_bool, 'Max Overall Index2'] = index
#         elif streak > streaks_df.loc[row_bool, 'Max Overall Streak3'].item():
#             streaks_df.loc[overall_bool, 'Max Overall Streak3'] = streak
#             streaks_df.loc[overall_bool, 'Max Overall Index3'] = index

#     def update_streaks(new_val, present_val, row_bool, overall_bool, new_bool):
#         if new_val == present_val:
#             streaks_df.loc[row_bool, 'Present Streak'] += 1
#         else:
#             streak = streaks_df.loc[row_bool, 'Present Streak'].item()
#             index = streaks_df.loc[row_bool, 'Present Index'].item()
#             update_df_maxes(streak, index, row_bool, overall_bool)
            
#             streaks_df.loc[row_bool, 'Present Streak'] = None
#             streaks_df.loc[row_bool, 'Present Index'] = None
#             streaks_df.loc[row_bool, 'Is Present Streak'] = False

#             streaks_df.loc[new_bool, 'Is Present Streak'] = True
#             streaks_df.loc[new_bool, 'Present Streak'] = 1
#             streaks_df.loc[new_bool, 'Present Index'] = update_row['index']

#     for tracking_col in tqdm(column_vals.keys()):
#         new_val = update_row[tracking_col]
#         row_bool = (streaks_df['Team'] == team) & (streaks_df['Tracking Stat'] == tracking_col) & (streaks_df['Is Present Streak'] == True) & (streaks_df['Condition 1'].isna())
#         present_val = streaks_df.loc[row_bool, 'Tracking Value'].item()
#         overall_bool = (streaks_df['Tracking Stat'] == tracking_col) & (streaks_df['Tracking Value'] == present_val) & (streaks_df['Condition 1'].isna())
#         new_bool = (streaks_df['Team'] == team) & (streaks_df['Tracking Stat'] == tracking_col) & (streaks_df['Tracking Value'] == new_val) & (streaks_df['Condition 1'].isna())
#         update_streaks(new_val, present_val, row_bool, overall_bool, new_bool)

#         for cond1 in tqdm(column_vals.keys()):
#             if cond1 == tracking_col:
#                 continue
#             row_bool = (streaks_df['Team'] == team) & (streaks_df['Tracking Stat'] == tracking_col) & \
#                         (streaks_df['Is Present Streak'] == True) & (streaks_df['Condition 1'] == cond1) & \
#                         (streaks_df['Condition 1 Value'] == update_row[cond1]) & (streaks_df['Condition 2'].isna())
#             present_val = streaks_df.loc[row_bool, 'Tracking Value'].item()    
#             overall_bool = (streaks_df['Tracking Stat'] == tracking_col) & (streaks_df['Tracking Value'] == present_val) & \
#                             (streaks_df['Condition 1'] == cond1) & (streaks_df['Condition 1 Value'] == update_row[cond1]) & \
#                             (streaks_df['Condition 2'].isna())
#             new_bool = (streaks_df['Team'] == team) & (streaks_df['Tracking Stat'] == tracking_col) & \
#                         (streaks_df['Tracking Value'] == new_val) & (streaks_df['Condition 1'] == cond1) & \
#                         (streaks_df['Condition 1 Value'] == update_row[cond1]) & (streaks_df['Condition 2'].isna())
#             update_streaks(new_val, present_val, row_bool, overall_bool, new_bool)
#             for cond2 in tqdm(column_vals.keys()):
#                 if cond2 == tracking_col or cond1 == cond2:
#                     continue
#                 row_bool = (streaks_df['Team'] == team) & (streaks_df['Tracking Stat'] == tracking_col) & \
#                             (streaks_df['Is Present Streak'] == True) & (streaks_df['Condition 1'] == cond1) & \
#                             (streaks_df['Condition 1 Value'] == update_row[cond1]) & (streaks_df['Condition 2'] == cond2) & \
#                             (streaks_df['Condition 2 Value'] == update_row[cond2])
#                 present_val = streaks_df.loc[row_bool, 'Tracking Value'].item()    
#                 overall_bool = (streaks_df['Tracking Stat'] == tracking_col) & (streaks_df['Tracking Value'] == present_val) & \
#                                 (streaks_df['Condition 1'] == cond1) & (streaks_df['Condition 1 Value'] == update_row[cond1]) & \
#                                 (streaks_df['Condition 2'] == cond2) & (streaks_df['Condition 2 Value'] == update_row[cond2])
#                 new_bool = (streaks_df['Team'] == team) & (streaks_df['Tracking Stat'] == tracking_col) & \
#                             (streaks_df['Tracking Value'] == new_val) & (streaks_df['Condition 1'] == cond1) & \
#                             (streaks_df['Condition 1 Value'] == update_row[cond1]) & (streaks_df['Condition 2'] == cond2) & \
#                             (streaks_df['Condition 2 Value'] == update_row[cond2])
#                 update_streaks(new_val, present_val, row_bool, overall_bool, new_bool)