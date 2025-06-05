#player class

class player:

    def __init__(self, is_computer = False, player_no = 1):
        self.__is_pc = is_computer
        self.__turn_no = player_no
        if self.__is_pc:
            self.__my_turn = False
        else:
            if self.__turn_no == 1:
                self.__my_turn = True
            else:
                self.__my_turn = False
    
    def make_move(self, board, row, col) -> list:
        #returns the board provided with an updated version of that board with the player's new move at that row and col
        board[row][col] = self.__turn_no
        return board