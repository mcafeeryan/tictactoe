import struct, string, random

class TicTacToeBoard:

    def __init__(self):
        self.board = (['N']*3,['N']*3,['N']*3)
                                      
    def PrintBoard(self):
        print(self.board[0][0] + "|" + self.board[1][0] + "|" + self.board[2][0])
        
        print(self.board[0][1] + "|" + self.board[1][1] + "|" + self.board[2][1])
        
        print(self.board[0][2] + "|" + self.board[1][2] + "|" + self.board[2][2])
        
    def play_square(self, col, row, val):
        self.board[col][row] = val

    def unplay_square(self, col, row):
        self.board[col][row] = 'N'

    def get_square(self, col, row):
        return self.board[col][row]

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if(self.board[i][j]=='N'):
                    return False

        return True
    
    #if there is a winner this will return their symbol (either 'X' or 'O'),
    #otherwise it will return 'N'
    def winner(self):
        #check the cols
        for col in range(3):
            if(self.board[col][0]!='N' and self.board[col][0] == self.board[col][1] and self.board[col][0]==self.board[col][2] ):
                return self.board[col][0]
        #check the rows
        for row in range(3):
            if(self.board[0][row]!='N' and self.board[0][row] == self.board[1][row] and self.board[0][row]==self.board[2][row] ):
                return self.board[0][row]
        #check diagonals
        if(self.board[0][0]!='N' and self.board[0][0] == self.board[1][1] and self.board[0][0]==self.board[2][2] ):
            return self.board[0][0]
        if(self.board[2][0]!='N' and self.board[2][0] == self.board[1][1] and self.board[2][0]==self.board[0][2]):
            return self.board[2][0]
        return 'N'

def possible_moves(board):
    moves = []
    for col in range(3):
        for row in range(3):
            if(board.get_square(col,row)=='N'):
                moves.append([col,row])
    return moves

def minimax_decision(board,player):
    maxi = -100
    action = []
    moves = possible_moves(board)
    if player == 'X':
        humanval = 'O'
    else:
        humanval = 'X'
    for move in moves:
        [col, row] = move
        board.play_square(col,row,player)
        val = min_val(board, humanval, -100, 100, player)
        board.unplay_square(col,row)
        if val >= maxi:
            maxi = val
            action = [col, row]
    return action

def max_val(board, player, alpha, beta, original):
    moves = possible_moves(board)
    winner = board.winner()
    if (winner == 'N') and (board.full_board()):
        return 0
    elif winner == original:
        return 1
    elif winner != 'N':
        return -1
    value = -100
    if player == 'X':
        other = 'O'
    else:
        other = 'X'
    for move in moves:
        [col, row] = move
        board.play_square(col, row, player)
        value = max(value, min_val(board,other, alpha, beta,original))
        board.unplay_square(col,row)
        if value >= beta:
            return value
        alpha = max(alpha,value)
    return value


def min_val(board, player, alpha, beta, original):
    moves = possible_moves(board)
    winner = board.winner()
    if (winner == 'N') and (board.full_board()):
        return 0
    elif winner == original:
        return 1
    elif winner != 'N':
        return -1
    value = 100
    if player == 'X':
        other = 'O'
    else:
        other = 'X'
    for move in moves:
        [col, row] = move
        board.play_square(col, row, player)
        value = min(value, max_val(board,other,alpha,beta,original))
        board.unplay_square(col,row)
        if value <= alpha:
            return alpha
        beta = min(beta,value)
    return value

def cpu_play(board, cpuval):
    action = minimax_decision(board,cpuval)
    [col, row] = action
    board.play_square(col,row,cpuval)

def evaluation(board,player):
    #the idea is to see how many possibilities there are for the other player to win, and for you to win, and subtract them

    possible_wins = 0
    possible_loss = 0
    score = 0
    winner = board.winner()
    if winner != 'N':
        if winner == player:
            return 1
        else:
            return -1

    #check all possible wins/losses
    #check the cols
    for col in range(3):
        if((board.get_square(col,0)==player or board.get_square(col,0) == 'N') and (board.get_square(col,1)==player or board.get_square(col,1) == 'N')
         and (board.get_square(col,2)==player or board.get_square(col,2)=='N')):
            possible_wins += 1
        if(board.get_square(col,0)!=player and board.get_square(col,1) != player and board.get_square(col,2)!=player):
            possible_loss += 1
    #check the rows
    for row in range(3):
        if((board.get_square(0,row)==player or board.get_square(0,row)=='N') and (board.get_square(1,row)==player or board.get_square(1,row)=='N')
         and (board.get_square(2,row)==player or board.get_square(2,row)=='N')):
            possible_wins += 1
        if(board.get_square(0,row)!=player and board.get_square(1,row) != player and board.get_square(2,row)!=player):
            possible_loss += 1
    #check diagonals
    if((board.get_square(0,0)==player or board.get_square(0,0)=='N') and (board.get_square(1,1)==player or board.get_square(1,1)=='N')
     and (board.get_square(2,2)==player or board.get_square(2,2)=='N')):
        possible_wins += 1
    if((board.get_square(0,2)==player or board.get_square(0,2)=='N') and (board.get_square(1,1)==player or board.get_square(1,1)=='N')
     and (board.get_square(2,0)==player or board.get_square(2,0)=='N')):
        possible_wins += 1
    if(board.get_square(0,0)!=player and board.get_square(1,1)!=player and board.get_square(2,2)!=player):
        possible_loss += 1
    if(board.get_square(0,2)!=player and board.get_square(1,1)!=player and board.get_square(2,0)!=player):
        possible_loss += 1

    score = possible_wins - possible_loss
    return score

def play(cpuval):
    Board = TicTacToeBoard()
    if cpuval == 'O':
        humanval = 'X'
    else:
        humanval = 'O'
    Board.PrintBoard()
    
    if humanval != 'X':
        print("CPU Move")
        cpu_play(Board,cpuval)
        Board.PrintBoard()

    while( Board.full_board()==False and Board.winner() == 'N'):
        print("your move, pick a row (0-2)")
        row = int(input())
        print("your move, pick a col (0-2)")
        col = int(input())

        if(Board.get_square(col,row)!='N'):
            print("square already taken!")
            continue
        else:
            Board.play_square(col,row,humanval)
            if(Board.full_board() or Board.winner()!='N'):
                break
            else:
                Board.PrintBoard()
                print("CPU Move")
                cpu_play(Board,cpuval)
                Board.PrintBoard()

    Board.PrintBoard()
    if(Board.winner()=='N'):
        print("Cat game")
    elif(Board.winner()==humanval):
        print("You Win!")
    elif(Board.winner()==cpuval):
        print("CPU Wins!")

def main():
    print("Pick what the CPU will be playing as (type X or O)")
    cpuval = str(input())
    play(cpuval)

main()