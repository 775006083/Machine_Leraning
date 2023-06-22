# -*- coding: utf-8 -*-
"""Bigml_IA_Telecom_Projet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VNA0GRkGidWGnZQPtlzEunjck9H5MTJ-
"""

import pandas as pd
import numpy as np
import pickle

#Charger les données du fichier
data = pd.read_csv("bigml.csv")
data.head()

#Afficher les colones de mon dataframe
print(data.columns)

#savoir les types de variables dans notre colonne
data.dtypes

#Infos sur les differents colones 
data.info()

#Afficher les valeurs statistiques de mon fichier 
data.describe()

"""# **Analyse des données manquantes**"""

#Dimension de mon dataframe
data.shape

#Verification des valeurs manquantes
data.isnull().sum()

"""Pas de valeurs manquantes"""

#Afficher les valeurs ddupliquées
data.duplicated()

"""pas de valeurs dupliqué"""

#Acceder au colone de type objet
data.iloc[:, [0,3,4,5,20]]

print ("Rows     : " ,data.shape[0])   #Afficher le nombre de ligne
print ("Columns  : " ,data.shape[1])   #Afficher le nombre de colone
print ("\nFeatures : \n" ,data.columns.tolist())   #Afficher les colonnes du dataset
print ("\nMissing values :  ", data.isnull().sum().values.sum())    #Compter les valeurs manquantes
print ("\nUnique values :  \n",data.nunique())   #Afficher les valeurs unique dans les colonnes

"""# **Normalisation des données**"""

def normalize(data):
  for column in data.columns:
    if data[column].dtypes not in ['object','bool']:
      max = data[column].max() 
      min = data[column].min()
      data[column]= (data[column]- min)/(max-min)
    return data
data = normalize(data)
data.head()

#Separer les client abonnées (Churn)  et no_abonnes(not_churn)
churn = data[data['churn'] == bool(True)]
no_churn = data[data['churn'] == bool(False)]

#Remplacer les valeurs Yes/No par 1 et 0 dans la colonne international plan
data['international plan']= data['international plan'].replace({"yes": 1, "no": 0}).astype(int)
data['voice mail plan'] = data['voice mail plan'].replace({"yes":1,"no":0}).astype(int)

#Effacer la colonne account length 
data = data.drop(['state','area code', 'phone number'], axis = 1)

#Afficher les les valeurs unique dans vmail message
print('unique vmail messages',data['number vmail messages'].unique())

#Affciher les colonnes de mon data
data.columns

#Diviser on dataset en featur (x) et targer (y)
x= data.drop(['churn'], axis=1).values
y = data['churn'].values

print(x.shape)
print(y.shape)

data.head()

"""# Encodage des valeurs categorielles"""

#Label Encoding categorical values
from sklearn.preprocessing import LabelEncoder
x_labelEncoder = LabelEncoder()
x[:,1] = x_labelEncoder.fit_transform(x[:,1])
x[:,2] = x_labelEncoder.fit_transform(x[:,2])

y_labelEncoder = LabelEncoder()
y = y_labelEncoder.fit_transform(y)

"""# Echantilloner le dataset en des données d'entrainement et de test"""

#Spliter le data en train et test 
from sklearn.model_selection import train_test_split 
x_train, x_test, y_train, y_test =  train_test_split(x,y, test_size= 0.20, random_state= 42)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

"""# **Algorithme de Random Forest**"""

#Importer les differents bibliotheques  de classification 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score 
#Suppression des erreurs de type warning 
import warnings 
warnings.simplefilter(action= 'ignore', category=FutureWarning)

#Random Forest
from sklearn.ensemble import RandomForestClassifier
randomforest = RandomForestClassifier()
randomforest.fit(x_train, y_train)
predict = randomforest.predict(x_test)
print("Score Random Forest", accuracy_score(predict, y_test))

# Saving model to disk
pickle.dump(randomforest, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))

print(model.predict([[128,	0,	1,	25,	265.1,	110,	45.07,	197.4,	99,	16.78,	244.7,	91,	11.01,	10.0,	3,	2.70,	1]]))