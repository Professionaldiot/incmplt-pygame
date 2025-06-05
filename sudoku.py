#sudoku
from random import randint

class Sudoku:
    def __init__(self):
        self.__board = []
        self.__r_c_valid = {}
        self.__init_board()
    
    def __init_board(self):
        for i in range(9):
            self.__board.append(["0" for a in range(9)])
            for j in range(9):
                r_c = (i, j)
                self.__r_c_valid[r_c] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

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

    def make_board(self, num_restarts: int = 0) -> list:
        #shuffle the row based on the nums at that pos
        #then systematically remove those nums from the spaces below
        #if we do this correctly, it will result in a correct board every time
        #things to make sure of:
        #   * to make sure the number we select is in the nums list in shuffle row
        #   * that we have one of every number in each row and col

        #if the for loop is able to finish correctly, then the board is automatically valid
        #if the weird bug happens when the box already has the number, then somehow the shuffle_row(i)
        #adds the same number in [which shouldn't happen] and causes teh first removals to break
        #then it's not valid at the moment and should be restarted
        restart = False
        for i in range(9):
            #first shuffle the row
            if self.__shuffle_row(i):
                restart = True
            #then systemically remove the nums from the same col in the rows below
            for row in range(i+1, 9):
                if restart:
                    break
                for col in range(9):
                    r_c = (row, col)
                    try:
                        self.__r_c_valid[r_c].remove(self.__board[i][col])
                    except(ValueError):
                        break
            if restart:
                break

            #gonna see if doing the box removal of nums here solves the box issues
            for i  in range(3):
                checked_nums = []
                # i * 3 = start of col index for each box
                for j in range(3):
                    checked_nums = []
                    # same for j, but this will give the start of the row index for each box
                    #check the items in that box, only need to do 3 each time
                    for k in range(i*3, (i*3)+3):
                        #start at i*3 and go until i*3 + 3
                        for l in range(j*3, (j*3)+3):
                            #start at j*3 and go until j*3 + 3
                            num = self.__board[k][l]
                            if (not (num in checked_nums)):
                                checked_nums.append(num)
                            elif num == "0":
                                r_c = (k, l)
                                for n in checked_nums:
                                    if n in self.__r_c_valid[r_c]:
                                        self.__r_c_valid[r_c].remove(n)
            #self.print_board()
            for row in range(9):
                if restart:
                    break
                for col in range(9):
                    r_c = (row, col)
                    if len(self.__r_c_valid[r_c]) == 0:
                        restart = True
                        break
            if restart:
                break
        if restart:
            print()
            restart = False
            self.__board = []
            self.__init_board()
            self.make_board(num_restarts + 1)
        else:
            self.print_board()
            print()
            print("Finished with " + str(num_restarts) + " restart(s)")
            return self.__board

    def __shuffle_row(self, row: int = 0):
        #randomizes the row provided, can only use the nums at (row, col)
        nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        new_row = []
        restart = False
        loop_count = 0
        #len(new_row) is the col # we're at
        #nums[ind] needs to be in the dict entry at that (row, col)
        attempts = 0
        while len(nums) > 0:
            if loop_count > 100:
                restart = True
                break
            col = len(new_row)
            r_c = (row, col)
            #get a new index based on the remaining valid nums at the row, col
            ind = randint(0, len(self.__r_c_valid[r_c])-1)
            num = self.__r_c_valid[r_c][ind]
            #save the num we're testing for easier access
            test_row = self.__r_c_valid[r_c]
            if num in nums:
                #if the num is in the above nums list, then everything is fine and dandy
                #go ahead and add it to the new row and then remove it from nums
                new_row.append(num)
                nums.remove(num)
            else:
                #but if it's not, then we need to check the validity of the row
                #meaning, if we have no possible option left, we need to restart the
                #randomization process
                test_row_validity = False
                x = 0
                while test_row[x] in new_row:
                    if x == len(test_row)-1:
                        test_row_validity = True
                        break
                    x += 1
                else:
                    attempts = attempts
                if test_row_validity:
                    new_row = []
                    nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    attempts += 1
                    loop_count += 1
        if len(new_row) == 9 and not restart:
            self.__board[row] = new_row
            print("Completed row: " + str(row + 1) + " in " + str(attempts) + " attempts")
        return restart
