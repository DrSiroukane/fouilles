def generate_users_movies_rating_matrix_with_all_movies(movies_file, ratings_file):
    """
    :param movies_file: movies file
    :param ratings_file: rating file

    :return: dictionary in a way
    {
        'user_1' : {'movie_1': rating_movie_1, 'movie_2': rating_movie_2, 'movie_3': rating_movie_3, ...},
        'user_2' : {'movie_1': rating_movie_1, 'movie_2': rating_movie_2, 'movie_3': rating_movie_3, ...},
        ...
    }
    """
    f_movies = open(movies_file, "r")
    f_ratings = open(ratings_file, "r")

    nbr_movies = sum(1 for _ in f_movies)
    dictionary = {}

    old_user_key = "-1"
    next_index = 1
    first = True
    for line in f_ratings:
        if not first:
            args = line.split(',')
            if args[0] not in dictionary.keys():
                if old_user_key != "-1":
                    for _index in range(next_index, nbr_movies):
                        dictionary[old_user_key][_index] = -1.0
                dictionary[args[0]] = {}
                old_user_key = args[0]

            movie_index = int(args[1])
            if movie_index <= nbr_movies:
                if next_index < movie_index:
                    for _index in range(next_index, movie_index):
                        dictionary[args[0]][_index] = -1.0
                dictionary[args[0]][movie_index] = float(args[2])
                next_index = movie_index + 1
        else:
            first = False

    return dictionary


def generate_users_movies_rating_matrix_with_all_movies_file(matrix, output_file):
    """
    :param matrix: result of generate users movies rating matrix function
    :param output_file: output file

    :return: create output file content matrix data
    """
    f_output = open(output_file, "w")

    for key_user in matrix:
        line = key_user
        for key_movie in matrix[key_user]:
            line += ", " + str(matrix[key_user][key_movie])
        f_output.write(line + "\n")

    f_output.close()


def generate_users_movies_rating_dictionary_from_file(users_movies_rating_file):
    """
    :param users_movies_rating_file: users x movies = rating file

    :return: dictionary in a way
    {
        'user_1' : {'movie_1': rating_movie_1, 'movie_2': rating_movie_2, 'movie_3': rating_movie_3, ...},
        'user_2' : {'movie_1': rating_movie_1, 'movie_2': rating_movie_2, 'movie_3': rating_movie_3, ...},
        ...
    }
    """
    f_users_movies_rating = open(users_movies_rating_file, "r")

    dictionary = {}
    for line in f_users_movies_rating:
        args = line.split(',')
        if args[0] not in dictionary.keys():
            dictionary[args[0]] = {}

        for i in range(1, len(args) - 1):
            value = float(args[i])
            if value != -1.0:
                dictionary[args[0]][i] = float(args[i])

    return dictionary


def distance(user1, user2):
    difference_absolue_notes = 0
    nombre_films_similaires = 0

    for movie1, note1 in user1.items():
        if movie1 in user2:
            difference_absolue_notes += (note1 - user2[movie1]) ** 2
            nombre_films_similaires += 1
        else:
            difference_absolue_notes += (note1 - 2.5) ** 2
            
    return (difference_absolue_notes / len(user1)) ** 0.5


import sys


def closest_users(user1, list_users):
    closest = sys.maxsize
    id_closest = -1
    for key_user, user in list_users.items():
        dist = distance(user1, user)
        if (dist < closest):
            closest = dist
            id_closest = key_user
    return (id_closest, closest)

def closest_users(user1, list_users, nb_users):
    list = []
    for key_user, user in list_users.items():
        list.append((key_user, distance(user1, user)))
    sorted(list, key=lambda dist: dist[1])
    return list[:nb_users]


# get the matrix
matrix = generate_users_movies_rating_matrix_with_all_movies("ml-20m/movies.csv", "100_first_user_ratings.csv")
# for key in matrix:
#     print(key)
#     print(matrix[key])
#     print()

# generate file content matrix data
generate_users_movies_rating_matrix_with_all_movies_file(matrix, "ml-20m/users_movies_rating_all.csv")

# generate dictionary from generated file
dic = generate_users_movies_rating_dictionary_from_file("ml-20m/users_movies_rating_all.csv")
# print(dic)

user = {29: 3.5, 32: 4}
"""
id, closes = closest_users(user, dic)
if 29 in dic[id].keys():
    print("29 :")
    print(dic[id][29])
if 32 in dic[id].keys():
    print("32 :")
    print(dic[id][32])
print(id)
print(closes)
print(user)
"""

print(closest_users(user, dic, 20))
