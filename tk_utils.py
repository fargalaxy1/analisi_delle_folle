from Tkinter import *
import pickle
from PIL  import Image, ImageDraw, ImageFont

DEBUG = False
timestep = 1

def initConfig_window():
    fields = 'Numero di persone', '% di uomini', '% di donne', '% di disabili'
    def fetch(entries):
        n_fields = 0
        _field_values = [0 for x in range(len(entries))]
        input_file = open('input_values.txt', 'w+')

        for entry in entries:
            _field_values[n_fields]  = entry[1].get()
            n_fields += n_fields
            input_file.write(("%s\n" %(_field_values[n_fields])))

        # print "return and quit \n"

    def makeform(root, fields):
       entries = []
       for field in fields:
          row = Frame(root)
          lab = Label(row, width=15, text=field, anchor='w')
          ent = Entry(row)
          row.pack(side=TOP, fill=X, padx=5, pady=5)
          lab.pack(side=LEFT)
          ent.pack(side=RIGHT, expand=YES, fill=X)
          entries.append((field, ent))
       return entries

    root = Tk()
    ents = makeform(root, fields)

    b1 = Button(root, text='Save', command=(lambda e=ents: fetch(ents)))
    b1.pack(side=LEFT, padx=5, pady=5)
    # b2 = Button(root, text='Quit', command=root.destroy)
    b2 = Button(root, text='Quit', command=root.destroy)
    b2.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()

def draw_arena_init(_persone, _exits,_xmax, _ymax):
    padding = 100
    master = Tk()
    print(" draw_arena_init(): _xmax/height = %d; _ymax/width = %d \n" % (_xmax, _ymax))
    canvas_width = _xmax + padding
    canvas_height = _ymax + padding

    w = Canvas(master,
               width=canvas_width,
               height=canvas_height)
    w.pack()

    traslate = padding / 2
    w.create_rectangle(traslate, traslate, _xmax + traslate, _ymax + traslate, outline="black", width=1)

    num_exits = len(_exits)

    for nl in range(0, num_exits):
        x0 = int(_exits[nl][0]) + traslate
        y0 = int(_exits[nl][1]) + traslate
        x1 = int(_exits[nl][2]) + traslate
        y1 = int(_exits[nl][3]) + traslate

        w.create_line(x0, y0, x1, y1, fill="white", width=1)

    num_persone = len(_persone)
    for nlp in range(0, num_persone):
        xp = int(_persone[nlp][0]) + traslate
        yp = int(_persone[nlp][1]) + traslate
        vel = int(_persone[nlp][2])
        rad = 1
        if (vel == 3):
            # print("man \n")
            w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='blue')
        elif vel == 2:
            # print("woman \n")
            w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='red')
        elif vel == 1:
            # print("disable \n")
            w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='green')
    master.mainloop()


def draw_arena(_persone, _exits,_xmax, _ymax):
    padding = 100
    # master = Tk()
    if DEBUG:
        print(" draw_arena_init(): _xmax/width = %d; _ymax/height = %d \n" %(_xmax, _ymax))
    canvas_width = _xmax + padding
    canvas_height = _ymax + padding
    if DEBUG:
        print(" canvas_width = %d; canvas_height = %d \n" %(canvas_width, canvas_height))

    # PIL create an empty image and draw object to draw on
    # memory only, not visible
    white = (255, 255, 255)

    image1 = Image.new("RGB", (canvas_width, canvas_height), white)
    draw = ImageDraw.Draw(image1)

    traslate = padding/2
    # w.create_rectangle(traslate, traslate, _ymax + traslate, _xmax + traslate, outline="black", width=1)
    draw.rectangle([traslate, traslate, _xmax + traslate, _ymax + traslate], outline="black")

    num_exits = len(_exits)

    for nl in range(0, num_exits):
        x0 = int(_exits[nl][0]) + traslate
        y0 = int(_exits[nl][1]) + traslate
        x1 = int(_exits[nl][2]) + traslate
        y1 = int(_exits[nl][3]) + traslate

        # w.create_line(x0,y0,x1,y1, fill="white", width=1)
        draw.line([x0, y0, x1, y1], white)

    num_persone = len(_persone)
    for nlp in range(0, num_persone):
        xp = int(_persone[nlp][0]) + traslate
        yp = int(_persone[nlp][1]) + traslate
        vel = int(_persone[nlp][2])
        isOut = int(_persone[nlp][4])
        rad = 1
        if isOut == 1:
            # w.create_oval(xp-rad,yp-rad,xp+rad,yp+rad,width=0,fill='white')
            # print("I'm out of the arena %d \n" %(isOut))
            # print("Coords %d %d \n" %(_persone[nlp][0], _persone[nlp][1]))
            draw.point((xp, yp), fill='white')
            _persone[nlp][4] = 2
        elif isOut == 0:
            if(vel == 3):
                #print("man \n")
                # w.create_oval(xp-rad,yp-rad,xp+rad,yp+rad,width=0,fill='blue')
                draw.point((xp, yp), fill='blue')

            elif vel == 2:
                #print("woman \n")
                # w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='red')
                draw.point((xp, yp), fill='red')

            elif vel == 1:
                # print("disable \n")
                # w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='green')
                draw.point((xp, yp), fill='green')

    global timestep

    image2 = image1.resize((canvas_width*3, canvas_height*3))
    filename = "output/timestep_" + str(timestep) +".png"

    # space_bwn_lines = 30
    # legenda_box_x = ((_xmax + traslate)/2)*3
    # legenda_box_y = (_ymax + traslate)*3 + 10
    space_bwn_lines = 30
    legenda_box_x = (traslate)*3
    legenda_box_y = (_ymax + traslate)*3 + 10

    draw2 = ImageDraw.Draw(image2)
    fontTitle = ImageFont.truetype("Arial.ttf", 24)
    font = ImageFont.truetype("Arial.ttf", 22)

    draw2.text((legenda_box_x, legenda_box_y ), "Legenda:", align = 'center', font = fontTitle, fill= 000)
    draw2.text((legenda_box_x, legenda_box_y + space_bwn_lines), "* Uomini", align = 'center', font = font, fill= 'blue')
    draw2.text((legenda_box_x, legenda_box_y + space_bwn_lines*2), "* Donne", align = 'center', font = font, fill= 'red')
    draw2.text((legenda_box_x, legenda_box_y + space_bwn_lines*3), "* Disabili", align = 'center', font = font, fill= 'green')
    image2.save(filename, 'PNG')

    timestep+=1
    return _persone
    # mainloop()

def popupmsg(_t50, _t90, _t100):
    import Tkinter as tk
    import tkMessageBox
    root = tk.Tk()
    root.withdraw()
    print("popupmsg()function 1 \n")

    message = "Il video della simulazione e' stato salvato in output/simulazione.mp4 \n" + "t50 = " + str(_t50) + "\n" + " t90 = " + str(_t90)  +  "\n" +" t100 = " + str(_t100)
    tkMessageBox.showinfo("Simulazione completata", message)

