from tkinter import *
from tkinter import messagebox

root = Tk()
clicked = False
count = 0
rec_count=0

grid=[[0,0,0],[0,0,0],[0,0,0]]# Magic square
board=[[0,0,0],[0,0,0],[0,0,0]]# Board positions
X_list=[]# Positions where X plays
O_list=[]# Positions where O plays
target=0
#helper function for magic square generation
def poss(x):
    global grid
    for i in range(3):
        for j in range(3):
            #checks repetition in grid
            if grid[j][i]==x:
                return False
    return True
#helper function for magic square generation
def check():
    global grid
    if grid[0][0]+grid[0][1]+grid[0][2]==15:
        if grid[1][0]+grid[1][1]+grid[1][2]==15:
            if grid[2][0]+grid[2][1]+grid[2][2]==15:
                if grid[0][0]+grid[1][0]+grid[2][0]==15:
                    if grid[0][1]+grid[1][1]+grid[2][1]==15:
                        if grid[0][2]+grid[1][2]+grid[2][2]==15:
                            if grid[0][0]+grid[1][1]+grid[2][2]==15:
                                if grid[2][0]+grid[1][1]+grid[0][2]==15:
                                    return True
    #check if magic square properties are satisfied
    return False
#function for magic square generation
def gen():
    #check for empty space in square
    for y in range(3):
        for x in range(3):
            if grid[y][x]==0:
                for n in range(1,10):# try all numbers
                    if poss(n):
                        grid[y][x]=n                        
                        gen()#backtracking using recursion
                    if not check():
                        grid[y][x]=0#reset if magic square property not satisfied
                        
                return   
gen()
print(grid)
def choose_target():
    global target
    diff=0
    for i in range(0,len(X_list)):
        for j in range(0,len(X_list)):
            if(i!=j):
                diff=15-(X_list[i]+X_list[j])
            if diff>9 or diff<=0:
                continue
            elif diff==target:
                continue
            else:
                target=diff#logic as explained in ppt
                break
# disable all the buttons
def disable_all_buttons():
    b1.config(state=DISABLED)
    b2.config(state=DISABLED)
    b3.config(state=DISABLED)
    b4.config(state=DISABLED)
    b5.config(state=DISABLED)
    b6.config(state=DISABLED)
    b7.config(state=DISABLED)
    b8.config(state=DISABLED)
    b9.config(state=DISABLED)
# Check to see if someone won
def checkifwon():
    global winner, X_list, O_list
    winner = False
    for i in range(len(X_list)):
        for j in range(i):
            for k in range(i):
                if(i!=j and i!=k and j!=k):
                    try:
                        if X_list[i]+X_list[j]+X_list[k]==15:
                            messagebox.showinfo("Tic Tac Toe", "X Wins!")
                            disable_all_buttons()
                            winner=True
                            pass
                            break

                        
                    
                        elif O_list[i]+O_list[j]+O_list[k]==15:
                            messagebox.showinfo("Tic Tac Toe", "O Wins!")
                            disable_all_buttons()
                            winner=True
                            pass
                            break
                        
                    
                    except:
                        pass
    if count == 9 and winner == False:
        messagebox.showinfo("Tic Tac Toe", "It's A Tie!\n No One Wins!")
        disable_all_buttons()
#update board positions
def update():
    global board
    for i in range(len(X_list)):
        for j in range(3):
            for k in range(3):
                if X_list[i]==grid[j][k]:
                    board[j][k]=1
    for i in range(len(O_list)):
        for j in range(3):
            for k in range(3):
                if O_list[i]==grid[j][k]:
                    board[j][k]=2
#calculates AI's next move
def ai():
    global rec_count
    rec_count+=1
    if count==0 or count==1:
        if b5["text"]==grid[1][1]:
            b_click(b5) 
        else:
            b_click(b6)#takes middle square if available, else takes square to right of middle
    elif rec_count<5:
        choose_target()
        move()
    else:
        if b1["text"]!='X' and b1["text"]!='O':
            b_click(b1)
        elif b2["text"]!='X' and b2["text"]!='O':
            b_click(b2)
        elif b3["text"]!='X' and b3["text"]!='O':
            b_click(b3)
        elif b4["text"]!='X' and b4["text"]!='O':
            b_click(b4)
        elif b5["text"]!='X' and b5["text"]!='O':
            b_click(b5)
        elif b6["text"]!='X' and b6["text"]!='O':
            b_click(b6)
        elif b7["text"]!='X' and b7["text"]!='O':
            b_click(b7)
        elif b8["text"]!='X' and b8["text"]!='O':
            b_click(b8)
        else:
            b_click(b9)
        
