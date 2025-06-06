#tictactoe
from player import player
from copy import deepcopy
from random import randint
from math import floor
import time

class tictactoe(player) :

    def __init__(self, against_pc = False):
        self.__board = [[0 for a in range(3)] for b in range(3)]
        self.__p1 = player(False, 1)
        self.__turn_no = 1
        if against_pc:
            self.__p2 = player(True, 2)
        else:
            self.__p2 = player(False, 2)
        self.__playing_cp = against_pc

    def print_board(self, board: list = None):
        #print the board
        if board == None:
            board = self.__board
        for row in range(3):
            row_str = ""
            for col in range(3):
                row_str += str(board[row][col]) + " "
            print(row_str)
        print()

    def game_loop(self, row: int = 0, col: int = 0, diff_as_int: int = 1):
        if self.__turn_no%2 == 0 and not self.__playing_cp:
            self.__board = self.__p2.make_move(self.__board, row, col)
        else:
            self.__board = self.__p1.make_move(self.__board, row, col)
        self.print_board()
        self.__turn_no += 1
        if self.__playing_cp:
            self.__min_max_player_two(diff_as_int)
            self.print_board()
        
    def __min_max_player_two(self, diff_as_int):
        round_no = self.__turn_no
        best_score = 0
        best_start_move = (0,0)
        j = 1
        k = 0
        
        while j > 0 or k > 1000:
            start_move = (0,0)
            temp_board = deepcopy(self.__board)
            i = round_no #i will be equal to the amount of moves done so far
            while k < 1000:
                #check if either player has won each time
                #if one of them has, assign the scores
                current_score = self.__check_board(temp_board)
                move = self.__find_best_move(2 - (i%2), temp_board, diff_as_int)
                if len(move) == 1 and self.__turn_no < 4:
                    best_start_move = move[0]
                    j = 0
                    break
                j = len(move)
                if len(move) == 0:
                    #here is where we check who won, and give a score based on that
                    self.print_board(temp_board)
                    break
                #print(move)
                ind = randint(0, len(move)-1)
                new_move = move[ind]
                if temp_board[new_move[0]][new_move[1]] == 0:
                    start_move = new_move
                if current_score != 0:
                    if current_score > best_score:
                        best_score = current_score
                        best_start_move = start_move
                    break
                if best_start_move == (0,0):
                    print(move)
                    best_start_move = start_move
                move.remove(new_move)
                if temp_board[new_move[0]][new_move[1]] != 0:
                    break
                temp_board[new_move[0]][new_move[1]] = 2 - (i%2)
                print(move)
                self.print_board(temp_board)
                i += 1
            #end while True
            k += 1
            #print(k)
            if j == 0 or k > 1000:
                print(best_start_move)
                self.__board = self.__p2.make_move(self.__board, best_start_move[0], best_start_move[1])
                break
        #end while j > 0

    def __check_board(self, board: list = None) -> int:
        if board == None:
            board == self.__board
        board_score = 0

        #check the rows
        for i in range(3):
            if board[i] == [2 for j in range(3)]:
                board_score = 100
            if board[i] == [1 for k in range(3)]:
                board_score = -100
        #check the cols
        for col in range(3):
            check = 0
            check_two = 0
            for r in range(3):
                if board[r][col] == 2:
                    check += 1
                if board[r][col] == 1:
                    check_two -= 1
                if check >= 3 and board_score == 0:
                    board_score = 100
                    break
                if check_two <= -3 and board_score == 0:
                    board_score = -100
                    break
        #check the diagnols
        check = 0
        check_two = 0
        for i in range(3):
            if board[i][i] == 2 or board[2-i][i] == 2:
                check += 1
            if board[i][i] == 1 or board[2-i][i] == 1:
                check_two -= 1
        #adjust the score based on who has one of the diagnols
        if check >= 3 and board_score == 0:
            board_score = 100
        if check_two <= -3 and board_score == 0:
            board_score = -100
        #print(board_score)
        return board_score
        
    def __find_best_move(self, player, temp_board, diff_as_int) -> list:
        #this funciton can control difficulty with the simple 
        #fact that if I want to make it harder for the player, then
        #I can only take the best move and not the other moves into consideration
        #while easier difficulties would use some or all of the list
        #1 -> easy
        #2 -> medium
        #3 -> hard

        #this function returns the best move on the board
        self.print_board(temp_board)
        best_score = 75
        best_moves = []
        #sets the default move to the middle spot, if not taken already
        if self.__board[1][1] == 1:
            best_move = (0,0)
        else:
            best_move = (1,1)
        for i in range(3):
            for j in range(3):
                if temp_board[i][j] == 0:
                    #only eval the board at this space if it's a 0
                    #no point in doing the ones with numbers on it already
                    new_score = self.__eval_board(temp_board, i, j, player)
                    #print(new_score)
                    if (best_score == new_score or len(best_moves) == 0) and diff_as_int < 3:
                        best_moves.append((i,j))
                    if best_score < new_score:
                        #if the new score is better, replace the old one
                        best_score = new_score
                        best_move = (i, j)
                        best_moves = [best_move]
                        print()
                        print(best_move)
                        print(best_score)
                        print()
        #print(best_score)
        #print(best_move)
        if diff_as_int < 3:
            #this will remove all the moves based on diff
            #easy -> no moves are removed
            #med -> 1/2 are removed
            #hard -> all are removed, but this is handled in the above statement when checking
            len_diff_move_list = floor((1 - (1/diff_as_int)) * len(best_moves))
            #the above statement gets the new length of the list, and we will randomally select indices that we haven't already
            i = 0
            while i < len_diff_move_list:
                ind = randint(0, len(best_moves))
                best_moves.remove(best_moves[ind])
                i += 1

        print(best_moves)
        return best_moves

    def __eval_board(self, board, row, col, player) -> int:
        #need to add the checks for placing pieces next to each other
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
                if c == 2 - ((player +1) % 2):
                    #that  2 - ((player + 1) % 2) gets the next player, always
                    # if player == 1
                    # (1 + 1) % 2 = 0
                    # 2 - 0 = 2
                    # if player == 2
                    # (2 + 1) % 2 = 1
                    # 2 - 1 = 1
                    temp_count += 1
                    print("horiz")
                    print(c)
                    print(2 - ((player + 1) % 2))
                    print()
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
                if board[r][col] == 2 - ((player +1) % 2):
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
                if board[i][i] == 2 - ((player +1) % 2):
                    count_one += 1
                if board[2-i][i] == 2 - ((player +1) % 2):
                    count_two += 1
                    print("diag: " + str((2-i)) + " " + str(i))
                    print()
            if count_one == 2:
                score += 100
            if count_two == 2:
                score += 100
                #somehow count two is happening on (2,2)
        
        #these are the checks for placing the piece at row, col and whether that move that will win the pc's current turn
        #this literally the same code as above, just replaced the checks for 1 to 2
        if 0 in board[row]:
            temp_count = 0
            for c in board[row]:
                if c == player:
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
                if board[r][col] == player:
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
                if board[i][i] == player:
                    count_one += 1
                if board[2-i][i] == player:
                    count_two += 1
            if count_one == 2:
                score += 500
            if count_two == 2:
                score += 500

        #add some score for placing a piece next to another piece of the same variety
        #2 - ((player +1) % 2)
        #this checks if there is 2 0's in a row and then if the player is also in that row
        z_count = 0
        for item in board[row]:
            if item == 0:
                z_count += 1
        if z_count == 2 and player in board[row]:
            score += 25
        
        #this does the checks for the col we're in
        z_count = 0
        found_player = False
        for r in range(3):
            if board[r][col] == 0:
                z_count += 1
            if board[r][col] == player:
                found_player = True
        if z_count == 2 and found_player:
            score += 25

        #and finally the diagnols
        z_count = 0
        #check for 0's
        for i in range(3):
            if board[i][i] == 0:
                z_count += 1
            if board[2-i][i] == 0:
                z_count += 1
        
        count_one = 0
        count_two = 0
        if z_count > 2:
            for i in range(3):
                if board[i][i] == 0:
                    count_one += 1
                if board[2-i][i] == 0:
                    count_two += 1
            if count_one == 2:
                score += 25
            if count_two == 2:
                score += 25

        return score