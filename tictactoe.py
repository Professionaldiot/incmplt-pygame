#tictactoe
from player import player
from copy import deepcopy

class tictactoe(player) :

    def __init__(self, against_pc = False):
        self.__board = [[0 for a in range(3)] for b in range(3)]
        self.__p1 = player(False, 1)

        if against_pc:
            self.__p2 = player(True, 2)
        else:
            self.__p2 = player(False, 2)

    def print_board(self):
        #print the board
        for row in range(3):
            row_str = ""
            for col in range(3):
                row_str += str(self.__board[row][col]) + " "
            print(row_str)
        print()

    def start_game(self):
        self.__board = self.__p1.make_move(self.__board, 0, 0)
        self.print_board()
        self.__board = self.__p2.make_move(self.__board, 0, 2)
        self.print_board()
        self.__board = self.__p1.make_move(self.__board, 2, 2)
        self.print_board()
        self.__board = self.__p2.make_move(self.__board, 1, 1)
        self.print_board()
        self.__board = self.__p1.make_move(self.__board, 2, 0)
        self.print_board()
        print(self.__find_best_move())

    def __find_best_move(self) -> tuple:
        temp_board = deepcopy(self.__board)
        best_score = 50
        best_move = (0,0)
        for i in range(3):
            for j in range(3):
                if self.__board[i][j] == 0:
                    new_score = self.__eval_board(temp_board, i, j)
                    if best_score < new_score:
                        best_score = new_score
                        best_move = (i, j)
        print(best_score)
        return best_move



    def __eval_board(self, board, row, col) -> int:
        #evaluates the board at the current state of the board
        #and gives a score based on how good the move is
        #50 for just placing a piece
        #100 for blocking the opponents winning move
        #500 for a winning move

        score = 50 #add the 50 score for just placing a piece 

        #these are the checks for blocking an enemy's next winning move
        #check the enemy winning conds for the row we're in
        if 0 in board[row]:
            temp_count = 0
            for c in board[row]:
                if c == 1:
                    temp_count += 1
            if temp_count == 2:
                score += 100

        #do a quick check for any zeros in the col
        found_zero = False
        for r in range(3):
            if board[r][col] == 0:
                found_zero = True
                break
        #now, if we find a zero in the col, check to see how many ones are there
        #this could be done in the above for loop, but it doesn't really matter right now
        if found_zero:
            temp_count = 0
            for r in range(3):
                if board[r][col] == 1:
                    temp_count += 1
            if temp_count == 2:
                score += 100
        #do the diaganol checks
        #diags are as follows:
        #(0,0), (1,1), (2,2)
        #(2,0), (1,1), (0,2)
        found_zero = False
        #check for 0's
        for i in range(3):
            if found_zero:
                break
            if board[i][i] == 0 and i == row and i == col:
                found_zero = True
                break
            if board[2-i][i] == 0 and (2-i) == row and i == col:
                found_zero = True
                break
        
        count_one = 0
        count_two = 0
        if found_zero:
            for i in range(3):
                if board[i][i] == 1:
                    count_one += 1
                if board[2-i][i] == 1:
                    count_two += 1
            if count_one == 2:
                score += 100
            if count_two == 2:
                score += 100
        
        #these are the checks for placing the piece at row, col and whether that move that will win the pc's current turn
        #this literally the same code as above, just replaced the checks for 1 to 2
        if 0 in board[row]:
            temp_count = 0
            for c in board[row]:
                if c == 2:
                    temp_count += 1
            if temp_count == 2:
                score += 500

        #do a quick check for any zeros in the col
        found_zero = False
        for r in range(3):
            if board[r][col] == 0:
                found_zero = True
                break
        #now, if we find a zero in the col, check to see how many ones are there
        #this could be done in the above for loop, but it doesn't really matter right now
        if found_zero:
            temp_count = 0
            for r in range(3):
                if board[r][col] == 2:
                    temp_count += 1
            if temp_count == 2:
                score += 500
        #do the diaganol checks
        #diags are as follows:
        #(0,0), (1,1), (2,2)
        #(2,0), (1,1), (0,2)
        found_zero = False
        #check for 0's
        for i in range(3):
            if found_zero:
                break
            if board[i][i] == 0:
                found_zero = True
                break
            if board[2-i][i] == 0:
                found_zero = True
                break
        
        count_one = 0
        count_two = 0
        if found_zero:
            for i in range(3):
                if board[i][i] == 2:
                    count_one += 1
                if board[2-i][i] == 2:
                    count_two += 1
            if count_one == 2:
                score += 500
            if count_two == 2:
                score += 500

        return score