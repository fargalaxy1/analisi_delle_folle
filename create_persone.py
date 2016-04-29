import random
import sys
print 'We are creating %d persone :\n', int(sys.argv[1])
number_of_people = int(sys.argv[1])
xMax = int(sys.argv[2])
yMax = int(sys.argv[3])

persone_file = open('persone.txt', 'w+')
# random.randint(1, 10)

for p in range(0, number_of_people):
    # print_variable = []
    xCoord_p = random.randint(1, xMax-2)
    yCoord_p = random.randint(1, yMax-2)
    vel_p = random.randint(1,3)
    target_exit = random.randint(1,2)
    # print_variable += xCoord_p, yCoord_p, vel_p
    persone_file.write(("%d %d %d %d \n" %(xCoord_p, yCoord_p, vel_p, target_exit)))