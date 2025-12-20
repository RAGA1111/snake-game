from tkinter import * 
import random 
import numpy
# constants
GAME_WIDTH = 600
GAME_HEIGHT = 600
GAME_SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00e6b8"
BACKGROUND_COLOR = "#001f2d"
FOOD_COLOR = "#1ea1a1"

# snake class
class Snake:
    def __init__(self):
        self.body_size=BODY_PARTS
        self.coordinates=[]
        self.squares=[]

        for i in range(0,BODY_PARTS):
            self.coordinates.append([0,0])
        
        for x,y in self.coordinates:
            square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tag="snake")
            self.squares.append(square)

# food class 
class Food:
    def __init__(self):
        x= random.randint(0,(GAME_WIDTH//SPACE_SIZE) -1) * SPACE_SIZE
        y= random.randint(0,(GAME_HEIGHT//SPACE_SIZE )-1) * SPACE_SIZE

        self.coordinates=[ x , y ]

        canvas.create_oval( x, y, x+SPACE_SIZE, y+SPACE_SIZE ,fill=FOOD_COLOR,tag="food" )

# functions

def start_game():
    global snake, food
    start_button.pack_forget()  

    # create objects for a snake and food
    snake = Snake()            
    food = Food()          

    next_turn(snake, food)     


def next_turn(snake,food):
    x,y=snake.coordinates[0]
    if direction=="up":
        y-=SPACE_SIZE
    elif direction=="down":
        y+=SPACE_SIZE
    elif direction=="left":
        x-=SPACE_SIZE
    elif direction=="right":
        x+=SPACE_SIZE

    snake.coordinates.insert(0,(x,y))

    square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR)

    snake.squares.insert(0,square)

    if x==food.coordinates[0] and y==food.coordinates[1]:
        global score
        score+=1 
        label.config(text="Score : {}".format(score))
        canvas.delete("food")
        food=Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(GAME_SPEED,next_turn,snake,food)

def change_direction(new_direction):
    global direction
    if new_direction=='left':
        if direction!='right':
            direction=new_direction
    elif new_direction=='right':
        if direction!='left':
            direction=new_direction
    elif new_direction=='up':
        if direction!='down':
            direction=new_direction
    elif new_direction=='down':
        if direction!='up':
            direction=new_direction
    

def check_collisions(snake):
    x,y=snake.coordinates[0]
    if x<0 or x>=GAME_WIDTH:
        return True
    elif y<0 or y>=GAME_HEIGHT:
        return True 
    for body_part in snake.coordinates[1:]:
        if x==body_part[0] and y==body_part[1]:
            return True 
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()//2 ,canvas.winfo_height()//2,font=("consolas",70),text="GAME OVER",fill="white",tag="gameover")
    restart_button.pack(pady=10) 

def restart_game():
    global score, direction, snake, food

    canvas.delete("all")  # Clear everything
    label.config(text="Score: 0")
    score = 0
    direction = "down"
    restart_button.pack_forget()  # Hide the restart button

    snake = Snake()
    food = Food()
    next_turn(snake, food)


# displaying on window
window=Tk()

window.title("SNAKE GAME")

window.resizable(False,False)

window.configure(bg="white")


score = 0
direction = "down"

# for score tracking 
label=Label(window,text="Score : {}".format(score),font=('consolas',40),background="white")
label.pack()

#create start button
start_button = Button(window, text="Start Game", font=('consolas', 20),bg="#006d77",fg="white" ,command=start_game)
start_button.pack(pady=10,fill='x')

#create restart button
restart_button = Button(window,text="Restart Game",font=('consolas', 20),command=restart_game,bg="#005f73",fg="white",activebackground="#00b4d8",activeforeground="white")
restart_button.pack_forget()  # Don't show it yet


# creates canvas
canvas=Canvas(window ,bg= BACKGROUND_COLOR , height= GAME_HEIGHT , width= GAME_WIDTH)
canvas.pack()

window.update()

window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

x= (screen_width//2) - (window_width//2)
y= (screen_height//2) - (window_height//2)

# center alignment 
window.state('zoomed')  # For Windows: makes the window fullscreen (not the canvas)


window.bind('<Left>',lambda event: change_direction('left'))
window.bind('<Right>',lambda event: change_direction('right'))
window.bind('<Up>',lambda event: change_direction('up'))
window.bind('<Down>',lambda event: change_direction('down'))



window.mainloop()

