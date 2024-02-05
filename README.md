# ConditionalStreaks
Systematically find all conditional streaks in historic premier league data.

An example of a conditional streak is Liverpool have scored at least two goals in their last 10 games when playing at home in February (fictional example).
This program iterates over all matches inputted, and calculates all current streaks, as well as top 3 streaks for each team, as well as the overall top 3, for each combination of tracking stat, and two conditions. 

The list of stats currently used as conditions or tracking stats are:
- Referee
- Month
- Quarter
- AtHome
- Opponent
- Scored
- Scored2Plus
- Scored3Plus
- CleanSheet
- Conceded2Plus
- Conceded3Plus
- ScoredFirstHalf
- Scored2PlusFirstHalf
- CleanSheetFirstHalf
- Conceded2PlusFirstHalf
- ScoredSecondHalf
- Scored2PlusSecondHalf
- CleanSheetSecondHalf
- Conceded2PlusSecondHalf
- Won
- Drew
- Lost
- WinningAtHalf
- TiedAtHalf
- LosingAtHalf
- Favourites
- Underdogs
- OddsOnFavourites
- OddsOnUnderdogs

So in the example used above, the tracking stat would be Scored2Plus, the first condition would be AtHome=True, and the second condition is Month=2 (Feb)

## Current Functionality

Currently, the program can calculate streaks for all inputted data. The data for seasons 18/19 - 23/24 (ongoing) are included in the repository. This data is taken from https://www.football-data.co.uk/englandm.php. More seasons can be included to get more historical data. This data is stored in a pickle format, and can be used by the analysis.py file to output any number of random 'interesting' streaks, where interesting refers to a current streak that would place in the overall top 3 for that category, and is not trivial (eg. Tracking Stat: Scored, Condition 1: Scored First Half). Further conditions can be added to filter the possible results, eg. the team for which you want to find streaks, or which stats to condition on.

## Work Still to be done

1. Create a user interface that allows one to find a random interesting streak based on selectable criteria on a web page, rather than through code. 
2. Implement a way to update the dataset with latest matches data automatically, using an API or web scraping.

### Note on statistical significance

This work is consciously looking for outliers. Thus, any streaks found through this method cannot be seen as statistically significant. This is purely for intrigue purposes. In any dataset this large, there are bound to be results far awy from the mean. This does not mean that these streaks are likely or unlikely to continue. PLEASE DO NOT USE THIS AS BETTING ADVICE. Refer to https://www.tylervigen.com/spurious-correlations for a great illustration of the kind of conclusions one might be tricked into drawing if looking at enough data without a specific hypothesis.
