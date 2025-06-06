
##main file
from wordle import Wordle
from sudoku import Sudoku
from tictactoe import tictactoe
import re
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

test = Sudoku()
test.make_board()
test.ensure_solvability(3)

# test = tictactoe(True)
# test.print_board()
# while True:
#     print("Reminder, everything starts at 0, not 1 for entry validity")
#     row = int(input("Enter row: "))
#     col = int(input("Enter col: "))
#     test.game_loop(row, col, 3)
