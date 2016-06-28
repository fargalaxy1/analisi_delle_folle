from Tkinter import *
import tkMessageBox
import pickle
# TOOLS
LINE, RECTANGLE = list(range(2))
arena_type = []
xmax, ymax = 0,0
g_exits_file = None
DEBUG = True

class Arena:
    def __init__(self, canvas):
        if DEBUG:
            print("Arena().__init__\n")

        self.canvas = canvas
        self._tool, self._obj = None, None
        self.lastx, self.lasty = None, None
        self.upperLeftx, self.upperLefty = None, None
        self.bottomRightx, self.bottomRighty = None, None
        self.initLinex,self.initLiney = None, None
        self.endLinex,self.endLiney = None, None
        self.arena_type = None
        self.nrows_a, self.ncols_a = 0, 0
        self.exits_file = None
        self.exit_target_number = 1
        self.canvas.bind('<Button-1>', self.dealWithButtonInit)
        self.canvas.bind('<B1-Motion>', self.drawArena)
        self.canvas.bind('<ButtonRelease-1>', self.dealWithButtonEnd)

    def dealWithButtonInit(self, event):
        if self._tool is None:
            print("self.tool is NONE \n")
            return
        x, y = event.x, event.y
        if DEBUG:
            print('dealWithButtonInit x=%d, y=%d \n'%(x,y))

        if self._tool == LINE:
            if DEBUG:
                print('dealWithButtonInit: lINE \n')

            if not self.arena_type:
                if DEBUG:
                    print('MESSAGE: _tool() %s \n' %self._tool)
                tkMessageBox.showwarning("Errore", "Bisogna prima disegnare l'arena - premi R")
            else:
                if DEBUG:
                    print('NOT MESSAGE \n')
                self.set_exits(event)
        elif self._tool == RECTANGLE:
            if DEBUG:
                print('dealWithButtonInit: RECTANGLE \n')
            self.set_upperLeftCorner(event)

        self.lastx, self.lasty = x, y

    def set_exits(self, event):
        x, y = event.x, event.y

        self.initLinex, self.initLiney = event.x, event.y
        self._obj = self.canvas.create_line((x, y, x, y))
        self.canvas.itemconfig(self._obj, fill = "Red")

        if DEBUG:
            print('Arena(): set_exits %d %d \n' % (x, y))

    def set_upperLeftCorner(self, event):
        x, y = event.x, event.y
        self.upperLeftx, self.upperLefty = x, y
        self._obj = self.canvas.create_rectangle((x, y, x, y))
        self.upperLeftx, self.upperLefty = x, y
        if DEBUG:
            print('Arena(): set_upperLeftCorner - (event.x, event.y) = (%d, %d) \n' %(x,y))

    def drawArena(self, event):
        # print('Arena().draw() : draw %d %d \n' % (event.x, event.y))

        if self._tool is None or self._obj is None:
            return
        x, y = self.lastx, self.lasty
        # print('Arena(): draw %d %d \n' %(event.x, event.y))

        if self._tool in (LINE, RECTANGLE):
            self.canvas.coords(self._obj, (x, y, event.x, event.y))

    def dealWithButtonEnd(self, event):
        # if DEBUG:
        #     print("end line %d %d" % (self.endLinex, self.endLiney))
        if self._tool == LINE:
            self.endLinex = event.x
            self.endLiney = event.y
            self.addExitToArena()
        elif self._tool == RECTANGLE:
            self.bottomRightx, self.bottomRighty = event.x, event.y
            self.buildArenaLists(self.upperLeftx, self.upperLefty, self.bottomRightx, self.bottomRighty)
            self._tool = None

    def set_bottomRightCorner(self, event):
        self.bottomRightx, self.bottomRighty = event.x, event.y
        # print self.upperLeftx, self.upperLefty, self.bottomRightx, self.bottomRighty
        self.buildArenaLists(self.upperLeftx, self.upperLefty, self.bottomRightx, self.bottomRighty)

    def buildArenaLists(self, ul_x, ul_y, br_x, br_y):
        if DEBUG:
            print self.upperLeftx, self.upperLefty, self.bottomRightx, self.bottomRighty
        nrows = br_y - ul_y
        ncols = br_x - ul_x
        global xmax
        global  ymax
        xmax = ncols
        ymax = nrows
        if DEBUG:
            print("nrows = %d, ncols = %d\n"%(nrows, ncols))
        # self.arena_type = [0 for xx in range(nrows*ncols)]
        global arena_type
        arena_type = [0 for gg in range(nrows*ncols+1)]
        self.arena_type = arena_type

        for i in range(0, ncols):
            for j in range(0, nrows):
                if(i == 0 or i == (ncols -1) or j == 0 or j == (nrows-1)):
                    print('buildArenaLists/arena_type %d %d --- %d %d \n'%(i,j, nrows, ncols))
                    arena_type[i + j*ncols] = -1
        if DEBUG:
            print("in Arena class, len(arena_type) %s \n" %len(arena_type))

        if DEBUG:
            print("arena_type %s \n" %arena_type)
        self.arena_type = arena_type
        self.nrows_a = int(nrows)
        self.ncols_a = int(ncols)
        print("nrows %d ncols %d \n" %(self.nrows_a, self.ncols_a))

    def select_tool(self, tool):
        if DEBUG:
            print('Tool def', tool)
        self._tool = tool

    def addExitToArena(self):
        diffX = self.endLinex - self.initLinex
        diffY = self.endLiney - self.initLiney
        print("addExitToArena %d %d \n" %(diffX, diffY))
        southExit, northExit = False, False
        eastExit, westExit = False, False
        global g_exits_file
        g_exits_file = open("exits.txt", "a")
        _exits_file = g_exits_file
        if diffX > diffY:
            print("horizonthal side %d \n" % (self.initLiney - self.upperLefty))

            exit_x_0 = self.initLinex - self.upperLeftx
            exit_x_1 = self.endLinex - self.upperLeftx

            print("initX %d initY %d\n " %(self.initLinex, self.endLinex))
            print("exit0 %d exit_1 %d\n " %(exit_x_0, exit_x_1))

            if self.initLiney - self.upperLefty > (self.nrows_a/2):
                print("south EXIT \n")
                southExit = True
                y_all = self.nrows_a
                self.updateArenaList("S", exit_x_0, exit_x_1)
                # _exits_file.write(("%s %d %d \n" % ("S", exit_0, exit_1)))
                _exits_file.write(("%d %d %d %d \n" % (exit_x_0, y_all, exit_x_1, y_all)))
            else:
                print("north EXIT \n")
                northExit = True
                y_all = 0
                self.updateArenaList("N", exit_x_0, exit_x_1 )
                #_exits_file.write(("%s %d %d \n" % ("N", exit_x_0, exit_x_1)))
                _exits_file.write(("%d %d %d %d\n" % (exit_x_0, y_all, exit_x_1, y_all)))
        else:
            print("vertical side  %d \n" % (self.initLinex - self.upperLeftx))

            exit_y_0 = self.initLiney - self.upperLefty
            exit_y_1 = self.endLiney - self.upperLefty

            if self.initLinex - self.upperLeftx > (self.ncols_a / 2):
                print("East EXIT \n")
                eastExit = True
                x_all = self.ncols_a
                self.updateArenaList("E", exit_y_0, exit_y_1)
                _exits_file.write(("%d %d %d %d \n" % (x_all, exit_y_0, x_all, exit_y_1)))
            else:
                print("West EXIT \n")
                westExit = True
                x_all = 0
                self.updateArenaList("W", exit_y_0, exit_y_1)
                # _exits_file.write(("%s %d %d \n" % ("W", exit_0, exit_1)))
                _exits_file.write(("%d %d %d %d \n" % (x_all, exit_y_0, x_all, exit_y_1)))

    def updateArenaList(self, position_flag, _exit_0, _exit_1):
        if(position_flag == "N"):
            print("sono a nord %d %d \n" %(_exit_0, _exit_1))
            for i in range(_exit_0, _exit_1 + 1):
                self.arena_type[i] = self.exit_target_number
            print(" exit_target_num %d \n" %self.exit_target_number)
            self.exit_target_number +=1
        elif(position_flag == "S"):
            print("sono a sud %d %d \n" %(_exit_0, _exit_1))
            for i in range(_exit_0, _exit_1 + 1):
                self.arena_type[(self.nrows_a - 1) * self.ncols_a + i] = self.exit_target_number
            print(" exit_target_num %d \n" %self.exit_target_number)
            self.exit_target_number +=1
        elif(position_flag == "E"):
            print("sono a est %d %d \n" %(_exit_0, _exit_1))
            for j in range(_exit_0, _exit_1):
                self.arena_type[(self.ncols_a ) * j + self.ncols_a -1] = self.exit_target_number
                print("j %d arena %s index %d \n" %(j, self.arena_type[(self.ncols_a -1 ) * j + self.ncols_a], (self.ncols_a -1 ) * j + self.ncols_a))
            print(" exit_target_num %d \n" %self.exit_target_number)
            self.exit_target_number += 1
        elif(position_flag == "W"):
            for j in range(_exit_0, _exit_1 + 1):
                self.arena_type[(self.ncols_a) * j] = self.exit_target_number
            print(" exit_target_num %d \n" %self.exit_target_number)
            self.exit_target_number += 1
        # print("arena_type %s \n" %self.arena_type)

