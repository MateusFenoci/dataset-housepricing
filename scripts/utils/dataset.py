import pandas as pd


webScraping = pd.read_csv("data.csv")
googleMaps = pd.read_csv("googlemaps.csv")


webScraping = webScraping.join(googleMaps)

webScraping.to_csv("dataset.csv",index=False)