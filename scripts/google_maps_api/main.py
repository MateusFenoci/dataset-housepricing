import pandas as pd
from scripts.utils import  get_features


df = pd.read_csv("data.csv")

for i, row in df.iterrows():
    try:
        info = pd.DataFrame([get_features(row["Lat"],row["Long"],500)])
        info.to_csv(f"googlemaps.csv",mode = "a", header=False ,index=False)
        print(f'Inserindo {i+1} de {df.shape[0]}')
    except Exception as e:
        print(f"Exception {e}")
        pass
        
    