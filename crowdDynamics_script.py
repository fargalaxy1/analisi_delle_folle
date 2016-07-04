import drawArena_GUI
import crowdDynamics_core

if __name__ == '__main__':
    print("draw!!!\n")
    drawArena_GUI.drawGUI()
    print("end draw\n")
    crowdDynamics_core.crowdDyn_main()
    print("end core")