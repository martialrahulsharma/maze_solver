import cv2
import numpy as np
import threading
import colorsys
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import colorsys


#class definition
class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    
img=None
loc=None
w=0
h=0
rw =2
count = 0
start = Point()
end = Point()
found = False
done_solving=False

dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]
#functions
def BFS(s,e):
    global img, h,w,dir4,found,done_solving
    const = 200
    q = []
    v = [ [0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]

    q.append(s)
    v[s.y][s.x] = 1
    while len(q) > 0:
        p = q.pop(0)
        for d in dir4:
            cell = p + d
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):
                q.append(cell)
                v[cell.y][cell.x] = v[p.y][p.x] + 1
                img[cell.y][cell.x] = list(reversed([i*255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x]/const, 1, 1)]))
                parent[cell.y][cell.x] = p
                if cell == e:
                    found = True
                    del q[:]
                    break

    path = []
    if found:
        p = e
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)
        path.reverse()
        for p in path:
            img[p.y][p.x] = [250,255,250]
        print("path found")
        done_solving=True;
    else:
        print("path not found")
        done_solving=True;

def disp():
    global img,found
    cv2.namedWindow("MouseEvent")
    cv2.imshow("MouseEvent",img)
    cv2.setMouseCallback('MouseEvent', mouse_event)
    while done_solving!=True:
        cv2.imshow('MouseEvent', img)
        cv2.waitKey(1)
    cv2.waitKey(3000)
    if done_solving==True:
        cv2.destroyWindow('MouseEvent')
        
def mouse_event(event, pX, pY, flags, params):
    global img, start, end, count
    if event == cv2.EVENT_LBUTTONUP:
        if count == 0:
            cv2.rectangle(img, (pX-rw, pY-rw), (pX+rw, pY+rw), (0,0,255), -1)
            start = Point(pX, pY)
            print("start = ", start.x, start.y)
            count+=1
        elif count == 1:
            cv2.rectangle(img, (pX-rw, pY-rw), (pX+rw, pY+rw), (0,200,50), -1)
            end = Point(pX, pY)
            print("end = ", end.x, end.y)
            count+=1
            
def mouse_event_handler():
    global start,end,img,loc,h,w
    img=cv2.imread(loc,cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    h, w = img.shape[:2]
    t = threading.Thread(target=disp, args=())
    t.daemon = True
    t.start()
    while count<2:
        pass
    BFS(start, end)
    re_renderTk()

def re_renderTk():
    global img
    imgTk=Image.fromarray(img)
    imgTk = ImageTk.PhotoImage(imgTk)
    imageRender.configure(image=imgTk)
    imageRender.image = imgTk
    


def open_img():
    global loc
    loc = filedialog.askopenfilename()     
    imgTk = Image.open(loc)
    imgTk = ImageTk.PhotoImage(imgTk)
    imageRender.configure(image=imgTk)
    imageRender.image = imgTk


def solveImage():
    global img,loc
    img=cv2.imread(loc,cv2.IMREAD_COLOR)
    cv2.imshow("MouseEvent",img)
    cv2.setMouseCallback('MouseEvent', mouse_event)
 
#variables definition   





    
window=Tk()
window.state('zoomed')
window.title('Maze Solver')
####################### START FROM HERE CODING OF UI #################################
varimage = StringVar()
inputimage = StringVar()


# CREATE FRAMES
MidFrame1 = Frame(window, height=200, width=200, highlightbackground="red", highlightthickness=4)
MidFrame1.pack(side=TOP, fill=X)

RightFrame = Frame(window, height=200, width=200, highlightbackground="black", highlightthickness=4)
RightFrame.pack(side=RIGHT, fill=Y)

LeftFrame = Frame(window, height=200, width=200, highlightbackground="black", highlightthickness=4)
LeftFrame.pack(side=LEFT, fill=Y)

MidFrame = Frame(window, highlightbackground="blue", highlightthickness=4)
MidFrame.pack(side=TOP, fill="both", expand=True)


BottomFrame = Frame(window, height=200, width=200, highlightbackground="black", highlightthickness=4)
BottomFrame.pack(side=BOTTOM, fill=X)


# LABLES
title = Label(MidFrame1, text='MAZE SOLVER', font=("Bold",20))
title.pack()
imageRender = Label(MidFrame, font=("Bold", 20))
imageRender.pack()
imageRender.bind()
solvedImageRender = Label(RightFrame, font=("Bold", 20),text="Right Frame")
solvedImageRender.pack()
solvedImageRender.bind()
# BUTTON
openImageButton = Button(BottomFrame, text='Open Image', command=lambda: open_img())
openImageButton.pack()
submitImageButton = Button(BottomFrame, text='Submit Image', command=lambda: mouse_event_handler())
submitImageButton.pack()

window.mainloop()



# filename = 'C:/Users/avanindkumar/Desktop/large.jpeg'
# img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
# _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
# img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# h, w = img.shape[:2]

# print("select start and end points: ")

# t = threading.Thread(target=disp, args=())
# t.daemon = True
# t.start()

# while p<2:
#     pass

# # BFS(start, end)
# cv2.waitKey(0)