class Tool:
    def __init__(self, whiteboard, parent=None):
        self.whiteboard = whiteboard
        self._lbl_L = None
        self._lbl_R = None
        self._activeL = False
        self._activeR = False
        print("Tool().__init__\n")

        frame = Frame(parent)
        self._curr_tool = None

        for i, (text, t) in enumerate((('L', LINE), ('R', RECTANGLE))):
            # print("i = %d, text = %s, t = %s\n" %(i, text, t))
            lbl = Label(frame, text=text, width=2, relief='raised')
            if not t:
                # if the line tool is the one that is being initialized - t = 0
                # find another way
                self._lbl_L = lbl
            else:
                self._lbl_R = lbl
            lbl._tool = t
            if DEBUG:
                print("lbl._tool %s \n"%t)
            lbl.bind('<Button-1>', self.update_tool)
            lbl.pack(padx=6, pady=6*(i % 2))

        frame.pack(side='left', fill='y', expand=True, pady=6)

    def update_tool(self, event):
        if DEBUG:
            print("Tool().update_tool\n")
        lbl = event.widget
        if DEBUG:
            print("lbl tool %s \n" %lbl._tool)
            print("_curr_tool %s \n" % self._curr_tool)

        if self._curr_tool:
            if DEBUG:
                print("1: a tool is already initiated")
            if lbl._tool:
                if DEBUG:
                    print("1.b: tool R to be raised")
                lbl['relief'] = 'sunken'
                if self._activeL:
                    if DEBUG:
                        print("1.c: tool L to be raised")
                    self._lbl_L['relief'] = 'raised'
                    self._activeL = False
                if self._activeR:
                    if DEBUG:
                        print("1.d: tool R again")
                    self._lbl_R['relief'] = 'raised'
                    self._activeR = False
                    self._curr_tool = None
                    self.whiteboard.select_tool(None)
                else:
                    self._activeR = True
                    self._curr_tool = lbl
                    self.whiteboard.select_tool(lbl._tool)
            else:
                if DEBUG:
                    print("1.e: tool LINE to be raised")
                lbl['relief'] = 'sunken'
                if self._activeR:
                    if DEBUG:
                        print("1.f: tool R to be raised")
                    self._lbl_R['relief'] = 'raised'
                    self._activeR = False
                if self._activeL:
                    if DEBUG:
                        print("1.g: tool L again")
                    self._lbl_L['relief'] = 'raised'
                    self._activeL = False
                    self._curr_tool = None
                    self.whiteboard.select_tool(None)
                else:
                    self._activeL = True
                    self._curr_tool = lbl
                    self.whiteboard.select_tool(lbl._tool)
        else:
            if DEBUG:
                print("2: no tool already active")
                print("2.0: tool %s active \n" %lbl._tool)

            lbl['relief'] = 'sunken'
            self._curr_tool = lbl
            self.whiteboard.select_tool(lbl._tool)

            if lbl._tool:
                if DEBUG:
                    print("2.d: R activaTED")
                self._activeR = True
            else:
                if DEBUG:
                    print("2.e: L activaTED")
                self._activeL = True

root = Tk()

canvas = Canvas(highlightbackground='black', height=500, width=700)
whiteboard = Arena(canvas)
tool = Tool(whiteboard)
canvas.pack(fill='both', expand=True, padx=6, pady=6)

g_exits_file = open("exits.txt", "w")

def save_and_quit():
    # arena_file = open('arena.txt', 'w+')
    with open('arena.txt', 'wb') as arena_file:
        pickle.dump(arena_type, arena_file)
    arena_dim = open('arena_dim.txt', 'w+')
    arena_dim.write(("%d %d \n" %(xmax, ymax)))
    # g_exits_file.flush()
    # g_exits_file.close()
    root.destroy()

root.protocol( "WM_DELETE_WINDOW", save_and_quit)

root.mainloop()