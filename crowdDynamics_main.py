from utils import read_configFile, read_arenaFile, read_arenaDimFile, create_personeFile, read_personeFile

DEBUG = True

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

