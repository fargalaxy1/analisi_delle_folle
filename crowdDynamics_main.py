from utils import read_configFile, read_arenaFile, read_arenaDimFile, create_personeFile, read_personeFile, place_persone_in_arena, read_exitsFile
from tk_utils import draw_arena_init
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

if DEBUG:
    print("xmax = %d, ymax = %d \n" %(xmax,ymax))

# create and read persone file
create_personeFile("persone.txt", num_persone, xmax, ymax)
persone = read_personeFile("persone.txt")

if DEBUG:
    print("persone %s \n" %persone)

#place persone in arena

arena_type = place_persone_in_arena(arena_type, persone, xmax, ymax)
print len(arena_type)
# save exits in array
exits = read_exitsFile("exits.txt")

if DEBUG:
    print("exits %s \n" %exits)

# draw initial arena simulation
draw_arena_init(persone, exits, xmax, ymax)
