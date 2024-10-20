import pandas as pd
from sklearn.model_selection import GridSearchCV,train_test_split
import matplotlib.pyplot as plt
import numpy as np
from keras import layers,models,callbacks



seed = 42

df = pd.read_csv("data/dataset.csv")

y = df["Rent"]

keypoints = [
    'school',             # Escolas
    'hospital',           # Hospitais
    'supermarket',        # Supermercados
    'subway_station',     # Estações de metrô
    'train_station',      # Estações de trem
    'bus_station',        # Estações de ônibus
    'park',               # Parques
    'restaurant',         # Restaurantes
    'shopping_mall',      # Shopping centers
    'gym',                # Academias
    'police',             # Delegacias de polícia
    'university',         # Universidades
    'Parking Spaces',     # Vagas de estacionamento
    'Square Meters',      # Metros quadrados
    'doctor',             # Médicos
    'parking',            # Estacionamento
    'Furnished?',         # Mobilhado?
    'pet_store',          # Pet shop
    'car_repair',         # Oficinas de reparação de automóveis
    'atm',                # Caixas eletrônicos
    'cafe',               # Cafés
    'Condo Fee',          # Taxa de condomínio
    'Property Tax',       # Imposto sobre propriedade
    'Fire Insurance'      # Seguro contra incêndio
]

df = df[keypoints]

X_train, X_test, y_train, y_test = train_test_split(
    df, y, test_size=0.2, random_state=seed)

model = models.Sequential()

model.add(layers.Dense(24,activation="relu",input_dim=24))

model.add(layers.Dense(16,activation="relu"))
model.add(layers.Dense(8,activation="relu"))

model.add(layers.Dense(1))

model.compile(optimizer="adam",loss="mean_absolute_error",metrics=["mean_absolute_error"])

callback = callbacks.ModelCheckpoint("best.keras",save_best_only=True)
early_stopping_callback = callbacks.EarlyStopping(monitor="loss",patience=5,restore_best_weights=True)  

history = model.fit(X_train, y_train, 
                    epochs=500, 
                    batch_size=64, 
                    validation_data=(X_test, y_test), 
                    shuffle=True, 
                    callbacks=[early_stopping_callback,callback],
                    verbose=1)

teste = pd.read_csv('teste.csv')
teste = teste[keypoints]

prediction = model.predict(np.array([teste]).reshape(-1,24))

#Salvando o modelo
model.save("model.h5")

#Salvando os pesos
model.save_weights("ModelWeights.weights.h5")

#Plotando o grafico de loss
plt.plot(history.history['loss'],color='red',label='training loss')
plt.plot(history.history['val_loss'],color='blue',label='validation loss')
plt.legend()
plt.show()