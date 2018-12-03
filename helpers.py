def read_dataset(input_filename, output_filename, lines_number):
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
        if i < lines_number:
            l.append(line)
            f_output.write(line)
        i += 1


# get 100 first user rating
read_dataset("ml-20m/ratings.csv", "100_first_user_ratings.csv", 11102)
