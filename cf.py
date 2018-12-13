import numpy as npy
import pandas as pds

# on peut choisir l'affichage verbeux ou non
""" set verb a True pour verbeux """
VERB = True

USER_COL = 'userId'
MOVIE_COL = 'movieId'
RATING_COL = 'rating'
TIMESTAMP_COL = 'timestamp'
TITLE_COL = 'title'
GENRES_COL = 'genres'

RATING_FILE_PATH = '100_first_user_ratings.csv'
MOVIES_FILE_PATH = 'ml-20m/movies.csv'


def prt(string):
    if (VERB):
        print(string)


from math import sqrt


def distance(user1, user2, mean_ratings_movies_list):
    square_user_1_2 = []
    for i in range(len(user1)):
        if user1[i] != 0 or user2[i] != 0:
            if user1[i] != 0:
                x = user1[i]
            else:
                x = mean_ratings_movies_list[i]

            if user2[i] != 0:
                y = user2[i]
            else:
                y = mean_ratings_movies_list[i]

            square_user_1_2.append((x - y) ** 2)

    return sqrt(sum(square_user_1_2))


def get_csv_index(dataframe_csv_index_list, dataframe_index):
    return dataframe_csv_index_list[dataframe_index]


def get_dataframe_index(dataframe_csv_index_list, csv_index):
    return dataframe_csv_index_list.index(csv_index)


def global_distances(matrix_ratings):
    matrix_len = len(matrix_ratings)
    mean_ratings_movies_list = npy.mean(matrix_ratings, axis=0).tolist()  # list of movies mean

    result = npy.zeros((matrix_len, matrix_len))
    for i in range(matrix_len):
        for j in range(i + 1, matrix_len):
            result[i][j] = result[j][i] = distance(matrix_ratings[i], matrix_ratings[j], mean_ratings_movies_list)

    return result


def get_closest_users_ids(dataset_matrix, dataframe_user_csv_index_list, user_id, n=5):
    dataframe_user_index = get_dataframe_index(dataframe_user_csv_index_list, user_id)
    current_user_distances = dataset_matrix[dataframe_user_index].tolist()
    user_distances_sorted = sorted(current_user_distances)

    result = []
    for i in range(1, n + 1):
        result.append(get_csv_index(
            dataframe_user_csv_index_list,
            current_user_distances.index(user_distances_sorted[i])))
    return result


def get_favorit_movies_specified_user(user_movies_list, dataframe_movies_csv_index_list):
    result = [], []
    for i in range(len(user_movies_list)):
        if user_movies_list[i] >= 4:
            result[0].append(dataframe_movies_csv_index_list[i])
            result[1].append(user_movies_list[i])

    return result


def get_recommendation_movies_for_each_closest_user(dataset_matrix, closest_users_csv_index_list,
                                                    dataframe_movies_csv_index_list):
    dic = {}
    for user_csv_index in closest_users_csv_index_list:
        user_dataframe_index = get_dataframe_index(dataframe_user_csv_index_list, user_csv_index)
        user_movies_list = dataset_matrix[user_dataframe_index].tolist()
        dic[user_csv_index] = get_favorit_movies_specified_user(user_movies_list, dataframe_movies_csv_index_list)
    return dic


def get_final_recommendation_movies(recomendation_movies_for_each_closest_user, n=10):
    recommendation_movies_list = []
    for key, value in dic.items():
        recommendation_movies_list += value[0]
    recommendation_movies_list = sorted(list(set(recommendation_movies_list)))
    # prt(recommendation_movies_list)

    nbr_of_movies = len(recommendation_movies_list)
    count_nbr_of_watcher = [0] * nbr_of_movies
    sum_of_ratings = [0] * nbr_of_movies

    for i in range(nbr_of_movies):
        for user_csv_index, user_favorit_movies_list in recomendation_movies_for_each_closest_user.items():
            movie_csv_index = recommendation_movies_list[i]
            if movie_csv_index in user_favorit_movies_list[0]:
                count_nbr_of_watcher[i] += 1
                sum_of_ratings[i] += user_favorit_movies_list[1][user_favorit_movies_list[0].index(movie_csv_index)]

    # prt(count_nbr_of_watcher)
    # prt(sum_of_ratings)

    avg_of_ratings = []
    for i in range(nbr_of_movies):
        avg_of_ratings.append(
            (recommendation_movies_list[i], sum_of_ratings[i] / count_nbr_of_watcher[i] + count_nbr_of_watcher[i]))
    avg_of_ratings.sort(key=lambda tup: tup[1], reverse=True)

    return avg_of_ratings[:n]


def mess_with_test_users_ratings(dataset_matrix, test_user_index_list, n=1):
    dic = {}
    for user_index in test_user_index_list[:5]:
        # prt(dataset_matrix[user_index].tolist())
        dic[user_index] = get_favorit_movies_specified_user(dataset_matrix[user_index].tolist())
    return dic


def get_dataset_ratings():
    return pds.read_csv(RATING_FILE_PATH, sep=',', encoding='utf-8',
                        usecols=[USER_COL, MOVIE_COL, RATING_COL, TIMESTAMP_COL]).pivot(index=USER_COL,
                                                                                        columns=MOVIE_COL,
                                                                                        values=RATING_COL).fillna(0.0)


def get_dataset_movies():
    return pds.read_csv(MOVIES_FILE_PATH, sep=',', encoding='utf-8',
                        usecols=[MOVIE_COL, TITLE_COL, GENRES_COL])


def get_dataset_movies_as_dictionnary():
    dataframe_movies = get_dataset_movies().values
    dic = {}
    for line in dataframe_movies:
        dic[line[0]] = line[1]
    return dic


def display_recommendation_movies(final_result):
    movies_dictionnary = get_dataset_movies_as_dictionnary()

    for tup in final_result:
        print("%d: %s" % (tup[0], movies_dictionnary[tup[0]]))


# Main programme

from sklearn import model_selection as ms

dataframe_ratings = get_dataset_ratings()

dataframe_user_csv_index_list = dataframe_ratings.index.values.tolist()
dataframe_movies_csv_index_list = dataframe_ratings.columns.values.tolist()

train_user_csv_index_list, test_user_csv_index_list = ms.train_test_split(dataframe_user_csv_index_list, test_size=0.2)

dist_matrix = global_distances(dataframe_ratings.values)


# recommendation for a random user
import random

selected_user = random.choice(dataframe_user_csv_index_list)
closest_users = get_closest_users_ids(dist_matrix, dataframe_user_csv_index_list, selected_user, n=15)  # default n = 5

dic = get_recommendation_movies_for_each_closest_user(dataframe_ratings.values, closest_users,
                                                      dataframe_movies_csv_index_list)

final_result = get_final_recommendation_movies(dic, n=15)

prt(final_result)

display_recommendation_movies(final_result)
