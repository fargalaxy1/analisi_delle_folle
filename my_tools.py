

def print_arena_shape_to_stdout(xMax, yMax, _arena_shape):
    for i in range(0, xMax):
        temp_variable = ' '
        for j in range(0, yMax):
            temp_variable += _arena_shape[ j + i*yMax]
        print temp_variable

def print_arena_shape_to_file(xMax, yMax, _arena_shape, file, first_line):
    file.write(str(first_line) + "\n")
    for i in range(0, yMax):
        temp_variable = ' '
        for j in range(0, xMax):
            temp_variable += _arena_shape[j + i*xMax]
        file.write(temp_variable+ "\n")

