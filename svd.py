import numpy as npy
import pandas as pds

# on peut choisir l'affichage verbeux ou non
""" set verb a True pour verbeux """

def prt(string) :
    verb = True
    if(verb) :
        print(string)

# lecture du .csv dans un dataframe
"""
index : user
colonne : movie
values : rating (0.0 si non renseigne)
"""
dataframe_ratings = pds.read_csv('100_first_user_ratings.csv', sep=',', encoding='utf-8', names=['user', 'movie', 'rating', 'tms']).pivot(index = 'user', columns ='movie', values = 'rating').fillna(0.0)

prt("\nDataframe des ratings :\n\n%s"%(dataframe_ratings.head()))

# on convertit le dataframe en numpy array
npy_array = dataframe_ratings.values
# on masque les ratings non renseignees par le user
npy_array_masked = npy.ma.masked_array(npy_array, npy_array == 0.0)
# calcul de la moyenne des ratings pour chaque user
mean_scaler = npy.mean(npy_array_masked, axis = 1)
# on soustrait la moyenne des ratings du user a ses propres ratings
npy_array_finale = npy_array + npy_array - (mean_scaler.reshape(-1, 1))

prt("\nNumpy array avec prise en compte de la moyenne des ratings de l'utilisateur :\n\n%s"%(npy_array_finale))
