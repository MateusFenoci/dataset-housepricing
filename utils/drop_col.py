import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras import layers, models, callbacks
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.metrics import mean_squared_log_error
import seaborn as sns
from sklearn.base import clone
import joblib


seed = 13

df = pd.read_csv("dataset.csv")

y = df["Rent"]
df = df.drop(columns=["Location","ID","Rent","Lat","Long"])



'''scaler = RobustScaler()
scaler.fit(df)
df = pd.DataFrame(scaler.transform(df))'''

X_train, X_test, y_train, y_test = train_test_split(
    df, y, test_size=0.2, random_state=seed)


model = GradientBoostingRegressor(n_estimators=200,random_state=seed)

model.fit(X_train, y_train)


pred = model.predict(X_test)
rmsle = mean_squared_log_error(y_test,pred) ** 0.5

## Avaliando o modelo

print(f"Mean RMSlE: {rmsle}")


def imp_df(column_names, importances):
    df = pd.DataFrame({'feature': column_names,'feature_importance': importances}).sort_values('feature_importance', ascending = False)
    return df


def drop_col_feat_imp(model, X_train, y_train, random_state = 42):
    
    # Clonando um modelo referencia
    model_clone = clone(model)
    model_clone.random_state = random_state
    model_clone.fit(X_train, y_train)
    benchmark_score = model_clone.score(X_train, y_train)
    importances = []

    for col in X_train.columns:
        
        #Treinar o mesmo modelo com uma coluna a menos e avaliar este impacto na performance do modelo
        model_clone = clone(model)
        model_clone.random_state = random_state
        model_clone.fit(X_train.drop(col, axis = 1), y_train)
        drop_col_score = model_clone.score(X_train.drop(col, axis = 1), y_train)
        importances.append(benchmark_score - drop_col_score)

        print(f"{col} = {benchmark_score - drop_col_score}")

    importances_df = imp_df(X_train.columns, importances)
    return importances_df



#Plotando um grafico de barras com as importancias das variaveis
importances = drop_col_feat_imp(model,X_train,y_train)
importances.to_csv("importances.csv",index=False)
plt.barh(importances["feature"],importances["feature_importance"])
plt.yticks(fontsize=6)
plt.show()


#Plotando um histograma para a variavel alvo
plt.figure(figsize=(9, 8))
plt.title("Frequencia em SalePrice")
sns.distplot(y, color='g', bins=100, hist_kws={'alpha': 0.4})

plt.show()


#Plotando um grafico com a correlação entre as variaveis
data = pd.concat([X_train,y_train],axis=1)
corr_matrix = data.corr()
sns.heatmap(corr_matrix.iloc[-20:, -20:], annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Features')
plt.show()


















