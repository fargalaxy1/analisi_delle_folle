from utils import read_configFile, read_arenaFile, read_arenaDimFile, create_personeFile, read_personeFile, place_persone_in_arena, read_exitsFile, add_target_exits_number
from tk_utils import draw_arena_init, draw_arena
import math

DEBUG = False

# read config file
config_array = read_configFile("configuration_file.txt")
num_persone = int(config_array[ 0 ])
tMax = int(config_array[ 1 ])
if DEBUG:
    print("read config file %d %d \n" %(num_persone,tMax))

# here I replace arena_type[] coming from the old manual method with the GUI one
arena_type = read_arenaFile("arena.txt")
xmax, ymax = read_arenaDimFile("arena_dim.txt")

# save exits in array
exits = read_exitsFile("exits.txt")
num_exits = len(exits)
if DEBUG:
    print("exits %s %d \n" %(exits, num_exits))

if DEBUG:
    print("xmax = %d, ymax = %d \n" %(xmax,ymax))

# create and read persone file
create_personeFile("persone.txt", num_persone, num_exits, xmax, ymax)
persone = read_personeFile("persone.txt")

if DEBUG:
    print("persone %s \n" %persone)

#place persone in arena
arena_type = place_persone_in_arena(arena_type, persone, xmax, ymax)
if DEBUG:
    print arena_type

# draw initial arena simulation
draw_arena_init(persone, exits, xmax, ymax)

# init lists for dealing with the people processing
processed = [ 0 for x in range(num_persone) ]
evacuated = [ 0 for x in range(num_persone) ]
exit_time = [ 0 for x in range(num_persone) ]

counter_horiz = 0
counter_vert = 0

