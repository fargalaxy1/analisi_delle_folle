import math

from utils import read_configFile, build_arena, read_personeFile, place_persone_in_arena, read_arenaFile
from my_tools import print_arena_shape_to_stdout, print_arena_shape_to_file

DEBUG = True

# read config file
config_array = read_configFile("configuration_file.txt")
xMax = int(config_array[ 0 ])
yMax = int(config_array[ 1 ])
tMax = int(config_array[ 2 ])

# build all arena lists
arena_x, arena_y, arena_type, arena_shape = build_arena(xMax, yMax)

# write init arena shape to a file
init_arena_only = open('init_arena_shape.txt', 'w+')
first_line = "Original shape"
print_arena_shape_to_file(xMax, yMax, arena_shape, init_arena_only, first_line)

# read persone file and place each person to the original arena
persone = read_personeFile("persone.txt")
num_persone = len(persone)
if DEBUG:
    print("num_persone: %d \n" %num_persone)
arena_type, arena_shape = place_persone_in_arena(arena_x, arena_y, arena_type, arena_shape, persone, xMax, yMax)
if DEBUG:
    print("arena type %s \n"%arena_type)

# here I replace arena_type[] coming from the old manual method with the GUI one
# in next releases, the arena_shape won't be necessary.
# The whole below code will be re-written based on the new GUI-based input method
arena_type = read_arenaFile("arena.txt")
if DEBUG:
    print("arena type GUI %s \n" %arena_type)

# init the file where all arena+people evolution timesteps will be saved
file_evolution = open('evolution.txt', 'w+')
n_time_step = str(0)
first_line = "Timestep: " + n_time_step
print_arena_shape_to_file(xMax, yMax, arena_shape, file_evolution, first_line)

processed = [ 0 for x in range(num_persone) ]
evacuated = [ 0 for x in range(num_persone) ]
exit_time = [ 0 for x in range(num_persone) ]

counter_horiz = 0
counter_vert = 0

