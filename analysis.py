import pandas as pd
import pickle
import time
from tqdm import tqdm
from update import append_row
pd.set_option('display.max_columns', None)

streaks_df = pickle.load(open('maxstreaks.pickle', 'rb'))
matches_data = pickle.load(open('matches_data.pickle', 'rb'))
vals = pickle.load(open('columnvals.pickle', 'rb'))
teamwise_matches_data = pickle.load(open('teamwise_matches.pickle', 'rb'))

def get_random_top3(row_bool=True):
    sample = streaks_df.loc[row_bool & (streaks_df['Overall Top 3'] == True)].sample(n=1)
    print(sample)

get_random_top3()

