import pygame
import random
pygame.init()
pygame.mixer.init()


screen_width = 900
screen_height = 600
orange = (255, 165, 0)
black = (0, 0, 0)
purple = (149, 53, 83)
white = (255, 255, 255)


#Creating Window
gamewindow = pygame.display.set_mode((screen_width,screen_height))   # (screen_width,screen_height)

#Game Title
pygame.display.set_caption("SerpentSprinterWithRJ")

bg = pygame.image.load('bgimg.jpg')
bg = pygame.transform.scale(bg,(screen_width, screen_height)).convert_alpha()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)
def text_screen(text,color,x,y) :
    screen_text = font.render(text,True,color)
    gamewindow.blit(screen_text,[x,y])
def plot_snake(gamewindow,black,snake_list,snake_size):
    for x,y in snake_list :
        pygame.draw.rect(gamewindow, black, [x, y, snake_size, snake_size])

def homescreen():

    exit_game = False
    snake_emoji = pygame.image.load("snakeemoji.png")  # I will add snake emoji
    snake_emoji = pygame.transform.scale(snake_emoji, (60, 60))
    while not exit_game :
        gamewindow.fill(orange)
        text_screen("Welcome to Serpent Sprinter", black, 190, 250)
        text_screen("Press \"spacebar\" to play", purple, 230, 295)
        text_screen("Designed by Rajat", white, 552, 560)
        gamewindow.blit(snake_emoji, (430, 190))
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                exit_game = True
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    pygame.mixer.music.load('back21.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(60)




#Creating a game loop
def gameloop() :
    # Creating Game-specific variables like fps,colors,bonus,exitgame,gameover
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 30
    snake_size = 15
    init_velocity = 4
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(10, 900 / 1.2)
    food_y = random.randint(10, 600 / 1.2)
    score = 0
    # Adding colors(rgb)
    white = (255, 255, 255)
    orange = (255, 165, 0)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (100, 255, 200)
    blue = (200, 0, 255)
    fps = 60
    snake_list = []
    snake_length = 1
    with open("highscore.txt","r") as f :
        highscore = f.read()

    while not exit_game:
        if game_over :
            with open("highscore.txt","w") as f :
                f.write(str(highscore))             # Saving the high score
            gamewindow.fill(white)
            text_screen("Well played! Game Over: Press \"enter\" to restart",red,10,250)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        homescreen()            # I replaced the gameloop() with homescreen() as I want homscreen after game gets over.
                if event.type == pygame.QUIT:
                    exit_game = True

        else:
            # Handling events like the cursor movements or keyboard inputs:It basically starts reading every moment using below for loop.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:      #QUIT is an event/constant in Pygame representing a quit event.It checks if quit event has occured in the program
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT :
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT :
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_DOWN :
                        velocity_x = 0
                        velocity_y = init_velocity
                    if event.key == pygame.K_UP :
                        velocity_x = 0
                        velocity_y = -init_velocity

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)< 10 and abs(snake_y - food_y)< 10 : #Snake eats

                score += 10
                food_x = random.randint(10, 900 / 1.2)
                food_y = random.randint(10, 600 / 1.2)
                snake_length += 5
                init_velocity += 0.1
                eating_sound = pygame.mixer.Sound('eating.mp3')     # Different then pygame.mixer.music. pygame.mixer.Sound module is used to play short sounds while allowing background music to play without any hindrance
                eating_sound.play()
                if score > int(highscore) :
                    highscore = score

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)



            gamewindow.fill(green)
            gamewindow.blit(bg,(0, 0))
            text_screen("Score =  " + str(score) + " High Score= " + str(highscore), orange, 5, 5)
            pygame.draw.rect(gamewindow, red, [food_x, food_y, snake_size, snake_size])
            plot_snake(gamewindow, black, snake_list, snake_size)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x<0 or snake_x > screen_width or snake_y <0 or snake_y > screen_height :
                game_over = True
                pygame.mixer.music.load('explosion.mp3')
                pygame.mixer.music.play()

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('explosion.mp3')
                pygame.mixer.music.play()





            #pygame.draw.rect(gamewindow,black,[snake_x,snake_y,snake_size,snake_size])

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

homescreen()



#Notes:
# 1)The window in computer graphics and game development typically uses a coordinate system where the origin (0,0) is at the top-left corner of the screen or window. This system is similar to the Cartesian coordinate system but with the y-axis flipped. Here's a breakdown:
#
# Origin (0,0): Top-left corner.
# X-Axis: Positive to the right.
# Y-Axis: Positive downwards.

#2)font = pygame.font.SysFont(None, 55): This line creates a font object using pygame.font.SysFont. The first argument is the font type, and None means using the default font. The second argument (55) is the font size.

#def text_screen(text, color, x, y):: This line defines a function named text_screen that takes four parameters: text (the text you want to display), color (the color of the text), x (the x-coordinate where you want to place the text), and y (the y-coordinate where you want to place the text).

#screen_text = font.render(text, True): This line renders the text using the previously defined font. It creates a new surface with the rendered text. The first argument is the text you want to render, and the second argument (True) indicates whether to use antialiasing (smoothing of the text edges).

#gamewindow.blit(screen_text, [x, y]): This line blits (draws) the rendered text onto the game window at the specified coordinates [x, y].


