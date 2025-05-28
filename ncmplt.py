##main file
from wordle import Wordle
from sudoku import Sudoku
import re

total_words = 145473
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

test = Wordle(words)
test.start_game()

# test = Sudoku()
# test.make_board()
# test.print_board()