# init evolution
for timestep in range(1, tMax):

    if DEBUG:
        print("\n")
        print("\n")
        print("------------------------------ init temporal loop %d -----------------------------\n"%timestep)
        print("\n")
        print("\n")
        print("\n")

    ev=0
    sum_p=0
    # init counters used in the timestep loop

    for i, persona in enumerate(persone):
        # print("I'm persona %d and processed %d \n" %(i, processed[i]))
        processed[i] = 0
        sum_p = sum_p + processed[i ] + evacuated[i ]
        # print("I'm persona %d and sum %d evacuated %d \n" %(i, sum_p, evacuated[i]))
        ev += evacuated[i]
        # print("init loop %d ev = %d \n" %(i, ev))
    percentage_of_evacuated = int(100 * ev / num_persone)

    if DEBUG:
        print("percentage_of_evacuated %d \n" % percentage_of_evacuated)
    if percentage_of_evacuated == 100:
        t100 = timestep
        if DEBUG:
            print("t100 = %d \n" % t100)
    elif percentage_of_evacuated >= 90:
        t90 = timestep
        if DEBUG:
            print("t90 = %d \n" % t90)
    elif percentage_of_evacuated >= 50:
        t50 = timestep
        if DEBUG:
            print("t50 = %d \n" % t50)

    if DEBUG:
        print("percentage %.2f \n" % (100 * ev / num_persone))
    if DEBUG:
        print("1 timestep: %d \n" % timestep)
    if DEBUG:
        print("BEFORE Init WHILE on sum<num_persone. Sum: %d \n" % sum_p)

    # if not all actors have been processed then ..
    while (sum_p < num_persone):
        if DEBUG:
            print("\n")
            print("\n")
            print("Init WHILE: Sum: %d \n" % sum_p)
            print("Init WHILE: num_persone: %d \n" % num_persone)
            print("\n")
            print("\n")
        vel = 0
        candidate = 0
        active_p = 0
        mosse = 0

        # here we choose the active persona to be processed in the following
        for active_p in range(0, num_persone):
            vel_p = int(persone[active_p][2])
            # print("processed[%d]= %d, vel_p=%d, evacuated[%d] = %d \n" %(active_p, processed[active_p], vel_p, active_p, evacuated[active_p]))
            if DEBUG:
                print("choose the active persona \n")
                print("active_p %d \n" %active_p)
            if (processed[active_p] == 0 and vel_p > vel and evacuated[active_p] == 0):
                vel = vel_p
                candidate = active_p
                if DEBUG:
                    print("active_p chosen %d \n" %candidate)
        active_p = candidate
        active_vel_p = int(persone[active_p][2])
        active_target_exit_p = int(persone[active_p][3])
        if DEBUG:
            print("active_p %d ---target exit %d \n" %(active_p, active_target_exit_p))

        if DEBUG:
            print("active_p: %d active_vel_p %d \n" % (active_p, active_vel_p))
        if DEBUG:
            print("persone[%d] %s \n" % (active_p, persone[active_p]))
        # once the active persona is chosed, then move it as many times as its velocity
        while mosse < active_vel_p:
            if DEBUG:
                print("\n")
                print("\n")
                print("Init WHILE on mosse: Mosse: %d \n" % mosse)
                print("Init WHILE on mosse: active_vel_p: %d \n" % active_vel_p)
                print("\n")
                print("\n")
            active_p_x = persone[active_p][0]
            active_p_y = persone[active_p][1]
            if DEBUG:
                print("---------------- init loop to move the active p --------------- \n")
            candidate_x = -1
            candidate_y = -1
            min_distance = 100000
            if DEBUG:
                print("Coordinates of active p before moving %s %s \n"%(active_p_x, active_p_y))
            # move active_p in the 8 cells surronding the one it sits on now
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    active_dx = int(active_p_x) + dx
                    active_dy = int(active_p_y) + dy
                    if DEBUG:
                        print("dx: %d dy %d \n" % (dx, dy))
                        print ("active_dx: %d active_dy %d \n" % (active_dx, active_dy))
                        print ("active_dx: %d xmax %d \n" % (active_dx, xmax))
                        print ("active_dy: %d ymax %d \n" % (active_dy, ymax))

                    # if the new position (x+dx, y+dy) is inside the arena then
                    if active_dx >= 0 and active_dx < ymax:
                        if active_dy >= 0 and active_dy < xmax:
                            active_p_newx = active_dx
                            active_p_newy = active_dy
                            if DEBUG:
                                print("The new position of p is inside the arena (%d, %d))\n" % (
                                active_p_newx, active_p_newy))
                            # if the test cell where the active_p has been moved IS NOT an obstacle
                            if arena_type[active_p_newx + xmax * active_p_newy] != -1:
                                if DEBUG:
                                    print("I'm sitting on a free cell, type %d\n" % arena_type[
                                        active_p_newx + xmax * active_p_newy])
                                # loop on each cell of the arena to detect the closest exit from the active cell
                                for i in range(0, ymax):
                                    for j in range(0, xmax):
                                        # print("distance loop (%d, %d) type %d\n" %(i,j, arena_type[ j + ymax * i ]))
                                        # if the arena cell (i,j) is an exit, then ..
                                        if (arena_type[j + xmax * i]) == active_target_exit_p and (i != 0 or j != 0):
                                            if DEBUG:
                                                print("USCITA SELEZIONATA %s (i,j) = (%d, %d) \n" % (
                                                arena_type[j + xmax * i], i, j))
                                            # compute the distance between the active cell (active_p_newx, active_p_newy) and the arena exit cell (i,j)
                                            distance_activep_newcell = math.sqrt(
                                                math.pow(i - active_p_newy, 2) + math.pow(j - active_p_newx, 2))
                                            if DEBUG:
                                                print(
                                                "The distance from this exit is: %f \n" % distance_activep_newcell)
                                            # if the distance between exit and test cell is smaller then the previous distance
                                            # then set the active test cell has the candidate cell to move the persona
                                            if float(distance_activep_newcell) < float(min_distance):
                                                min_distance = distance_activep_newcell
                                                candidate_x = active_p_newx
                                                candidate_y = active_p_newy
                                                if DEBUG:
                                                    print("I found distance_activep_newcell %.2f and I'm %d \n" %(distance_activep_newcell, active_p))
                                                if DEBUG:
                                                    print(
                                                    "candidate_x %d candidate_y %d\n" % (candidate_x, candidate_y))
                            elif arena_type[active_p_newx + xmax * active_p_newy] == -1:
                                if DEBUG:
                                    print("I'm sitting on a BUSY cell, type %d\n" % arena_type[active_p_newx + xmax * active_p_newy])
            if DEBUG:
                print("\n")
                print("\n")
                print("END OF MOVING, the closest position from exit found at %d %d \n "%(candidate_x,candidate_y))
                print("\n")
                print("\n")
            # if the candidate new position is not outside the arena
            if candidate_x != -1:
                if DEBUG:
                    print("candidate_x is not an obstacle %d \n " %(candidate_x))

                # the active person will leave the current cell, so its shape is set to blank space
                arena_type[int(active_p_x) + xmax * int(active_p_y)] = 0
                if DEBUG:
                    print("old position %s %s %d \n " % (active_p_x, active_p_y, active_p))
                    print("Cell left %d \n " %arena_type[int(active_p_x) + xmax * int(active_p_y)])

                # NB qui ho trasformato la tupla persone[] in una list per renderla modificabile
                persone[ active_p ] = list(persone[ active_p ])
                persone[ active_p ][0] = candidate_x
                persone[ active_p ][1] = candidate_y
                if DEBUG:
                    print("\n")
                    print("\n")
                # OCCHIO QUI
                if arena_type[candidate_x + xmax * candidate_y] == active_target_exit_p:
                    if candidate_x == 4:
                        counter_horiz += 1
                    elif candidate_x == 0:
                       counter_vert += 1
                    if DEBUG:
                        print("La persona %d ha trovato l'uscita al tempo %d \n" %(active_p, timestep))
                        print("\n")
                        print("\n")
                    #  if the active person has found an exit, set the cell where it was residing to a blank space
                    arena_type[candidate_x + xmax * candidate_y] = -2
                    persone[active_p][4] = 1
                    # print("La persona %d ha trovato l'uscita al tempo %d \n" %(active_p, timestep))
                    # print("Uscita al tempo %d %d \n" % (candidate_x, candidate_y))
                    exit_time[active_p] = timestep
                    evacuated[active_p] = 1
                    # tb decided a better exit strategy
                    mosse = 100
                else:
                    if DEBUG:
                        print("NOT AN EXIT: %s \n" %arena_type[candidate_x + xmax * candidate_y] )
                        print("\n")
                        print("\n")
                    #  if the new cell is not exit, then become occupied by the active_-> obstacle for the others
                    arena_type[ candidate_x + xmax * candidate_y] = -1

            mosse +=1
            if DEBUG:
                print("End of check if new pos is exit or not")
                print("\n")
                print("\n")

            if mosse >= active_vel_p:
                processed[active_p] = 1
                if DEBUG:
                    print("processed[%d] = %d" %(active_p,processed[active_p]))
                    print("Mosse exausted %d, active_p %d at rest \n" % (mosse, active_p))
                sum_p += 1

    if DEBUG:
        print("\n")
        print("\n")
        print(" WHILE loop on moving p=%d ENDED \n" %active_p)
    if DEBUG:
        print("EV %d \n" %ev)
    if ev==num_persone:
        if DEBUG:
            print("All people has been moved: evolved = %d, num_persone = %d \n" % (ev, num_persone))
            print("EXIT NOW from while loop on all people")
        break
    elif ev < num_persone:
        if DEBUG:
            print("CONTINUE the while loop until all people has been moved \n")
            print("CONTINUE: ev = %d, num_persone = %d \n" %(ev, num_persone))
        draw_arena(persone, exits, xmax, ymax)
        continue


if DEBUG:
    print("sono appena uscita dal loop temporale \n")
