import drawArena_GUI
import crowdDynamics_core
import easygui
if __name__ == '__main__':
    drawArena_GUI.drawGUI()
    # print("end draw\n")
    crowdDynamics_core.crowdDyn_main()
    print("end core")
