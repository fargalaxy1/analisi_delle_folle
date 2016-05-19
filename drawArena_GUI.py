from Tkinter import *
# TOOLS
LINE, RECTANGLE = list(range(2))

arena_type = []
class Arena:
    def __init__(self, canvas):
        print("Arena().__init__\n")

        self.canvas = canvas
        self._tool, self._obj = None, None
        self.lastx, self.lasty = None, None
        self.upperLeftx, self.upperLefty = None, None
        self.bottomRightx, self.bottomRighty = None, None
        self.arena_type = None
        self.canvas.bind('<Button-1>', self.set_upperLeftCorner)
        self.canvas.bind('<B1-Motion>', self.drawArena)
        self.canvas.bind('<ButtonRelease-1>', self.set_bottomRightCorner)

    def drawArena(self, event):
        # print('Arena().draw() : draw %d %d \n' % (event.x, event.y))
        # print('Arena().draw() : draw %d %d \n' % (event.x, event.y))

        if self._tool is None or self._obj is None:
            return
        x, y = self.lastx, self.lasty
        # print('Arena(): draw %d %d \n' %(event.x, event.y))

        if self._tool in (LINE, RECTANGLE):
            self.canvas.coords(self._obj, (x, y, event.x, event.y))
            # self.bottomRightx, self.bottomRighty = event.x, event.y

    def set_upperLeftCorner(self, event):
        if self._tool is None:
            return
        x, y = event.x, event.y

        if self._tool == LINE:
            root.quit()
            # self._obj = self.canvas.create_line((x, y, x, y))
            # print('Arena(): LINE update_xy %s \n' %(self._tool))
        elif self._tool == RECTANGLE:
            self._obj = self.canvas.create_rectangle((x, y, x, y))
            self.upperLeftx, self.upperLefty = x,y
            # print('Arena(): set_upperLeftCorner - (event.x, event.y) = (%d, %d) \n' %(x,y))

        self.lastx, self.lasty = x, y

    def set_bottomRightCorner(self, event):
        self.bottomRightx, self.bottomRighty = event.x, event.y
        # print self.upperLeftx, self.upperLefty, self.bottomRightx, self.bottomRighty
        self.buildArenaLists(self.upperLeftx, self.upperLefty, self.bottomRightx, self.bottomRighty)

    def buildArenaLists(self, ul_x, ul_y, br_x, br_y):
        print self.upperLeftx, self.upperLefty, self.bottomRightx, self.bottomRighty
        nrows = br_y - ul_y
        ncols = br_x - ul_x
        print("nrows = %d, ncols = %d\n"%(nrows,ncols))
        self.arena_type = [0 for xx in range(nrows*ncols)]
        global arena_type
        arena_type = [0 for xx in range(nrows*ncols)]
        arena_type = self.arena_type

        for i in range(0, nrows):
            for j in range(0, ncols):
                if(i == 0 or i == (nrows -1) or j == 0 or j == (ncols-1)):
                    arena_type[j + i*ncols] = -1
        print("in ARena class, len(arena_type) %s \n" %len(arena_type))

        print("arena_type %s \n" %arena_type)

    def select_tool(self, tool):
        print('Tool', tool)
        self._tool = tool

class Tool:
    def __init__(self, whiteboard, parent=None):
        self.whiteboard = whiteboard
        print("Tool().__init__\n")

        frame = Frame(parent)
        self._curr_tool = None
        for i, (text, t) in enumerate((('L', LINE), ('R', RECTANGLE))):
            # print("i = %d, text = %s, t = %s\n" %(i, text, t))
            lbl = Label(frame, text=text, width=2, relief='raised')
            lbl._tool = t
            lbl.bind('<Button-1>', self.update_tool)
            lbl.pack(padx=6, pady=6*(i % 2))
        frame.pack(side='left', fill='y', expand=True, pady=6)

    def update_tool(self, event):
        print("Tool().update_tool\n")

        lbl = event.widget
        if self._curr_tool:
            self._curr_tool['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        self._curr_tool = lbl
        self.whiteboard.select_tool(lbl._tool)

root = Tk()

canvas = Canvas(highlightbackground='black')
whiteboard = Arena(canvas)
tool = Tool(whiteboard)
canvas.pack(fill='both', expand=True, padx=6, pady=6)

def save_and_quit():
    arena_file = open('arena.txt', 'w+')
    arena_file.write(("%s \n" %(arena_type)))
    # print("arena_ type %s"%arena_type)
    root.destroy()

root.protocol( "WM_DELETE_WINDOW", save_and_quit)

root.mainloop()