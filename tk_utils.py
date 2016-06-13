from Tkinter import *

# master = Tk()
#
# w = Canvas(master, width=200, height=100)
# w.pack()
#
# w.create_line(0, 0, 200, 100)
# w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
#
# w.create_rectangle(50, 25, 150, 75, fill="blue")
#
# mainloop()

def draw_arena_init(_persone, _exits,_xmax, _ymax):
    padding = 100
    master = Tk()
    print(" draw_arena_init(): _xmax/height = %d; _ymax/width = %d \n" %(_xmax, _ymax))
    canvas_width = _xmax + padding
    canvas_height = _ymax + padding
    print(" canvas_width = %d; canvas_height = %d \n" %(canvas_width, canvas_height))

    w = Canvas(master,
               width=canvas_height,
               height=canvas_width)
    w.pack()

    traslate = padding/2
    w.create_rectangle(traslate, traslate, _ymax + traslate, _xmax + traslate, outline="black", width=1)

    num_exits = len(_exits)

    for nl in range(0, num_exits):
        x0 = int(_exits[nl][0]) + traslate
        y0 = int(_exits[nl][1]) + traslate
        x1 = int(_exits[nl][2]) + traslate
        y1 = int(_exits[nl][3]) + traslate

        w.create_line(x0,y0,x1,y1, fill="white", width=1)

    num_persone = len(_persone)
    for nlp in range(0, num_persone):
        xp = int(_persone[nlp][0]) + traslate
        yp = int(_persone[nlp][1]) + traslate
        vel = int(_persone[nlp][2])
        rad = 1
        if(vel == 3):
            #print("man \n")
            w.create_oval(xp-rad,yp-rad,xp+rad,yp+rad,width=0,fill='blue')
        elif vel == 2:
            #print("woman \n")
            w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='red')
        elif vel == 1:
            # print("disable \n")
            w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='green')
    mainloop()