def move():
    global grid, X_list, target, rec_count
    tar_x=tar_y=0
    #print(target)
    #find target in grid

    for i in range(3):
        for j in range(3):
            if grid[i][j]==target:
                tar_x=i
                tar_y=j
                break
    
    tar_b=3*(tar_x)+tar_y+1
    if tar_b==1 and b1["text"]!='X' and b1["text"]!='O':
        b_click(b1)
    elif tar_b==2 and b2["text"]!='X' and b2["text"]!='O':
        b_click(b2)
    elif tar_b==3 and b3["text"]!='X' and b3["text"]!='O':
        b_click(b3)
    elif tar_b==4 and b4["text"]!='X' and b4["text"]!='O':
        b_click(b4)
    elif tar_b==5 and b5["text"]!='X' and b5["text"]!='O':
        b_click(b5)
    elif tar_b==6 and b6["text"]!='X' and b6["text"]!='O':
        b_click(b6)
    elif tar_b==7 and b7["text"]!='X' and b7["text"]!='O':
        b_click(b7)
    elif tar_b==8 and b8["text"]!='X' and b8["text"]!='O':
        b_click(b8)
    elif tar_b==9 and b9["text"]!='X' and b9["text"]!='O':
        b_click(b9)
    else:
        #if target is occupied, search next available empty slot, but only up to 5 times
        rec_count+=1        
        ai()
        rec_count=0

# Button clicked function
def b_click(b):
    global clicked,count, X_list,O_list


    if b["text"] != "X" and b["text"] != "O" and clicked == True:
        X_list.append(int(b["text"]))
        b["activeforeground"]="black"

        b["fg"]="black"
        b["text"] = "X"
       
        clicked = False
        count += 1
        checkifwon()
        update()
        # print(board)
        ai()
        

    elif b["text"] != "X" and b["text"] != "O" and clicked == False:
        O_list.append(int(b["text"]))
        b["text"] = "O"
        b["fg"]="black"
        b["activeforeground"]="black"
        clicked = True
        count += 1
        checkifwon()
        update()
        print(O_list)
    else:
        messagebox.showerror("Tic Tac Toe", "Hey! That box has already been selected\nPick Another Box..." )
    
# Start the game over!
def reset():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    global clicked, count, X_list, O_list,board
    clicked = False
    count = 0
    X_list=[]
    O_list=[]
    board=[[0,0,0],[0,0,0],[0,0,0]]

    # Build our buttons
    b1 = Button(root, text=grid[0][0], activeforeground="white", fg="white", font=("Helvetica", 20), height=3,  bg="white", width=6, command=lambda: b_click(b1))
    b2 = Button(root, text=grid[0][1], activeforeground="white", fg="white", font=("Helvetica", 20), height=3, bg="white", width=6, command=lambda: b_click(b2))
    b3 = Button(root, text=grid[0][2], activeforeground="white", fg="white", font=("Helvetica", 20), height=3, bg="white", width=6, command=lambda: b_click(b3))

    b4 = Button(root, text=grid[1][0], activeforeground="white", fg="white",font=("Helvetica", 20), height=3, bg="white", width=6, command=lambda: b_click(b4))
    b5 = Button(root, text=grid[1][1], activeforeground="white", fg="white",font=("Helvetica", 20), height=3, bg="white", width=6, command=lambda: b_click(b5))
    b6 = Button(root, text=grid[1][2], activeforeground="white", fg="white",font=("Helvetica", 20), height=3, bg="white", width=6, command=lambda: b_click(b6))

    b7 = Button(root, text=grid[2][0], activeforeground="white", fg="white",font=("Helvetica", 20), height=3, bg="white", width=6, command=lambda: b_click(b7))
    b8 = Button(root, text=grid[2][1], activeforeground="white", fg="white",font=("Helvetica", 20), height=3, bg="white", width=6, command=lambda: b_click(b8))
    b9 = Button(root, text=grid[2][2], activeforeground="white", fg="white",font=("Helvetica", 20), height=3, bg="white", width=6, command=lambda: b_click(b9))

    # Grid our buttons to the screen
    b1.grid(row=0, column=0)
    b2.grid(row=0, column=1)
    b3.grid(row=0, column=2)

    b4.grid(row=1, column=0)
    b5.grid(row=1, column=1)
    b6.grid(row=1, column=2)

    b7.grid(row=2, column=0)
    b8.grid(row=2, column=1)
    b9.grid(row=2, column=2)

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create Options Menu
options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Reset", command=reset)

reset()
ai()
root.mainloop()