##wordle
import re
from random import randint

class Wordle:

    def __init__(self, dict_list: list = None):
        #if the word is None still, grab a random word from the dictionary
        self.__guess = ""
        self.__g_amnt_tot = 6
        self.__found_word = False
        self.__word_len = 6
        self.__word = ""
        self.__dict_list = dict_list
        self.__select_new_word()

    def change_word_len(self, new_word_len):
        self.__word_len = new_word_len
        self.__dict_list = []
        with open("word_dict_" + str(self.__word_len) + ".txt", "r") as file:
            file.seek(0)
            for line in file:
                temp_line = ""
                for char in line:
                    if char not in ["1","2","3","4","5", "6", "7", "8", "9", "0",","]:
                        temp_line += char
                temp_line = re.sub("\n",'', temp_line)
                self.__dict_list.append(temp_line)
            file.close()
        self.__select_new_word()

    def __select_new_word(self):
        word = randint(0, len(self.__dict_list))
        self.__word = self.__dict_list[word].lower()
        self.print_word()

    def __get_word(self) -> str:
        return self.__word
    
    def print_word(self):
        print(self.__get_word())
    
    def print_guess(self):
        print(self.__guess)

    def __guess_input(self):
        if self.__g_amnt_tot == 0 or self.__found_word:
            return False
        print("Letter amount: " + str(len(self.__word)))
        print("Guess left: " + str(self.__g_amnt_tot))
        new_guess = input("Guess: ")
        if len(new_guess) == len(self.__word):
            self.__g_amnt_tot -= 1
        # else:
        #     print("Word lengths do not match, try again.")
        while True in self.__make_guess(new_guess):
            if len(new_guess) != len(self.__word):
                print("Word lengths do not match, try again.")
            elif not (self.__word in self.__dict_list):
                #self.__g_amnt_tot -= 1
                break
            else:
                print("Word not found in dictionary.")
            if self.__g_amnt_tot == 0:
                return False
            if self.__found_word:
                return False
            new_guess = input("Guess: ")
        return True

    def __make_guess(self, guess: str) -> list:
        value_list = []
        self.__guess = guess
        p_guess = [char for char in self.__guess]
        print("Your guess: "+ self.__guess)
        self.__make_colors(p_guess)
        if self.__guess == self.__word:
            self.__found_word = True
        elif len(self.__guess) != len(self.__word):
            value_list.append(True)
        elif not (self.__word in self.__dict_list):
            value_list.append(True)
        return value_list
    
    def __make_colors(self, p_guess: list):
        #🟥
        #🟨
        #🟩
        sym_str = ""
        c_word = [c for c in self.__word]
        for char in p_guess:
            if char in c_word:
                for i in range(len(c_word)):
                    if c_word[i] == char:
                        c_word[i] = 0
                        break
                for j in range(len(p_guess)):
                    if p_guess[j] == char:
                        p_guess[j] = 0
                        break
                if i == j:
                    sym_str += "🟩"
                elif (i != j):
                    sym_str +=  "🟨"
            else:
                sym_str += "🟥"
        print(sym_str)




    def start_game(self):
        while self.__guess_input() == True:
            self.__guess_input()
            continue