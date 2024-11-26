
# (c) 2024 Roland Labana
# Modified by Gabriel Villegas and Giancarlo Umberto Ambrosino

import random

DEBUG = False # Debug variable, set to True to enable debug functions
PRINTING = False

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
        if PRINTING:
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
                if PRINTING:
                    self.display_board()
                player.make_move(self)
                if self.check_win(game.board):
                    if PRINTING:
                        self.display_board()
                        print(f"{player.symbol} wins!")
                    return
                if self.is_board_full():
                    if PRINTING:
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
                
    def dfs(self, target_score, depth, find_max):
        # Base case: if the node has the target score and is a leaf, return its depth
        if self.score == target_score and not self.children:
            return depth

        # Recursive case: explore children
        depths = [
            child.dfs(target_score, depth + 1, find_max) for child in self.children
            if (find_max and child.score >= target_score) or (not find_max and child.score <= target_score)
        ]
        return min(depths, default=float('inf'))
    
    """
    Finds the depth of the shallowest node with the target score.
    If find_max is True, we search for the highest score; otherwise, the lowest score.
    Not implemented in Minimax V 1.1 but could be used in the future
    """
    def find_best_depth(self, target_score, find_max=True):
        return self.dfs(target_score, 0, find_max)

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
        self.symbol = symbol

    # Helper function; different from your is_board_full as it asks for a board 
    # instead of checking the object's board field
    def is_board_full(self, board):
        return ' ' not in board

    # Build the tree and assign scores based on the leaf nodes
    def buildTree(self, board, turn):
        # Base cases
        winner = None
        if game.check_win(board):
            winner = 'X' if turn == 'O' else 'O'
        if winner:
            return TreeNode(board, 1 if winner == self.symbol else -1)
        if self.is_board_full(board):
            return TreeNode(board, 0)

        # Create root node for current board
        root = TreeNode(board[:], 0)

        # Initialize list to store scores of child nodes
        child_scores = []

        # Iterate through available moves
        for move in range(9):
            if board[move] == ' ':
                # Make the move
                board[move] = turn
                # Recursively call buildTree on the new board state
                next_turn = 'X' if turn == 'O' else 'O'
                child_node = self.buildTree(board[:], next_turn)
                root.add_child(child_node)
                child_scores.append(child_node.score)
                # Undo the move
                board[move] = ' '

        # Assign score to root based on children's scores
        if turn == self.symbol:
            root.score = max(child_scores)
        else:
            root.score = min(child_scores)

        return root

    # Pick the first good move on the children array
    def pickMove(self):
        # Choose the move with the best score
        best_score = max(child.score for child in self.root.children)
        best_moves = [child for child in self.root.children if child.score == best_score]

        # If multiple moves have the same best score, you can choose the first one
        best_move = best_moves[0]

        # Find the move that resulted in this board
        for tile in range(len(game.board)):
            if game.board[tile] != best_move.board[tile]:
                return tile

    def determine_move(self, game):
        board = game.board[:]
        self.root = self.buildTree(board, self.symbol)
        return self.pickMove()
    
class MiniMaxDepthGG(MiniMaxGG):

    def __init__(self, symbol, depth):
        super().__init__(symbol)
        self.depth = depth
    
    '''
    Scores if leaf node is reached:
    +1000: win at leaf node
    -1000: lose at leaf node
    0: tie at leaf node
    
    Scores in other cases:
    +3: control of the center tile (position 4)
    -3: opponent controls the center tile
    
    +2: control of a corner tile (positions 0, 2, 6, 8)
    -2: opponent controls a corner tile
    
    +1: control of an edge tile (positions 1, 3, 5, 7)
    -1: opponent controls an edge tile
    
    +50: immediate win (two player symbols and one empty space in a line)
    -50: immediate block (opponent has two symbols and one empty space in a line)
    
    +5: creating a potential fork (one player symbol and two empty spaces in a line)
    -10: preventing an opponent fork (one opponent symbol and two empty spaces in a line)
    
    +1 per player symbol in a winning line with no opponent symbols
    -1 per opponent symbol in a winning line with no player symbols
    
    +1: symmetry bonus for controlling corners diagonally (e.g., positions 0 and 8 or 2 and 6)
    
    Late-game adjustments:
    +20: completing a line with two player symbols and one empty space (prioritized in late game)
    -20: blocking a line with two opponent symbols and one empty space (prioritized in late game)
    '''
    def evaluate(self, board, player):
        opponent = 'X' if player == 'O' else 'O'
        score = 0

        # Positional advantage
        center = 4
        corners = [0, 2, 6, 8]
        edges = [1, 3, 5, 7]

        # Center control
        if board[center] == player:
            score += 3
        elif board[center] == opponent:
            score -= 3

        # Corner control
        for corner in corners:
            if board[corner] == player:
                score += 2
            elif board[corner] == opponent:
                score -= 2

        # Edge control
        for edge in edges:
            if board[edge] == player:
                score += 1
            elif board[edge] == opponent:
                score -= 1

        # Line evaluation and advanced heuristics
        winning_lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]

        for line in winning_lines:
            player_count = sum(1 for i in line if board[i] == player)
            opponent_count = sum(1 for i in line if board[i] == opponent)
            empty_count = sum(1 for i in line if board[i] == ' ')

            if player_count == 2 and empty_count == 1:
                score += 50  # Immediate win
            if opponent_count == 2 and empty_count == 1:
                score -= 50  # Immediate block

            if player_count == 1 and empty_count == 2:
                score += 5  # Encourage creating forks
            if opponent_count == 1 and empty_count == 2:
                score -= 10  # Discourage opponent forks

            if player_count > 0 and opponent_count == 0:
                score += player_count  # Potential winning line
            elif opponent_count > 0 and player_count == 0:
                score -= opponent_count  # Opponent's potential winning line

        # Symmetry bonus
        if board[0] == player and board[8] == ' ':
            score += 1
        if board[2] == player and board[6] == ' ':
            score += 1

        # Late-game adjustments
        empty_spaces = sum(1 for i in board if i == ' ')
        if empty_spaces <= 3:
            if player_count == 2 and empty_count == 1:
                score += 20  # Late-game boost for completing lines
            if opponent_count == 2 and empty_count == 1:
                score -= 20  # Late-game boost for blocking threats

        return score


    # Build Tree according the depth limitation, if leaf is not reached use the above eval function
    def buildTree(self, board, turn, depth):
        # Base cases
        winner = None
        if game.check_win(board):
            winner = 'X' if turn == 'O' else 'O'
        if winner:
            return TreeNode(board, 1000 if winner == self.symbol else -1000)
        if self.is_board_full(board):
            return TreeNode(board, 0)
        
        # No leaf node was reached, call eval function to determine score
        if depth == 0:
            return TreeNode(board, self.evaluate(board, turn))

        # Create root node for current board
        root = TreeNode(board[:], 0)

        # Initialize list to store scores of child nodes
        child_scores = []

        # Iterate through available moves
        for move in range(9):
            if board[move] == ' ':
                # Make the move
                board[move] = turn
                # Recursively call buildTree on the new board state
                next_turn = 'X' if turn == 'O' else 'O'
                child_node = self.buildTree(board[:], next_turn, depth-1)
                root.add_child(child_node)
                child_scores.append(child_node.score)
                # Undo the move
                board[move] = ' '

        # Assign score to root based on children's scores
        if turn == self.symbol:
            root.score = max(child_scores)
        else:
            root.score = min(child_scores)

        return root
    
    def determine_move(self, game):
        board = game.board[:]
        self.root = self.buildTree(board, self.symbol, self.depth)
        return self.pickMove()


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
