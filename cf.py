import numpy as npy
import pandas as pds

# on peut choisir l'affichage verbeux ou non
""" set verb a True pour verbeux """
VERB = True


def prt(string):
    if (VERB):
        print(string)


from math import sqrt


def distance(user1, user2):
    square_user_1_2 = []
    for i in range(len(user1) - 1):
        if user1[i] != 0 and user2[i] != 0:
            square_user_1_2.append((user1[i] - user2[i]) ** 2)

    return sqrt(sum(square_user_1_2))


def pairwise_distances(matrix_ratings):
    matrix_len = len(matrix_ratings)
    # result = [[0] * matrix_len] * matrix_len
    result = npy.zeros((matrix_len, matrix_len))
    for i in range(matrix_len - 1):
        result[i][i] = 1
        for j in range(i + 1, matrix_len - 1):
            # prt("%d, %d"%(i,j))
            result[i][j] = distance(matrix_ratings[i], matrix_ratings[j])

    return result

def get_dataset():
    # lecture du .csv dans un dataframe
    """
    index : user
    colonne : movie
    values : rating (0.0 si non renseigne)
    """
    return pds.read_csv('100_first_user_ratings.csv', sep=',', encoding='utf-8',
                                     names=['user', 'movie', 'rating', 'tms']).pivot(index='user', columns='movie',
                                                                                     values='rating').fillna(0.0)
from sklearn import model_selection as ms

dataframe_ratings = get_dataset()

train, test = ms.train_test_split(dataframe_ratings, test_size=0.2)

dist_matrix = pairwise_distances(train.values)

prt(dist_matrix[:4, :4])
