import tkinter
canvas=tkinter.Canvas(width=452,height=452,bg="white")
canvas.pack()

number=[0]*81
x=[]
y=[]
xi=[None]*81
yi=[None]*81
n_lines=0
fixed=[]
critical=[]

with open("sudoku1.txt","r") as file:
    for line in file:
        line=line.split(" ")
        n_lines+=1
        x_img=int(line[0])-1
        y_img=int(line[1])-1
        number[x_img*9+y_img]=int(line[2])
        fixed.append(x_img*9+y_img)
        xi[x_img*9+y_img]=x_img
        yi[x_img*9+y_img]=y_img

img=[None]*81

x_yellow,y_yellow=xi,yi

def Images():
    global number,img
    for i in range(len(number)):
        if number[i]!=0:
            img[i]=tkinter.PhotoImage(file=str(number[i])+".png")

for i in range(len(number)):
    if x_yellow[i]!=None:
        canvas.create_rectangle(2+50*x_yellow[i],2+50*y_yellow[i],52+50*x_yellow[i],52+50*y_yellow[i],fill="yellow")

def Draw():
    global number,img
    canvas.delete("card")
    canvas.delete("outline")
    Images()
    for i in range(len(number)):
        if number[i]!=0:
            canvas.create_image(25+50*xi[i],28+50*yi[i],image=img[i],tags="card")

    for i in range(9):
        for j in range(9):
            canvas.create_rectangle(2+50*i,2+50*j,52+50*i,52+50*j,tags="outline")
            x.append(i)
            y.append(j)
            #number.append(0)
    for i in range(3):
        for j in range(3):
            canvas.create_rectangle(2+150*i,2+150*j,152+150*i,152+150*j,width=5,tags="outline")

x_critical=[]
y_critical=[]

def LeftClick(coords):
    global number,xi,yi,fixed,n,critical, win
    win = False
    canvas.delete("highlight")
    x=int(coords.x//50)
    y=int(coords.y//50)
    if not win:
        n=x*9+y
        critical=[]
        CheckRow()
        CheckColumn()
        CheckSquare()
        if n not in fixed:
            number[n]+=1
            if number[n]>9:
                number[n]=1
            xi[n]=int(x)
            yi[n]=int(y)
        Highlight()
        Draw()
        CheckGame()

def RightClick(coords):
    global number,xi,yi,img,win
    win = False
    x=int(coords.x//50)
    y=int(coords.y//50)
    if not win:
        n=x*9+y
        if number[n]>0 and n not in fixed:
            number[n]=0
            xi[n]=None
            yi[n]=None
            img[n]=None
        canvas.delete("highlight")
        Draw()

rows=[]
for i in range(9):
    rows.append([None]*9)

for i in range(9):
    for j in range(9):
        rows[i][j]=i+9*j

def CheckRow():
    global number,n,critical,x_critical,y_critical,rows,fixed
    if n not in fixed:
        row=number[n%9:81:9]
        new_number=number[n]+1
        row_value=[]
        row_place=[]
        if new_number==10:
            new_number=1
        for i in range(9):
            if n in rows[i]:
                row_place=rows[i]
                break
        if row_place!=[]:
            for i in row_place:
                row_value.append(number[i])
        if new_number in row_value:
            c=row_place[row_value.index(new_number)]
            critical.append(c)

proto=[0,1,2,9,10,11,18,19,20]
square_ids=[]

for i in range(9):
    square_ids.append([None]*9)

for i in range(9):
        for j in range(9):
            square_ids[i][j]=proto[j]+3*i+18*(i//3)

def CheckSquare():
    global number,n,critical,square_ids,proto,square_place,square_value,fixed
    if n not in fixed:
        new_number=number[n]+1
        square_value=[]
        square_place=[]
        for i in range(9):
            if n in square_ids[i]:
                square_place=square_ids[i]
        if square_place!=[]:
            for i in square_place:
                square_value.append(number[i])
        if new_number in square_value:
            c=square_place[square_value.index(new_number)]
            critical.append(c)

def CheckColumn():
    global number,n,critical,fixed
    if n not in fixed:
        col=number[n//9*9:n//9*9+9]
        new_number=number[n]+1
        if new_number>9:
            new_number=1
        if new_number in col:
            identical=col.index(new_number)
            critical.append(n//9*9+identical)
        else:
            canvas.delete("highlight")

def Highlight():
    global critical,x,y,x_critical,y_critical
    canvas.delete("highlight")
    for i in critical:               
        canvas.create_rectangle(2+50*x[i],2+50*y[i],52+50*x[i],52+50*y[i],tags="highlight",fill="orange")

win=0

def CheckGame():
    global number,critical,win
    if min(number)!=0 and len(critical)==0:
        canvas.delete("all")
        canvas.create_text(225,225,text="You won!",font="Arial 30")
        win=1


Draw()
canvas.bind("<1>",LeftClick)
canvas.bind("<3>",RightClick)
    
