import time
import math
from player import ComputerPlayer, HumanPlayer


class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[idx*3:(idx+1) * 3] for idx in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        print("\nThe computer will be 'X' and you will be 'O'.")
        print('Here is the board with numbers for each square. \n')
        # map number squares on board (0-8)
        # 0 | 1 | 2
        # 3 | 4 | 5
        # 6 | 7 | 8
        number_board = [[str(idx) for idx in range(jdx*3, (jdx+1)*3)] for jdx in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # row check
        row_idx = math.floor(square / 3)
        row = self.board[row_idx*3:(row_idx+1)*3]   
        if all([s == letter for s in row]):
            return True
        
        # column check
        col_idx = square % 3
        column = [self.board[col_idx+idx*3] for idx in range(3)]
        if all([s == letter for s in column]):
            return True
        
        # diagonal check
        if square % 2 == 0:
            # diag - upper left to right
            diagonal1 = [self.board[idx] for idx in [0, 4, 8]]
     
            if all([loc == letter for loc in diagonal1]):
                return True
            # diag - upper right to left
            diagonal2 = [self.board[idx] for idx in [2, 4, 6]]
 
            if all([loc == letter for loc in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [idx for idx, loc in enumerate(self.board) if loc == " "]


def play(game, x_player, o_player, print_game=True):

    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):

            if print_game:
                print('\nIt is now the Computer\'s turn.')
                sleep_time = 1
                print(letter + ' moves to square {}'.format(square))
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    if letter == 'X':
                        print('The Computer wins!')
                    else:
                        print('You win!')
                # ends the game
                return letter              
            # switch players
            if letter == 'X':
                letter = 'O'  
            else:
                letter = 'X'

        time.sleep(.8)

    if print_game:
        print('The match is a draw!')

if __name__ == '__main__':
    x_player = ComputerPlayer('X')
    o_player = HumanPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)