
# (c) 2024 Roland Labana
# Modified by Gabriel Villegas and Giancarlo Umberto Ambrosino

import random

DEBUG = False # Debug variable, set to True to enable debug functions

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, game):
        raise NotImplementedError("Subclass must implement abstract method")

class HumanPlayer(Player):
    def make_move(self, game):
        while True:
            try:
                move = int(input(f"Enter your move for '{self.symbol}' (0-8): "))
                if game.is_valid_move(move):
                    game.make_move(move, self.symbol)
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number.")

# Template for AI Player
class AIPlayer(Player):
    def __init__(self, symbol, strategy):
        super().__init__(symbol)
        self.strategy = strategy

    def make_move(self, game):
        # Here's where students would implement their AI logic
        print(f"{self.symbol}'s AI is thinking...")
        move = self.strategy.determine_move(game)
        if game.is_valid_move(move):
            game.make_move(move, self.symbol)
        else:
            print(f"Error: Invalid move suggested by {self.symbol}'s AI. Defaulting to random move.")
            # Default to random move if AI suggests an invalid move
            for i in range(9):
                if game.is_valid_move(i):
                    game.make_move(i, self.symbol)
                    break

class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [' ' for _ in range(9)]
        self.players = [player1, player2]
        #self.display_board()  # Display the board initially


    def play(self):
         while True:
            for player in self.players:
                self.display_board()
                player.make_move(self)
                if self.check_win(game.board):
                    self.display_board()
                    print(f"{player.symbol} wins!")
                    return
                if self.is_board_full():
                    self.display_board()
                    print("It's a draw!")
                    return

    def is_valid_move(self, move):
        return self.board[move] == ' ' and 0 <= move <= 8

    def make_move(self, move, symbol):
        self.board[move] = symbol

    def check_win(self, theBoard):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(theBoard[i] == symbol for i in combo) for symbol in ['X', 'O'] for combo in win_conditions)

    def is_board_full(self):
        return ' ' not in self.board

    def display_board(self):
        #print("\nCurrent Board State:")
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("-----------")
        print ()

        

# Example of a simple AI strategy - pick FIRST available space 0 - 8
class SimpleAI:
    def determine_move(self, game):
        # Simple strategy: check for winning move, then blocking opponent's win, then take first open space
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'X'  # Assuming this AI plays 'X'
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'O'  # Check if opponent ('O') could win
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check
        # If no immediate winning or blocking move, take first available space
        for i in range(9):
            if game.is_valid_move(i):
                return i
            
# Example of a simple AI strategy - pick a RANDOM available space 0 - 8
class RandomAI:
    def determine_move(self, game):
        possibleMoves = []
        #add all open spaces into a list to then randomly choose one
        for i in range(9):
            if game.is_valid_move(i):
                possibleMoves.append(i)
        return (random.choice(possibleMoves))
    
# an AI strategy that prioritizes getting three corners 
# before picking corners though, it will check if there is a winning move or not
# if there are no more corners or winning moves, it will fill in the rest of the tiles
class GabeSimpleAI:
    def get_corners_GV(self,possibleMoves,corners): # creates lists of valid corner and non-corner tiles
        valid_corners = [] 
        valid_non_corners = [] 
        for tile in possibleMoves:
            if tile in corners:
                valid_corners.append(tile)
            else:
                valid_non_corners.append(tile)
        return valid_corners, valid_non_corners
    
    def block_or_win_GV(self,possibleMoves): #checks each move and returns the first winning move, for either player
        for tile in possibleMoves:           #a winning move and a losing move hold the same value in this strategy, which yes has faults
            if self.block_check_GV(tile) == True:
                return tile
        return None
    
    def block_check_GV(self,tile): # used in block_or_win_GV to actually find winning and blocking moves, and returns a boolean value
        sim_board = game.board

        sim_board[tile] = "X"
        if game.check_win(sim_board):
            sim_board[tile] = " "; return True
        
        sim_board[tile] = "O"
        if game.check_win(sim_board):
            sim_board[tile] = " "; return True
        
        sim_board[tile] = " "; return False

    def determine_move(self, game): # funciton that calls all the beforehand funcitons and returns an integer to Mr. Labana's code
        corners = [0,2,6,8]
        possibleMoves = []
        #add all open spaces into a list to then randomly choose one
        for i in range(0,9):
            if game.is_valid_move(i):
                possibleMoves.append(i)

        res = self.block_or_win_GV(possibleMoves)

        if res == None: # Nothing to block or nothing to win
            valid_corners, valid_non_corners = self.get_corners_GV(possibleMoves,corners)
            

            if valid_corners == [] and len(valid_corners)<=3:
                if valid_non_corners == []:
                    move = None ## this shouldn't happen since the board would be full
                else:
                    move = random.choice(valid_non_corners)
            else:
                move = random.choice(valid_corners)

            
            return move
        
        else: # something can be blocked or a win is possible
            return res

