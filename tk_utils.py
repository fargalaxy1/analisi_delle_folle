from Tkinter import *
from PIL  import Image, ImageDraw
DEBUG = False

timestep = 0

def draw_arena_init(_persone, _exits,_xmax, _ymax):
    padding = 100
    master = Tk()
    if DEBUG:
        print(" draw_arena_init(): _xmax/height = %d; _ymax/width = %d \n" %(_xmax, _ymax))
    canvas_width = _xmax + padding
    canvas_height = _ymax + padding
    if DEBUG:
        print(" canvas_width = %d; canvas_height = %d \n" %(canvas_width, canvas_height))

    w = Canvas(master,
               width=canvas_height,
               height=canvas_width)
    w.pack()

    # PIL create an empty image and draw object to draw on
    # memory only, not visible
    white = (255, 255, 255)

    image1 = Image.new("RGB", (canvas_height, canvas_width), white)
    draw = ImageDraw.Draw(image1)

    traslate = padding/2
    w.create_rectangle(traslate, traslate, _ymax + traslate, _xmax + traslate, outline="black", width=1)
    draw.rectangle([traslate, traslate, _ymax + traslate, _xmax + traslate], outline="black")

    num_exits = len(_exits)

    for nl in range(0, num_exits):
        x0 = int(_exits[nl][0]) + traslate
        y0 = int(_exits[nl][1]) + traslate
        x1 = int(_exits[nl][2]) + traslate
        y1 = int(_exits[nl][3]) + traslate

        w.create_line(x0,y0,x1,y1, fill="white", width=1)
        # print("create_line %d \n", nl)
        # do the PIL image/draw (in memory) drawings
        draw.line([x0,y0,x1,y1], white)

    num_persone = len(_persone)
    for nlp in range(0, num_persone):
        xp = int(_persone[nlp][0]) + traslate
        yp = int(_persone[nlp][1]) + traslate
        vel = int(_persone[nlp][2])
        rad = 1

        if(vel == 3):
            #print("man \n")
            w.create_oval(xp-rad,yp-rad,xp+rad,yp+rad,width=0,fill='blue')
            draw.point((xp, yp), fill='blue')

        elif vel == 2:
            #print("woman \n")
            w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='red')
            draw.point((xp, yp) , fill='red')

        elif vel == 1:
            # print("disable \n")
            w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='green')
            draw.point((xp, yp), fill='green')

    # PIL image can be saved as .png .jpg .gif or .bmp file (among others)
    filename = "output/init.jpg"
    quality_val = 100

    image1.save(filename, 'JPEG', quality=quality_val)
    mainloop()


def draw_arena(_persone, _exits,_xmax, _ymax):
    padding = 100
    master = Tk()
    if DEBUG:
        print(" draw_arena_init(): _xmax/height = %d; _ymax/width = %d \n" %(_xmax, _ymax))
    canvas_width = _xmax + padding
    canvas_height = _ymax + padding
    if DEBUG:
        print(" canvas_width = %d; canvas_height = %d \n" %(canvas_width, canvas_height))

    w = Canvas(master,
               width=canvas_height,
               height=canvas_width)
    w.pack()

    # PIL create an empty image and draw object to draw on
    # memory only, not visible
    white = (255, 255, 255)

    image1 = Image.new("RGB", (canvas_height, canvas_width), white)
    draw = ImageDraw.Draw(image1)

    traslate = padding/2
    w.create_rectangle(traslate, traslate, _ymax + traslate, _xmax + traslate, outline="black", width=1)
    draw.rectangle([traslate, traslate, _ymax + traslate, _xmax + traslate], outline="black")

    num_exits = len(_exits)

    for nl in range(0, num_exits):
        x0 = int(_exits[nl][0]) + traslate
        y0 = int(_exits[nl][1]) + traslate
        x1 = int(_exits[nl][2]) + traslate
        y1 = int(_exits[nl][3]) + traslate

        w.create_line(x0,y0,x1,y1, fill="white", width=1)
        draw.line([x0, y0, x1, y1], white)

    num_persone = len(_persone)
    for nlp in range(0, num_persone):
        xp = int(_persone[nlp][0]) + traslate
        yp = int(_persone[nlp][1]) + traslate
        vel = int(_persone[nlp][2])
        isOut = int(_persone[nlp][4])
        rad = 1
        if isOut:
            w.create_oval(xp-rad,yp-rad,xp+rad,yp+rad,width=0,fill='white')
            draw.point((xp, yp), fill='white')
        else:
            if(vel == 3):
                #print("man \n")
                w.create_oval(xp-rad,yp-rad,xp+rad,yp+rad,width=0,fill='blue')
                draw.point((xp, yp), fill='blue')

            elif vel == 2:
                #print("woman \n")
                w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='red')
                draw.point((xp, yp), fill='red')

            elif vel == 1:
                # print("disable \n")
                w.create_oval(xp - rad, yp - rad, xp + rad, yp + rad, width=0, fill='green')
                draw.point((xp, yp), fill='green')

    global timestep
    timestep+=1

    filename = "output/timestep_" + str(timestep) +".jpg"
    quality_val = 100

    image1.save(filename, 'JPEG', quality=quality_val)
    mainloop()
