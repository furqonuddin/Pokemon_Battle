import pandas as pd
import numpy as np

dfp = pd.read_csv('pokemon.csv')
dfc = pd.read_csv('combats.csv')


dfp = dfp.drop(['Type 1', 'Type 2', 'Generation', 'Legendary', 'Name'], axis='columns')

dfp1 = pd.merge(dfc,dfp, left_on='Second_pokemon', right_on='#', how='inner')
dfp1 = dfp1.rename(
    {
        'First_pokemon':'pokemon1',
        'Second_pokemon':'pokemon2',
        '#':'id',
        'HP': 'HP2',
        'Attack': 'Attack2',
        'Defense': 'Defense2',
        'Sp. Atk':'Sp. Atk2',
        'Sp. Def':'Sp. Def2',
        'Speed':'Speed2',
        'Winner':'winner'

    }, axis='columns'
)
dfp1 = pd.merge(dfp1,dfp, left_on='pokemon1', right_on='#', how='inner')
dfp1 = dfp1.drop(['#', 'id'], axis='columns')
# print(dfp1.columns.values)
# print(dfp1['winner'].iloc[0])

win =[]
for i in range(len(dfp1)):
    if dfp1['winner'].iloc[i] == dfp1['pokemon1'].iloc[i]:
        h = 1
        win.append(h)
    else:
        h = 0
        win.append(h)
dfp1['winner']=win
# print(dfp1.head(10))
dfp1.to_csv('pokemon_model.csv')