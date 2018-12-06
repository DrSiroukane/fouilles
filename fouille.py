def generate_users_movies_ranking_matrix(movies_file, rankings_file):
    """
    :param movies_file: movies file
    :param rankings_file: ranking file

    :return: dictionary in a way
    {
        'user_1' : {'movie_1': ranking_movie_1, 'movie_2': ranking_movie_2, 'movie_3': ranking_movie_3, ...},
        'user_2' : {'movie_1': ranking_movie_1, 'movie_2': ranking_movie_2, 'movie_3': ranking_movie_3, ...},
        ...
    }
    """
    f_movies = open(movies_file, "r")
    f_rankings = open(rankings_file, "r")

    nbr_movies = sum(1 for _ in f_movies) - 1
    dictionary = {}

    first = True
    for line in f_rankings:
        if not first:
            args = line.split(',')
            if args[0] not in dictionary.keys():
                dictionary[args[0]] = {}

            movie_index = int(args[1])
            if movie_index <= nbr_movies:
                dictionary[args[0]][movie_index] = float(args[2])
        else:
            first = False

    return dictionary


def generate_users_movies_ranking_matrix_with_all_movies(movies_file, rankings_file):
    """
    :param movies_file: movies file
    :param rankings_file: ranking file

    :return: dictionary in a way
    {
        'user_1' : {'movie_1': ranking_movie_1, 'movie_2': ranking_movie_2, 'movie_3': ranking_movie_3, ...},
        'user_2' : {'movie_1': ranking_movie_1, 'movie_2': ranking_movie_2, 'movie_3': ranking_movie_3, ...},
        ...
    }
    """
    f_movies = open(movies_file, "r")
    f_rankings = open(rankings_file, "r")

    nbr_movies = sum(1 for _ in f_movies)
    dictionary = {}

    old_user_key = "-1"
    next_index = 1
    for line in f_rankings:
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

    return dictionary


def generate_users_movies_ranking_matrix_with_all_movies_file(matrix, output_file):
    """
    :param matrix: result of generate users movies ranking matrix function
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

def distance(user1, user2):
    difference_absolue_notes = 0
    nombre_films_similaires = 0
    for movie1, note1 in user1.items():
        if(user2.has_key(movie1)):
            difference_absolue_notes += (note1 - user2[movie1]) ** 2
            nombre_films_similaires += 1
    return difference_absolue_notes / nombre_films_similaires

def closest_users(user1, list_users, nb_users):
    closest = -1
    for user in list_users:
        if(user != user1):
            dist = distance(user1, user)
            if(closest < dist):
                closest = dist
    return closest

dictionary = generate_users_movies_ranking_matrix("ml-20m/movies.csv", "ml-20m/ratings.csv")
print(dictionary)

# get the matrix
# matrix = generate_users_movies_ranking_matrix_with_all_movies("ml-20m/movies.csv", "100_first_user_ratings.csv")
# for key in matrix:
#     print(key)
#     print(matrix[key])
#     print()

# save matrix data into file
# generate_users_movies_ranking_matrix_with_all_movies_file(matrix, "users_movies_ranking.csv")