# init evolution
for timestep in range(1, tMax):
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

    percentage_of_evacuated = int(100 * ev/num_persone)
    if DEBUG:
        print("percentage_of_evacuated %d \n" %percentage_of_evacuated)
    if percentage_of_evacuated == 100:
        t100 = timestep
        if DEBUG:
            print("t100 = %d \n" %t100)
    elif percentage_of_evacuated >= 90:
        t90 = timestep
        if DEBUG:
            print("t90 = %d \n" % t90)
    elif percentage_of_evacuated >= 50:
        t50 = timestep
        if DEBUG:
            print("t50 = %d \n" %t50)

    if DEBUG:
        print("percentage %.2f \n" %(100*ev/num_persone))
    if DEBUG:
        print("1 timestep: %d \n" %timestep )
    if DEBUG:
        print("BEFORE Init WHILE on sum<num_persone. Sum: %d \n" % sum_p)

    # if not all actors have been processed then ..
    while(sum_p<num_persone):
        if DEBUG:
            print("Init WHILE on sum<num_persone. Sum: %d \n" % sum_p)
        vel=0
        candidate = 0
        active_p = 0
        mosse = 0

        # here we choose the active persona to be processed in the following
        for active_p in range(0, num_persone):
            vel_p = int(persone[active_p][2])
            # print("processed[%d]= %d, vel_p=%d, evacuated[%d] = %d \n" %(active_p, processed[active_p], vel_p, active_p, evacuated[active_p]))
            if(processed[active_p]==0 and vel_p>vel and evacuated[active_p]==0):
                vel = vel_p
                candidate = active_p
        active_p = candidate
        active_vel_p = int(persone[ active_p ][ 2 ])
        active_target_exit_p = int(persone[ active_p ][ 4 ])
        # print("target exit p %d \n" %active_target_exit_p)

        if DEBUG:
            print("active_p: %d active_vel_p %d \n" %(active_p, active_vel_p))
        if DEBUG:
            print("persone[%d] %s \n" %(active_p, persone[active_p]))
        # once the active persona is chosed, then move it as many times as its velocity
        while mosse < active_vel_p:
            if DEBUG:
                print("Init WHILE on mosse < active_vel_p. Mosse: %d \n" %mosse)

            active_p_x = persone[active_p][0]
            active_p_y = persone[active_p][1]
            candidate_x = -1
            candidate_y = -1
            min_distance = 100000
            # print mosse
            # move active_p in the 8 cells surronding the one it sits on now
            for dx in range(-1,2):
                for dy in range(-1, 2):
                    active_dx = int(active_p_x) + dx
                    active_dy = int(active_p_y) + dy
                    if DEBUG:
                        print("dx: %d dy %d \n" % (dx, dy))
                        print ("active_dx: %d active_dy %d \n" % (active_dx, active_dy))

                    # if the new position (x+dx, y+dy) is inside the arena then
                    if active_dx >= 0 and active_dx < xMax:
                        if active_dy >= 0 and active_dy < yMax:
                            active_p_newx = active_dx
                            active_p_newy = active_dy
                            if DEBUG:
                                print("The new position of p is inside the arena (%d, %d))\n" % (active_p_newx, active_p_newy))
                                print("Is this new pos in a free cell? %d \n"%arena_type[active_p_newx + xMax * active_p_newy])

                            # if the test cell where the active_p has been moved IS NOT an obstacle
                            if arena_type[active_p_newx + xMax * active_p_newy]!= -1:
                                if DEBUG:
                                    print("I'm sitting on a free cell, type %d\n" % arena_type[active_p_newx + xMax * active_p_newy])
                                # loop on each cell of the arena to detect the closest exit from the active cell
                                for i in range(0, yMax):
                                    for j in range(0, xMax):
                                        # print("distance loop (%d, %d) type %d\n" %(i,j, arena_type[ j + yMax * i ]))
                                        # if the arena cell (i,j) is an exit, then ..
                                        if (arena_type[ j + xMax * i ]) == active_target_exit_p and (i!=0 or j!=0):
                                            if DEBUG:
                                                print("USCITA SELEZIONATA %s (i,j) = (%d, %d) \n" %(arena_type[ j + xMax * i ], i, j))
                                            # compute the distance between the active cell (active_p_newx, active_p_newy) and the arena exit cell (i,j)
                                            distance_activep_newcell = math.sqrt(math.pow(i - active_p_newy, 2) + math.pow(j - active_p_newx,2))
                                            if DEBUG:
                                                print("The distance from this exit is: %f \n" %distance_activep_newcell)
                                            # if the distance between the exit and the test cell is smaller then the previous positive distance
                                            # then set the active test cell has the candidate cell to move the persona
                                            if distance_activep_newcell < min_distance:
                                                min_distance = distance_activep_newcell
                                                candidate_x = active_p_newx
                                                candidate_y = active_p_newy
                                                # print("I found distance_activep_newcell %d \n" %distance_activep_newcell)
                                                if DEBUG:
                                                    print("candidate_x %d candidate_y %d\n" %(candidate_x,candidate_y))

                            elif arena_type[active_p_newx + xMax * active_p_newy]== -1 :
                                if DEBUG:
                                    print("I'm sitting on a BUSY cell, type %d\n" % arena_type[active_p_newy + yMax * active_p_newx ])
            if DEBUG:
                print("END OF MOVING %d %d \n "%(candidate_x,candidate_y))
            # candidate_x = 5
            # if the candidate new position is not outside the arena
            if candidate_x != -1:
                # the active person will leave the current cell, so its shape is set to blank space
                arena_shape[int(active_p_x) + xMax * int(active_p_y)] = " "
                arena_type[int(active_p_x) + xMax * int(active_p_y)] = 0
                if DEBUG:
                    print("old position %s %s \n " % (active_p_x, active_p_y))
                    print("old arena shape %s \n " % arena_shape[int(active_p_x) + xMax * int(active_p_y)])

                # NB qui ho trasformato la tupla persone[] in una list per renderla modificabile
                persone[ active_p ] = list(persone[ active_p ])
                persone[ active_p ][0] = candidate_x
                persone[ active_p ][1] = candidate_y
                person_shape = persone[active_p][3]
                if DEBUG:
                    print("persone_shape %s \n" %person_shape)
                # OCCHIO QUI
                if arena_type[candidate_x + xMax * candidate_y] == active_target_exit_p:
                    if candidate_x == 4:
                        counter_horiz += 1
                    elif candidate_x == 0:
                       counter_vert += 1

                    #  if the active person has found an exit, set the cell where it was residing to a blank space
                    arena_shape[candidate_x + xMax * candidate_y] = " "
                # print("La persona %d ha trovato l'uscita al tempo %d \n" %(active_p, timestep))
                    # print("Uscita al tempo %d %d \n" % (candidate_x, candidate_y))
                    exit_time[active_p] = timestep
                    evacuated[active_p] = 1
                    # tb decided a better exit strategy
                    mosse = 100
                else:
                    if DEBUG:
                        print("NOT AN EXIT: %s \n" %arena_type[candidate_x + xMax * candidate_y] )
                    #  if the new cell is not an exit, then the cell is now occupied by the active_p and thus become an obstacle for the others
                    arena_type[ candidate_x + xMax * candidate_y] = -1
                    arena_shape[candidate_x + xMax * candidate_y] = person_shape
                    if DEBUG:
                        print("the active person is %s \n" %arena_shape[candidate_x + xMax * candidate_y])

            mosse +=1

            if mosse >= active_vel_p:
                processed[active_p] = 1
                if DEBUG:
                    print("processed[%d] = %d" %(active_p,processed[active_p]))
                sum_p += 1

    if DEBUG:
        print("EV %d \n" %ev)
    if ev==num_persone:
        if DEBUG:
            print("ENDDDD --- EV >= num_persone %d %d \n" %(ev, num_persone))
            print("timestep %d \n" %(timestep))
        # first_line = "Timestep: " + str(timestep)
        break
    elif ev < num_persone:
        if DEBUG:
            print("GO ON --- EV >= num_persone %d %d \n" %(ev, num_persone))
        first_line = "Timestep: " + str(timestep)

        continue

if DEBUG:
    print("sono appena uscita dal loop temporale \n")
# print("counter_horiz %d \n" % counter_horiz)
# print("counter_vert %d \n" % counter_vert)