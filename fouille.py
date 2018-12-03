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


def generate_users_movies_ranking_matrix_file(matrix, output_file):
    """
    :param matrix: matrixult of generate users movies ranking matrix function
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


# get the matrix
matrix = generate_users_movies_ranking_matrix("ml-20m/movies.csv", "100_first_user_ratings.csv")
# for key in matrix:
#     print(key)
#     print(matrix[key])
#     print()

# save matrix data into file
generate_users_movies_ranking_matrix_file(matrix, "users_movies_ranking.csv")
