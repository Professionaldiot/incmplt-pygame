
##main file
from wordle import Wordle
from sudoku import Sudoku
from tictactoe import tictactoe
from play_button import button
import re
import pygame

'''
TODO:
-add a timer mode to wordle
-add the pygame gui and get the games interacting with it
-make tic-tac-toe
    -fix the weird quirks of the min-max alg
-make minesweeper
'''

words = []
print("Loading word bank, this may take a while")
with open("word_dict_6.txt", "r") as file:
    file.seek(0)
    for line in file:
        temp_line = ""
        for char in line:
            if char not in ["1","2","3","4","5", "6", "7", "8", "9", "0",","]:
                temp_line += char
        temp_line = re.sub("\n",'', temp_line)
        words.append(temp_line)
    file.close()

# test = Wordle(words)
# test.start_game()

# test = tictactoe(True)
# test.print_board()
# while True:
#     print("Reminder, everything starts at 0, not 1 for entry validity")
#     row = int(input("Enter row: "))
#     col = int(input("Enter col: "))
#     test.game_loop(row, col, 3)

test = Sudoku()
test.make_board()
test.ensure_solvability(1)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")

    window = pygame.display.get_surface()
    pos = pygame.mouse.get_pos()
    #we want to span the space between x and 720 - x evenly between 4 independent assests
    play = button((540, 60), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\play_button.png", window)
    if play.check_for_click(pos):
        play = button((540, 60), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\play_button_dark.png", window)
    else:
        play = button((540, 60), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\play_button.png", window)


    select = button((540, 230), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\select.png", window)
    if select.check_for_click(pos):
        select = button((540, 230), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\select_dark.png", window)
    else:
        select = button((540, 230), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\select.png", window)


    settings = button((540, 390), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\settings_button.png", window)
    if settings.check_for_click(pos):
        settings = button((540, 390), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\settings_button_dark.png", window)
    else:
        settings = button((540, 390), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\settings_button.png", window)


    quit = button((540, 560), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\quit.png", window)
    if quit.check_for_click(pos):
        quit = button((540, 560), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\quit_dark.png", window)
    else:
        quit = button((540, 560), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\quit.png", window)


    pygame.display.flip()

    clock.tick(60)

pygame.quit()