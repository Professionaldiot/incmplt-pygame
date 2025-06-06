#sudoku
from random import randint
from copy import deepcopy

class Sudoku:
    def __init__(self):
        self.__board = []
        self.__r_c_valid = {}
        self.__init_board()
    
    def __init_board(self):
        for i in range(9):
            self.__board.append(["0" for a in range(9)])
            #creates a list of 9 "0"s for each row
            for j in range(9):
                r_c = (i, j)
                self.__r_c_valid[r_c] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                #sets up the dict for each space on the board

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

    def ensure_solvability(self, diff_as_num):
        #essentially the thought goes like this, to ensure a board is solvable
        #first take the fully solven board (which we have with make_board)
        #then systematically remove numbers that don't interfere with the logic of
        #the sudoku rules. After which, you need to check for uniqueness, which is as follows:
        #the board has one and only one solution
        #if the board has more than one solution, than it's not a unique board
        #the stopping point is when you have no more numbers that can be removed without
        #creating multiple solutions
        #the thought here to actually create this would to be to take the board we have
        #and randomly remove numbers and see if that causes non-uniqueness
        #if it does, then don't remove that number and re-radomize until we find one that still
        #has the unique solution, do this for an uncertain amount of time, after which we will
        #start checking each number, space by space, to see if it can be removed and create the
        #unique solution
        #difficulty levels could be as follows:
        #easy -> removes 3/8 all possible numbers to create the one unique solution
        #medium -> removes 5/8 all possible numbers to create the one unique solution
        #hard -> removes all possible numbers to create the one unique solution
        #easy -> 40 iters
        #med -> 80 iters
        #hard -> 120 iters
        #of course these could depend on modes, but those could have their own unique solvers

        for i in range(40*diff_as_num):
            row = randint(0,8)
            col = randint(0,8)
            r_c = (row, col)
            self.__r_c_valid[r_c] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            self.__board[row][col] = "0"
            self.__backtrack()
        self.print_board()
        return self.__board

    def __backtrack(self, board = None, t_dict = None, row = 0, col = 0):
        '''
        Choose an initial solution.
        Explore all possible extensions of the current solution.
        If an extension leads to a solution, return that solution.
        If an extension does not lead to a solution, backtrack to the previous solution and try a different extension.
        Repeat steps 2-4 until all possible solutions have been explored.
        '''
        #first save the board in it's current state, as well as the dict for the board
        #find the first 0
        #then try the first num in the dict at the row, col, which is a valid solution, obviously
        #then remove the nums in the copied dict and go to the next point and redo this
        #if it we end with a solution that has any 0's in it, then it's an invalid solution
        r_c = (row,col)
        if board == None:
            board = deepcopy(self.__board)
        if t_dict == None:
            t_dict = deepcopy(self.__r_c_valid)
        f_zero = False
        for row in range(9):
            if f_zero:
                break
            for col in range(9):
                if board[row][col] == "0":
                    f_zero = True
                    break
        while len(t_dict[r_c]) > 0:
            num = t_dict[r_c][0]
            #save the num
            t_dict[r_c].remove(num)
            #remove the num from the copied dict
            board[row][col] = num
            #set the board at the row, col with a zero to the new num
            self.__remove_from_dict(board, t_dict, row, col)
            #then remove that num from all invalid spaces on the board
            #the next part checks once again if there is any spaces on the board that
            #have no numbers left, if there is, then it's an invalid solution and we need to
            #permantently remove it from the list
            restart = False
            for row in range(9):
                if restart:
                    break
                for col in range(9):
                    r_c = (row, col)
                    if len(self.__r_c_valid[r_c]) == 0:
                        #if there is, then we need to restart
                        restart = True
                        break
            if restart:
                self.__r_c_valid[r_c].remove(num)
                if t_dict == None:
                    t_dict = deepcopy(self.__r_c_valid)
            else:
                if (col+1)%8 == 0:
                    self.__backtrack(board, t_dict, (row+1)%9, (col+1)%9)
                else:
                    self.__backtrack(board, t_dict, row, (col+1)%9)

    def __remove_from_dict(self, board = None, t_dict = None, start_row = 0, start_col = None):
        if board == None:
            board = deepcopy(self.__board)
        if t_dict == None:
            t_dict = deepcopy(self.__r_c_valid)
        for row in range(start_row+1, 9):
            if row != start_row+1:
                start_col = 0
            for col in range(9):
                r_c = (row, col)
                try:
                    t_dict[r_c].remove(board[start_row][col])
                except(ValueError):
                    break
            if start_col != None:
                for col in range(start_col+1, 9):
                    r_c = (start_row, col)
                    try:
                        t_dict[r_c].remove(board[start_row][col])
                    except(ValueError):
                        break

        #remove the nums in the boxes
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
                        num = board[k][l]
                        if (not (num in checked_nums)):
                            checked_nums.append(num)
                        elif num == "0":
                            r_c = (k, l)
                            for n in checked_nums:
                                if n in t_dict[r_c]:
                                    t_dict[r_c].remove(n)

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
            #self.print_board()
            self.__remove_from_dict(self.__board, self.__r_c_valid, i)
            #check if there are any spaces with no valid numbers left
            for row in range(9):
                if restart:
                    break
                for col in range(9):
                    r_c = (row, col)
                    if len(self.__r_c_valid[r_c]) == 0:
                        #if there is, then we need to restart
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

    def __shuffle_row(self, row: int = 0) -> bool:
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
                #ensures we only re-attempt this 100 times
                #if it's more than that, then restart
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
                    #checks that the number at x in test_row is in new_row
                    if x == len(test_row)-1:
                        #and if x gets all the way to the end, then we need to restart
                        test_row_validity = True
                        break
                    x += 1
                if test_row_validity:
                    #resets the row if needed
                    new_row = []
                    nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    attempts += 1
                    loop_count += 1
        if len(new_row) == 9 and not restart:
            #if the new_row is correct len and we aren't going to restart
            #set the board at the row index to the new row
            self.__board[row] = new_row
            print("Completed row: " + str(row + 1) + " in " + str(attempts) + " attempts")
        return restart