import numpy as npy
import pandas as pds
"""from sklearn.decomposition import TruncatedSVD"""
from scipy.sparse.linalg import svds

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
dataframe_ratings = pds.read_csv('1000_first_user_ratings.csv', sep=',', encoding='utf-8', usecols=['userId', 'movieId', 'rating', 'timestamp']).pivot(index = 'userId', columns ='movieId', values = 'rating').fillna(0.0)

prt("\nDataframe des ratings :\n\n%s"%(dataframe_ratings.head()))

# on convertit le dataframe en numpy array
npy_array = dataframe_ratings.values
# on masque les ratings non renseignes par le user
npy_array_masked = npy.ma.masked_array(npy_array, npy_array == 0.0)
# calcul de la moyenne des ratings pour chaque user
mean_scaler = npy.mean(npy_array_masked, axis = 1)
# on soustrait la moyenne des ratings du user a ses propres ratings
npy_array_finale = npy_array - (mean_scaler.reshape(-1, 1))

prt("\nNumpy array avec prise en compte de la moyenne des ratings de l'utilisateur :\n\n%s\n"%(npy_array_finale))


U, sigma, Vt = svds(npy_array_finale, k = 50)
predictions = npy.dot(npy.dot(U, npy.diag(sigma)), Vt) + mean_scaler.reshape(-1, 1)

dataframe_finale = pds.DataFrame(predictions, columns = dataframe_ratings.columns)

prt(dataframe_finale.head())

"""
dataframe_ratings : le dataframe avec les ratings de depart
dataframe : le dataframe calcule, dans lequel les valeurs des films non vus ne sont plus 0.0
"""
def max_movie_list(dataframe, row, nb_users, dataframe_ratings) :
    data = dataframe_finale.iloc[row]
    dict = {}
    res = []
    count = 0
    for i in range(len(data)) :
        dict[i] = data.iloc[i]
    while(count != nb_users) :
        maxi = None
        k_max = None
        for k in dict:
            if maxi is None or dict[k] > maxi:
                maxi = dict[k]
                k_max = k
        dict[k_max] = -5.0
        # le user a-t-il deja vu le film
        if(dataframe_ratings.iloc[row][k_max] == 0.0):
            print("deja vu")
            print(k_max)
        else :
            res.append(k_max)
            count += 1
            print("on ajoute")
    return res

# affiche le nom des movies a partir de la liste d'id de movies donnee en argument
def print_movies_name(filename, list_id_movies) :
    dataframe_movies = pds.read_csv(filename, sep=',', encoding='utf-8', names=['movieId', 'title', 'genres'])
    for i in range(len(list_id_movies)) :
        print("%s : %s"%(i+1, dataframe_movies['title'][list_id_movies[i]]))

print_movies_name('movies.csv', [1, 2, 3])
