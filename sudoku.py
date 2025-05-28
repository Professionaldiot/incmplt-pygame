#sudoku
from random import randint

class Sudoku:
    def __init__(self):
        self.__board = []
        self.__init_board()
    
    def __init_board(self):
        for i in range(9):
            self.__board.append(["0" for a in range(9)])
        
    def print_board(self):
        for i in range(9):
            line_str = ""
            if (i) % 3 == 0:
                print()
            for j in range(9):
                line_str += str(self.__board[i][j])
                if (j+1) % 3 == 0:
                    line_str += "   "
            print(line_str)

    def make_board(self):
        row = 0
        while row < 9:
            self.__shuffle_row(row)
            while self.__check_board() == False:
                invalid_nums = self.__check_board(row)
                #print(invalid_nums)
                if len(invalid_nums) == 0:
                    break
                elif len(invalid_nums) == 1:
                    self.__shuffle_row(row)
                    continue
                elif len(invalid_nums) == 2:
                    #swap those two nums
                    held_num = self.__board[row][invalid_nums[0]]
                    self.__board[row][invalid_nums[0]] = self.__board[row][invalid_nums[1]]
                    self.__board[row][invalid_nums[1]] = held_num

                    if self.__check_board() == False:
                        self.__shuffle_row(row)
                        continue
                elif len(invalid_nums) < 5:
                    #from right to left, swap the number on the end with the first number in the list, then remove the last number in the list
                    j = len(invalid_nums)
                    while j > 0:
                        #first swap the nums at the [-1] and [0] indices
                        held_num = self.__board[row][invalid_nums[-1]]
                        self.__board[row][invalid_nums[-1]] = self.__board[row][invalid_nums[0]]
                        self.__board[row][invalid_nums[0]] = held_num
                        invalid_nums.remove(invalid_nums[-1])
                        j -= 1
                else:
                    self.__shuffle_row(row)
            print()
            self.print_board()
            row += 1

    def __shuffle_row(self, row: int = 0):
        #randomizes the row provided
        nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        new_row = []
        while len(nums) > 0:
            ind = randint(0, len(nums)-1)
            new_row.append(nums[ind])
            nums.remove(nums[ind])
        if len(new_row) == 9:
            self.__board[row] = new_row

    
    def __check_board(self, row: int = None):
        #if the row is none when called, return a bool
        #else return a list of numbers in that row that are invalid
        valid = True
        invalid_nums = []
        #self.print_board()
        
        #check the horizontal rows
        for i in range(9):
            nums = []
            for j in range(9):
                if self.__board[i][j] in nums and self.__board[i][j] != 0:
                    valid = False
                elif self.__board[i][j] != 0:
                    nums.append(self.__board[i][j])

        #check the vertical rows
        for i in range(9):
            nums = []
            for j in range(9):
                if self.__board[j][i] in nums and self.__board[j][i] != 0:
                    if row != None and j == row:
                        invalid_nums.append(i)
                    valid = False
                elif self.__board[j][i] != 0:
                    nums.append(self.__board[j][i])
        
        #check that one of each number is in each box
        for i  in range(3):
            checked_nums = []
            # i * 3 = start of col index for each box
            for j in range(3):
                checked_nums = []
                # same for j, but this will give the start of the row index for each box
                #check the items in that box, only need to do 3 each time
                for k in range(i*3, (i*3)+3):
                    #start at i*2 and go until i*2 + 3
                    for l in range(j*3, (j*3)+3):
                        #start at j*2 and go until j*2 + 3
                        num = self.__board[k][l]
                        if not (num in checked_nums) and num != "0":
                            checked_nums.append(num)
                        elif num != "0":
                            valid = False
                            if row != None and l == row:
                                invalid_nums.append(l)
                        if len(checked_nums) != 9:
                            valid = False

        
        if row == None:
            return valid
        else:
            return invalid_nums