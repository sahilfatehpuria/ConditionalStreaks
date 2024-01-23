def get_features(temp_df, team):
    
    streak_columns = ['Referee', 'Month', 'Quarter', 'AtHome', 'Opponent', 'Scored', 'Scored2Plus', 'Scored3Plus', 'CleanSheet', 'Conceded2Plus', 'Conceded3Plus', 'ScoredFirstHalf', 'Scored2PlusFirstHalf', 'CleanSheetFirstHalf', 'Conceded2PlusFirstHalf', 'ScoredSecondHalf',  'Scored2PlusSecondHalf', 'CleanSheetSecondHalf', 'Conceded2PlusSecondHalf', 'Won', 'Drew', 'Lost', 'WinningAtHalf', 'TiedAtHalf', 'LosingAtHalf', 'Favourites', 'Underdogs', 'OddsOnFavourites', 'OddsOnUnderdogs']

    temp_df['AtHome'] = temp_df['HomeTeam'].apply(lambda x: x==team)
    temp_df['Opponent'] = temp_df[['HomeTeam', 'AwayTeam', 'AtHome']].apply(lambda x: x['AwayTeam'] if x['AtHome'] else x['HomeTeam'], axis=1)

    temp_df['NumScored'] = temp_df[['FTHG', 'FTAG', 'AtHome']].apply(lambda x: (x['FTHG']) if x['AtHome'] else (x['FTAG']), axis=1)
    temp_df['NumConceded'] = temp_df[['FTHG', 'FTAG', 'AtHome']].apply(lambda x: (x['FTAG']) if x['AtHome'] else (x['FTHG']), axis=1)

    temp_df['NumScoredFirstHalf'] = temp_df[['HTHG', 'HTAG', 'AtHome']].apply(lambda x: (x['HTHG']) if x['AtHome'] else (x['HTAG']), axis=1)
    temp_df['NumConcededFirstHalf'] = temp_df[['HTHG', 'HTAG', 'AtHome']].apply(lambda x: (x['HTAG']) if x['AtHome'] else (x['HTHG']), axis=1)

    temp_df['NumScoredSecondHalf'] = temp_df[['NumScored', 'NumScoredFirstHalf']].apply(lambda x: x['NumScored'] - x['NumScoredFirstHalf'], axis=1)
    temp_df['NumConcededSecondHalf'] = temp_df[['NumConceded', 'NumConcededFirstHalf']].apply(lambda x: x['NumConceded'] - x['NumConcededFirstHalf'], axis=1)

    temp_df['WinningOdds'] = temp_df[['B365H', 'B365A', 'AtHome']].apply(lambda x: x['B365H'] if x['AtHome'] else x['B365A'], axis=1)
    temp_df['LosingOdds'] = temp_df[['B365H', 'B365A', 'AtHome']].apply(lambda x: x['B365A'] if x['AtHome'] else x['B365H'], axis=1)

    temp_df['Scored'] = temp_df['NumScored'].apply(lambda x: x > 0)
    temp_df['Scored2Plus'] = temp_df['NumScored'].apply(lambda x: x > 1)
    temp_df['Scored3Plus'] = temp_df['NumScored'].apply(lambda x: x > 2)
    temp_df['CleanSheet'] = temp_df['NumConceded'].apply(lambda x: x == 0)
    temp_df['Conceded2Plus'] = temp_df['NumConceded'].apply(lambda x: x > 1)
    temp_df['Conceded3Plus'] = temp_df['NumConceded'].apply(lambda x: x > 2)

    temp_df['ScoredFirstHalf'] = temp_df['NumScoredFirstHalf'].apply(lambda x: x > 0)
    temp_df['Scored2PlusFirstHalf'] = temp_df['NumScoredFirstHalf'].apply(lambda x: x > 1)
    temp_df['CleanSheetFirstHalf'] = temp_df['NumConcededFirstHalf'].apply(lambda x: x == 0)
    temp_df['Conceded2PlusFirstHalf'] = temp_df['NumConcededFirstHalf'].apply(lambda x: x > 1)
    
    temp_df['ScoredSecondHalf'] = temp_df['NumScoredSecondHalf'].apply(lambda x: x > 0)
    temp_df['Scored2PlusSecondHalf'] = temp_df['NumScoredSecondHalf'].apply(lambda x: x > 1)
    temp_df['CleanSheetSecondHalf'] = temp_df['NumConcededSecondHalf'].apply(lambda x: x == 0)
    temp_df['Conceded2PlusSecondHalf'] = temp_df['NumConcededSecondHalf'].apply(lambda x: x > 1)

    temp_df['Won'] = temp_df[['NumScored', 'NumConceded']].apply(lambda x: x['NumScored'] > x['NumConceded'], axis=1)
    temp_df['Drew'] = temp_df['FTR'].apply(lambda x: x == 'D')
    temp_df['Lost'] = temp_df[['NumScored', 'NumConceded']].apply(lambda x: x['NumScored'] < x['NumConceded'], axis=1)

    temp_df['WinningAtHalf'] = temp_df[['NumScoredFirstHalf', 'NumConcededFirstHalf']].apply(lambda x: x['NumScoredFirstHalf'] > x['NumConcededFirstHalf'], axis=1)
    temp_df['TiedAtHalf'] = temp_df['HTR'].apply(lambda x: x == 'D')
    temp_df['LosingAtHalf'] = temp_df[['NumScoredFirstHalf', 'NumConcededFirstHalf']].apply(lambda x: x['NumScoredFirstHalf'] < x['NumConcededFirstHalf'], axis=1)

    # Favourites - Bookmakers (Bet365) think they were more likely to win this game than the opponent
    temp_df['Favourites'] = temp_df[['WinningOdds', 'LosingOdds']].apply(lambda x: x['WinningOdds'] < x['LosingOdds'], axis=1)

    # Underdogs - Bookmakers (Bet365) think they were less likely to win this game than the opponent
    temp_df['Underdogs'] = temp_df[['WinningOdds', 'LosingOdds']].apply(lambda x: x['WinningOdds'] > x['LosingOdds'], axis=1)

    #Odds On Favourites- Bookmakers (Bet365) think they were more likely to win this game than not win it
    temp_df['OddsOnFavourites'] = temp_df['WinningOdds'].apply(lambda x: x < 2)

    #Odds On Underdogs- Bookmakers (Bet365) think they were more likely to win this game than not win it
    temp_df['OddsOnUnderdogs'] = temp_df['LosingOdds'].apply(lambda x: x < 2)
  
    for c in temp_df.columns:
            if c not in streak_columns and c != 'index':
                temp_df.drop(c, axis=1, inplace=True)