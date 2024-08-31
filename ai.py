import random
from pieces import Piece
from rules import is_checkmate, is_stalemate

class AI:
    def __init__(self, game, color):
        self.game = game
        self.color = -1  # AI plays as black, adjust if necessary

    def make_move(self):
        best_move = self.find_best_move()
        if best_move:
            self.game.move(best_move)
            self.game.display()  # Display game state after the move
            print(f"Move executed: {best_move}")
        
    def find_best_move(self, depth=3):
        best_move = None
        best_value = -float('inf')
        
        legal_moves = self.game.get_legal_moves(self.color)
        
        for move in legal_moves:
            piece, start_pos, end_pos = move
            move = piece, start_pos, end_pos[1]
            
            # Clona lo stato del tabellone
            cloned_game = self.game.clone()
            
            # Esegui la mossa sulla copia del tabellone
            cloned_game.move(move)
            
            # Crea una nuova istanza dell'AI per il tabellone clonata
            ai_clone = AI(cloned_game, self.color)
            eval = ai_clone.minimax(depth - 1, -float('inf'), float('inf'), False)
            
            if eval > best_value:
                best_value = eval
                best_move = move
        
        return best_move



    def evaluate_board(self):
        piece_values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0
        }
        board_value = 0

        for row in self.game.board:
            for piece in row:
                if isinstance(piece, Piece):
                    notation = piece.get_notation()
                    board_value += piece_values.get(notation, 0) * piece.color
                    
                    # Evaluate piece position
                    board_value += self.position_value(piece)

        return board_value
    
    def position_value(self, piece):
        # Simplified position value function that ignores specific positions
        piece_type = piece.get_notation().lower()
    
        # Return a simple value for each piece type
        if piece_type == 'p':
            return 1  # Pawns
        elif piece_type == 'n':
            return 3  # Knights
        elif piece_type == 'b':
            return 3  # Bishops
        elif piece_type == 'r':
            return 5  # Rooks
        elif piece_type == 'q':
            return 9  # Queens
        elif piece_type == 'k':
            return 0  # Kings (usually not evaluated in terms of points)
        return 0

    def minimax(self, depth, alpha, beta, is_maximizing):
        if depth == 0 or is_checkmate(self.game, self.color) or is_stalemate(self.game, self.color):
            return self.evaluate_board()
    
        if is_maximizing:
            max_eval = -float('inf')
            for move in self.game.get_legal_moves(self.color):
                piece, start_pos, end_pos = move
                move = piece, start_pos, end_pos[1]
    
                # Clona lo stato del tabellone
                cloned_game = self.game.clone()
    
                # Esegui la mossa nel gioco clonata
                if not cloned_game.move(move):
                    continue  # Salta se la mossa non è valida
    
                # Crea una nuova istanza dell'AI per il tabellone clonata
                ai_clone = AI(cloned_game, -self.color)
                eval = ai_clone.minimax(depth - 1, alpha, beta, False)
    
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.game.get_legal_moves(-self.color):
                piece, start_pos, end_pos = move
                move = piece, start_pos, end_pos[1]
    
                # Clona lo stato del tabellone
                cloned_game = self.game.clone()
    
                # Esegui la mossa nel gioco clonata
                if not cloned_game.move(move):
                    continue  # Salta se la mossa non è valida
    
                # Crea una nuova istanza dell'AI per il tabellone clonata
                ai_clone = AI(cloned_game, -self.color)
                eval = ai_clone.minimax(depth - 1, alpha, beta, True)
    
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


