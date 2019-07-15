import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('pokemon_model.csv')

x = df.drop(['Unnamed: 0', 'pokemon1', 'pokemon2', 'winner'], axis='columns')
y = df['winner']

from sklearn.model_selection import train_test_split
xtr, xts, ytr, yts = train_test_split(
    x,
    y,
    test_size = 0.1
)
model = RandomForestClassifier(n_estimators=20)
model.fit(xtr, ytr)
# print(x.columns.values)

import joblib
joblib.dump(model, 'modelML')