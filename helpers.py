def read_dataset(input_filename, output_filename, nbr_of_users):
    """
    :param input_filename: input_file
    :param output_filename: output_file
    :param lines_number: number of line to copy from input_file to output_file

    :return: create output_file which has lines_number copied from input_file
    """
    f = open(input_filename, 'r')
    f_output = open(output_filename, 'w')
    l = []
    i = 0
    for line in f.readlines():
        args = line.split(",")
        if i == 0 or int(args[0]) <= nbr_of_users:
            l.append(line)
            f_output.write(line)
        else:
            break
        i += 1


i = 100
# get 100 first user rating
read_dataset("ml-20m/ratings.csv", str(i) + "_first_user_ratings.csv", i)

i = 500
# get 500 first user rating
read_dataset("ml-20m/ratings.csv", str(i) + "_first_user_ratings.csv", i)

i = 1000
# get 1000 first user rating
read_dataset("ml-20m/ratings.csv", str(i) + "_first_user_ratings.csv", i)
