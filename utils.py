import os
import pickle
import random

def empty_output_directory():
    import os
    path = './output'
    try:
        print("1 \n")
        os.makedirs(path)
        print("2 \n")
    except OSError:
        print("3 \n")
        if not os.path.isdir(path):
            raise

    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def read_inputPersone_File(c_file):
    with open(c_file, "r") as ins:
        content = ins.read().splitlines()
        return content

def read_arenaDimFile(c_file):
    file = open(c_file, "r")
    raw = file.read().splitlines()
    X = raw[0].split()[0]
    Y = raw[0].split()[1]
    return int(X), int(Y)

def read_arenaFile(a_file):
    with open(a_file) as list_1_file:
        content = pickle.load(list_1_file)
    return content

def create_personeFile(p_file, _inputList, _num_exits, xMax, yMax):
    print("_inputList %s \n" % _inputList)
    num_totale = int(_inputList[0])
    num_p_fast = num_totale * int(_inputList[1]) / 100
    num_p_medium = num_totale * int(_inputList[2]) / 100
    num_p_slow = num_totale * int(_inputList[3]) / 100
    print("numTOT = %d, fast = %d, medium = %d, slow = %d \n " %(_num_exits, num_p_fast, num_p_medium, num_p_slow))
    persone_file = open(p_file, 'w')
    for p in range(0, num_p_fast):
        # print_variable = []
        xCoord_p = random.randint(1, xMax-2)
        yCoord_p = random.randint(1, yMax-2)
        vel_p = 3
        target_exit = random.randint(1,_num_exits)
        # target_exit = random.randint(_num_exits+1, 2*_num_exits +1 )

        isOut = 0
        # print_variable += xCoord_p, yCoord_p, vel_p
        persone_file.write(("%d %d %d %d %d\n" %(xCoord_p, yCoord_p, vel_p, target_exit, isOut)))
    for pp in range(0, num_p_medium):
        # print_variable = []
        xCoord_p = random.randint(1, xMax-2)
        yCoord_p = random.randint(1, yMax-2)
        vel_p = 2
        target_exit = random.randint(1,_num_exits)
        isOut = 0
        # print_variable += xCoord_p, yCoord_p, vel_p
        persone_file.write(("%d %d %d %d %d\n" %(xCoord_p, yCoord_p, vel_p, target_exit, isOut)))

    for pi in range(0, num_p_slow):
        # print_variable = []
        xCoord_p = random.randint(1, xMax-2)
        yCoord_p = random.randint(1, yMax-2)
        vel_p = 1
        target_exit = random.randint(1,_num_exits)
        isOut = 0
        # print_variable += xCoord_p, yCoord_p, vel_p
        persone_file.write(("%d %d %d %d %d\n" %(xCoord_p, yCoord_p, vel_p, target_exit, isOut)))


def read_personeFile(c_file):
    with open(c_file, "r") as f:
        raw_persone = f.read().splitlines()
        n_lines_in_file = len(raw_persone)
        persone_def = [0 for x in range(n_lines_in_file)]
        # print("read_personeFile %d \n" %len(persone_def))
        # print n_lines_in_file
        for x in range(0, n_lines_in_file):
            persone_dict = raw_persone[x]
            p_x = persone_dict.split()[0]
            p_y = persone_dict.split()[1]
            p_vel = persone_dict.split()[2]
            p_vel = int(p_vel)
            p_target_exit = persone_dict.split()[3]
            isOut = persone_dict.split()[4]
            persone_def[x] = p_x, p_y, p_vel, p_target_exit, isOut
        return persone_def

def place_persone_in_arena(_arena_type, persone, xmax, ymax):
    n_p = len(persone)
    # print("place_persone_in_arena, n_p = %d \n" %n_p)
    for p in range(0,n_p):
        i = int(persone[p][0])
        j = int(persone[p][1])
        _arena_type[i + xmax*j] = -1
    return _arena_type

def read_exitsFile(e_file):
    with open(e_file, "r") as f:
        raw_exits = f.read().splitlines()
        print("raw_exits %s \n" %raw_exits)
        n_lines_in_file = len(raw_exits)
        exits_a = [0 for x in range(n_lines_in_file)]
        print n_lines_in_file
        for l in range(0, n_lines_in_file):
            exits_dict = raw_exits[l]
            x_0 = exits_dict.split()[0]
            y_0 = exits_dict.split()[1]
            x_1 = exits_dict.split()[2]
            y_1 = exits_dict.split()[3]
            g_x = exits_dict.split()[4]
            g_y = exits_dict.split()[5]

            print("loop exits_dict %s %s %s %s %s %s \n" %(x_0, y_0, x_1, y_1,g_x, g_y))
            exits_a[l] = x_0, y_0, x_1, y_1, g_x, g_y

        return exits_a

def add_target_exits_number(_arena_type, _exits, xmax, ymax):
    n_e = len(_exits)
    # print("add_target_exits_number, n_e = %d \n" % n_e)
    num_exits = len(_exits)

    for nl in range(0, num_exits):
        x0 = int(_exits[nl][0])
        y0 = int(_exits[nl][1])
        x1 = int(_exits[nl][2])
        y1 = int(_exits[nl][3])

    return _arena_type

def mount_video():
    commandString = "ffmpeg -f image2 -r 4 -i output/timestep_%01d.png -vcodec mpeg4 -y output/simulazione.mp4"
    os.system(commandString)

def save_percentage_to_file(_t50, _t90, _t100):
    percentage_file = open('output_percentuali.txt', 'w')
    percentage_file.write(("t50 t90 t100 \n" ))
    percentage_file.write(("%d %d %d \n" % (_t50, _t90, _t100)))