import numpy as npy
import pandas as pds

# on peut choisir l'affichage verbeux ou non
""" set verb a True pour verbeux """
VERB = True


def prt(string):
    if (VERB):
        print(string)


from math import sqrt


def distance(user1, user2, mean_ratings_movies):
    square_user_1_2 = []
    for i in range(len(user1) - 1):
        if user1[i] != 0 or user2[i] != 0:
            if user1[i] != 0:
                x = user1[i]
            else:
                x = mean_ratings_movies[i]
            if user2[i] != 0:
                y = user2[i]
            else:
                y = mean_ratings_movies[i]
            square_user_1_2.append((x - y) ** 2)

    return sqrt(sum(square_user_1_2))


def pairwise_distances(matrix_ratings):
    matrix_len = len(matrix_ratings)
    mean_ratings_movies = npy.mean(matrix_ratings, axis=0)

    result = npy.zeros((matrix_len, matrix_len))
    for i in range(matrix_len - 1):
        result[i][i] = 1
        for j in range(i + 1, matrix_len - 1):
            result[i][j] = result[j][i] = distance(matrix_ratings[i], matrix_ratings[j], mean_ratings_movies)

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

prt(dist_matrix[:5, :5])
