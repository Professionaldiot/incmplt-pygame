
##main file
from wordle import Wordle
from sudoku import Sudoku
from tictactoe import tictactoe
from button import button
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
with open("word_dict_5.txt", "r") as file:
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



pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

most_recent=0
with open("save_data.txt", "r") as file:
    file.seek(0)
    for line in file:
        for char in range(len(line)):
            if line[char] == "=":
                most_recent = int(line[char+1])
    file.close()

change_screen = False
screen_list = [0, 0, 0, 0, 0]
list_of_screens = ["main", "select", "settings", "quit", "main", "sudoku"]
new_menu = "main"
back_num = 0

test = Sudoku()
test.make_board()
sud_board = test.ensure_solvability(2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    # when buttons are pressed, the index for the next screen is given as an int
    # that button's return statement, only play will be different every time, as it
    # should go to the most recent played game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")
    

    if change_screen:
        change_screen = False
        while screen_list[0] == 0:
            screen_list.remove(0)
        

    window = pygame.display.get_surface()
    pos = pygame.mouse.get_pos()
    pressing = pygame.mouse.get_pressed(num_buttons = 3)

    
    if (len(screen_list) > 0) and screen_list[0] < most_recent:
        new_menu = list_of_screens[screen_list[0]]
        
    else:
        new_menu = list_of_screens[most_recent]


    #pressing[0] is the left button, pressing[1] is middle mouse, pressing[2] is the right button
    #we want to span the space between x and 720 - x evenly between 4 independent assests

    """
    0 is a placeholder, meant for holding a button not being pressed
    1 is the select screen
    2 is the settings screen
    3 quits the game
    4 is the main menu
    """
    if back_num in screen_list:
            back_num = 4
    if new_menu == "quit":
        running = False
        continue
    if new_menu == "main":
        play = button((540, 60), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\play_button", window, pos, pressing[0], most_recent)
        select = button((540, 230), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\select", window, pos, pressing[0], 1)
        settings = button((540, 390), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\settings_button", window, pos, pressing[0], 2)
        quit = button((540, 560), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\quit", window, pos, pressing[0], 3)
        
        if len(screen_list) != 5:
            screen_list = [0, 0, 0, 0, 0]
        screen_list[0] = (play.get_action_ind())
        screen_list[1] = (select.get_action_ind())
        screen_list[2] = (settings.get_action_ind())
        screen_list[3] = (quit.get_action_ind())
        for i in range(1,4):
            if i in screen_list:
                back_num = i
                change_screen = True
                break
    elif new_menu == "select":
        back = button((60, 310), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\back", window, pos, pressing[0], 4)
        
        if back.get_action_ind() == 4:
            change_screen = True
            screen_list = [0, 0, 0, 0, 0]
            screen_list[4] = 4
    elif new_menu == "settings":
        back = button((60, 310), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\back", window, pos, pressing[0], 4)
        if back.get_action_ind() == 4:
            change_screen = True
            screen_list = [0, 0, 0, 0, 0]
            screen_list[4] = back_num
    else:
        #this will draw the buttons for any game we are in
        back = button((60, 560), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\back", window, pos, pressing[0], 4)
        settings = button((60, 420), r"C:\Users\Declan\Desktop\incmplt-pygame\pygame-assets\settings_button", window, pos, pressing[0], 2)

        if settings.get_action_ind() == 2:
            change_screen = True
            screen_list = [0, 0, 0, 0, 0]
            screen_list[2] = 2
            back_num = most_recent
        if back.get_action_ind() == 4:
            change_screen = True
            screen_list = [0, 0, 0, 0, 0]
            screen_list[4] = back_num
            
    if new_menu == "sudoku":
        #this draws text to the screen in the middle, 10 pixels down
        #10 pixels down with a font size of 64 is 74 pixels from the top
        #720 - 74 = 646
        font = pygame.font.Font(None, 64)
        text = font.render("Sudoku", True, (10, 10, 10))
        textpos = text.get_rect(centerx = screen.get_width() / 2, y = 10)
        screen.blit(text, textpos)
        test.render_sudoku(sud_board, screen)
        test.update_boxes(pos, screen)
    pygame.display.flip()

    clock.tick(60)


pygame.quit()