import pandas as pd

df = pd.read_csv('dane.csv')
print('=== NAZWY KOLUMN W CSV ===')
print(df.columns.tolist())
print('\n=== PIERWSZY WIERSZ (DANE) ===')
print(df.iloc[0].to_dict())