# Helper Tree class for MiniMax, implemented by Giancarlo
class TreeNode:
    def __init__(self, board, score):
        self.board = board
        self.score = score
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
    
    def print_tree(self, level=0):
        indent = "  " * level
        board_str = ''.join(self.board)
        print(f"{indent}Board: {board_str}, Score: {self.score}")
        for child in self.children:
            if isinstance(child, TreeNode):
                child.print_tree(level + 1)

''' 
"AI" that uses the MiniMax algorithm to determine the next move.
The algorithm first builds a tree of all possibilities, then it
assigns a score to each of them, and lastly it picks the value
that is best for the current symbol.
The algorithm assumes the other player will always play optimally.
Implemented by Gabe and Giancarlo 
'''
class MiniMaxGG:

    def __init__(self, symbol):
        # TODO: implement logic to see if it is going first or not
        self.firstMove = True
        self.symbol = symbol

    def buildTree(self, board, turn):
        # Base cases for win or draw
        if game.check_win(board):
            return TreeNode(board, 1 if turn != self.symbol else -1)
        if game.is_board_full():
            return TreeNode(board, 0)

        # Create root node for current board
        root = TreeNode(board, 0)

        # Iterate through available moves
        for move in range(9):
            if board[move] == ' ':
                # Make the move
                board[move] = turn
                # Recursively call buildTree on the new board state
                next_turn = 'X' if turn == 'O' else 'O'
                child_node = self.buildTree(board[:], next_turn)
                root.add_child(child_node)
                # Undo the move
                board[move] = ' '

        # Assign score to root based on children's scores
        if root.children:  # Ensure there are children before calculating the score
            if turn == self.symbol:
                root.score = max(child.score for child in root.children)
            else:
                root.score = min(child.score for child in root.children)

        return root
    
    # TODO: implement method that returns move based on tree scores
    # Look at the node's children and find the ones with a -1 score
    def pickMove(self, currBoard):
        NODE_LOC = 0
        DEPTH_LOC = 1
        goodMoves = []
        for move in currBoard.children: # finding -1 scores
            if move.score == -1:
                goodMoves.append([move,0]) # the 0 will be replaced with a depth number
        
        depth_of_moves = []
        for move in goodMoves: # finds the best depth of each child node to 
            move[DEPTH_LOC] = move[NODE_LOC].find_best_depth
            depth_of_moves.append(move[DEPTH_LOC])
        
        best_depth = min(depth_of_moves)
        for move in goodMoves:
            if move[DEPTH_LOC] == best_depth:
                return best_depth

    def determine_move(self, game):
        board = game.board

        self.root = TreeNode(board, -2)

        self.root = self.buildTree(board[:], self.symbol)

        if DEBUG:
            self.root.print_tree()

        return self.pickMove(self.root)

if __name__ == "__main__":
    # Here you can decide how to initialize players
    # For example, to test with one human and one AI:
    # player1 = HumanPlayer('X')
    # player2 = AIPlayer('O', SimpleAI())
    # game = TicTacToe(player1, player2)
    # game.play()

    # For students' AI competition:
    player1 = HumanPlayer('X')
    #player2 = HumanPlayer('O')

    #player2 = AIPlayer('O', SimpleAI())  # Replace with student AI implementation - name function with your name ie: "Jim-AI"
    #player2 = AIPlayer('X', RandomAI())  # Replace with another student AI implementation or the same for testing ie: "Mary-AI"
    
    #player1 = AIPlayer('X',GabeSimpleAI())
    player2 = AIPlayer('O', MiniMaxGG('O'))

    game = TicTacToe(player1, player2)
    game.play()