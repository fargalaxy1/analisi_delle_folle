import sys

def read_configFile(c_file):
    with open(c_file, "r") as ins:

        content = ins.read().splitlines()
        return content

# def build_arena(_xMax, _yMax):
#
#     xmax = int(_xMax)
#     ymax = int(_yMax)
#     arena_x = [0 for x in range(xmax*ymax)]
#     arena_y = [0 for x in range(xmax*ymax)]
#     arena_type = [0 for x in range(xmax*ymax)]
#     arena_shape = [0 for x in range(xmax*ymax)]
#     arena_def = [ 0 for x in range(xmax*ymax) ]
#     for i in range(xmax):
#         for j in range(ymax):
#             # print("build_arena (%d, %d)\n " %(i,j))
#             arena_x[j + ymax * i] = i
#             arena_y[j + ymax * i] = j
#             arena_type[j + ymax * i] = 0
#             arena_shape[j + ymax * i] = 0
#             if (i == 0):
#                 if j<10 or j>13:
#                     arena_shape[j + ymax * i] = "-"
#                     arena_type[j + ymax * i] = -1
#                     sys.stdout.write("-")
#                 else:
#                     arena_shape[j + ymax * i] = " "
#                     arena_type[j + ymax * i] = 1
#                     sys.stdout.write(" ")
#             elif i==(xmax-1):
#                 arena_shape[j + ymax * i] = "-"
#                 arena_type[j + ymax * i] = -1
#                 sys.stdout.write("-")
#             elif j==0:
#                 if i<10 or i>13:
#                     arena_shape[ j + ymax * i ] = "|"
#                     arena_type[ j + ymax * i ] = -1
#                     sys.stdout.write("|")
#                 else:
#                     arena_shape[j + ymax * i] = " "
#                     arena_type[j + ymax * i] = 1
#                     sys.stdout.write(" ")
#             elif j==ymax-1:
#                 arena_shape[j + ymax * i] = "|"
#                 arena_type[j + ymax * i] = -1
#                 sys.stdout.write("|")
#             else:
#                 arena_shape[j + ymax * i] = " "
#                 sys.stdout.write(" ")
#         print("\r")
#     return arena_x, arena_y, arena_type, arena_shape

def build_arena(_xMax, _yMax):

    # xmax numero massimo di colonne
    # ymax numero massimo di righe
    xmax = int(_xMax)
    ymax = int(_yMax)
    arena_x = [0 for xx in range(xmax*ymax)]
    arena_y = [0 for xx in range(xmax*ymax)]
    arena_type = [0 for xx in range(xmax*ymax)]
    arena_shape = [0 for xx in range(xmax*ymax)]
    # print("xmax = %d , ymax = %d \n"%(xmax,ymax))

    for i in range(0, ymax):
        for j in range(0, xmax):
            # print("--------------\n")
            # print("build_arena (%d, %d)\n " %(i,j))
            # print("j + ymax * i = %d\n " %(j + xmax * i))
            # arena_x[j + xmax * i] = j
            arena_y[j + xmax * i] = i
            arena_type[j + xmax * i] = 0
            arena_shape[j + xmax * i] = 0

            if (i == 0):
                if j<4 or j>4:
                    arena_shape[j + xmax * i] = "-"
                    arena_type[j + xmax * i] = -1
                    sys.stdout.write("-")
                else:
                    arena_shape[j + xmax * i] = " "
                    arena_type[j + xmax * i] = 2
                    sys.stdout.write(" ")
            elif i == (ymax-1):
                arena_shape[j + xmax * i] = "-"
                arena_type[j + xmax * i] = -1
                sys.stdout.write("-")
            elif j == 0:
                if i<4 or i>4:
                    arena_shape[ j + xmax * i ] = "|"
                    arena_type[ j + xmax * i ] = -1
                    sys.stdout.write("|")
                else:
                    arena_shape[j + xmax * i] = " "
                    arena_type[j + xmax * i] = 1
                    sys.stdout.write(" ")
            elif j==xmax-1:
                arena_shape[j + xmax * i] = "|"
                arena_type[j + xmax * i] = -1
                sys.stdout.write("|")
            else:
                arena_shape[j + xmax * i] = " "
                sys.stdout.write(" ")
        print("\r")
    return arena_x, arena_y, arena_type, arena_shape

def read_personeFile(c_file):
    with open(c_file, "r") as f:
        raw_persone = f.read().splitlines()
        n_lines_in_file = len(raw_persone)
        persone_dict = {}
        persone_def = [0 for x in range(n_lines_in_file-1)]
        # print n_lines_in_file
        for x in range(0, n_lines_in_file):
            persone_dict = raw_persone[x]
            p_x = persone_dict.split()[0]
            p_y = persone_dict.split()[1]
            p_vel = persone_dict.split()[2]
            p_vel = int(p_vel)
            p_target_exit = persone_dict.split()[3]
            p_shape = " "
            if p_vel ==1:
                p_shape = "d"
            elif p_vel == 2:
                p_shape = "f"
            elif p_vel == 3:
                p_shape = "m"
            else:
                print("ATTENTION, one person has not velocity ")
            # print p_shape
            persone_def[x-1] = p_x, p_y, p_vel, p_shape, p_target_exit
        return persone_def

def place_persone_in_arena(_arena_x, _arena_y, _arena_type, _arena_shape, persone, xmax, ymax):
    n_p = len(persone)
    # print("place_persone_in_arena, n_p = %d \n" %n_p)
    for p in range(0,n_p):
        i = int(persone[p][1])
        j = int(persone[p][0])
        vel = int(persone[p][2])
        # print("person p = %d %s \n"%(p, persone[p]))
        if(vel == 1):
            _arena_shape[j + xmax * i] = "d"
        elif(vel == 2):
            _arena_shape[j + xmax * i] = "f"
        elif(vel == 3):
            _arena_shape[j + xmax * i] = "m"
        _arena_type[j + xmax*i] = -1
    return _arena_type, _arena_shape


