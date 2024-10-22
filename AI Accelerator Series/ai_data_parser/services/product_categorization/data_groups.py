import pandas as pd

#Load data
sports_data = pd.read_csv('data/sports_combos.csv')
ent_data = pd.read_csv('data/entertainment_combos.csv')

#Sports Data
sport_product = list(set(sports_data['PRODUCT']))
sport_programming = list(set(sports_data['PROGRAMMING']))
sport_sport = list(set(sports_data['SPORT']))
sport_league = list(set(sports_data['LEAGUE']))
sport_show_title = list(set(sports_data['SHOW_TITLE']))

#Entertainment Data
ent_product = list(set(ent_data['PRODUCT']))
ent_content_brand_name = list(set(ent_data['CONTENT_BRAND_NAME']))
ent_genre = list(set(ent_data['GENRE']))
ent_show_title = list(set(ent_data['SHOW_TITLE']))