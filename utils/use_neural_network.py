import tensorflow as tf
import pandas as pd
import numpy as np


def make_prediction(dataset):
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
    model = tf.keras.models.load_model('model.h5')
    model.load_weights('ModelWeights.weights.h5')
    teste = dataset
    teste = teste[keypoints]

    prediction = model.predict(np.array([teste]).reshape(-1,24))
    return prediction
