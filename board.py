from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from rules import is_valid_move, is_castling_move, is_checkmate, is_stalemate, handle_end_game
import copy

class Chess:
    def __init__(self, EPD='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'):
        """
        Initializes a new chess game.
        EPD: A string representing the initial chess setup in EPD format.
        """
        self.x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']  
        self.y = ['8', '7', '6', '5', '4', '3', '2', '1']  
        self.piece_classes = {
            'P': Pawn, 'N': Knight, 'B': Bishop, 'R': Rook, 'Q': Queen, 'K': King,
            'p': Pawn, 'n': Knight, 'b': Bishop, 'r': Rook, 'q': Queen, 'k': King
        }
        self.reset(EPD=EPD)
        self.log = []

    def reset(self, EPD='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'):
        """
        Resets the game to its initial state.
        EPD: A string representing the initial chess setup in EPD format.
        """
        self.log = []  
        self.init_pos = EPD  
        self.EPD_table = {}  
        self.p_move = 1  
        self.castling = [1, 1, 1, 1]  
        self.en_passant = None  
        self.board = [[0] * 8 for _ in range(8)]  
        self.load_EPD(EPD)

    def load_EPD(self, EPD):
        """
        Loads the initial chess setup from the EPD string.
        EPD: A string representing the initial chess setup in EPD format.
        """
        data = EPD.split(' ')
        if len(data) == 4:
            for x, rank in enumerate(data[0].split('/')):
                y = 0
                for p in rank:
                    if p.isdigit():
                        y += int(p)
                    else:
                        piece_class = self.piece_classes[p]
                        color = 1 if p.isupper() else -1
                        # Set the piece position
                        self.board[x][y] = piece_class(self, color, (x, y))
                        y += 1
            self.p_move = 1 if data[1] == 'w' else -1
            self.castling = [1 if c in data[2] else 0 for c in "KQkq"]
            self.en_passant = None if data[3] == '-' else self.board_2_array(data[3])
            return True
        else:
            return False

    def display(self):
        """
        Displays the current chessboard.
        """
        result = '  a b c d e f g h  \n  ----------------\n'
        for c, y in enumerate(self.board):
            result += f'{8 - c}|'
            for x in y:
                if x != 0:
                    piece_notation = x.get_notation().upper() if x.color == 1 else x.get_notation().lower()
                    result += piece_notation + ' '
                else:
                    result += '. '
            result += f'|{8 - c}\n'
        print(result)
        
    def clone(self):
        return copy.deepcopy(self)

    @staticmethod
    def board_2_array(pos):
        """
        Converts a position in chess notation to a (row, column) tuple of the board matrix.
        pos: A string representing a position in chess notation (e.g. 'a1', 'h8').
        """
        if len(pos) == 2 and pos[0] in 'abcdefgh' and pos[1] in '12345678':
            return int(pos[1]) - 1, ord(pos[0]) - ord('a')
        else:
            return None

    def move(self, move, player=None):
        if move:
            piece, from_pos, to_pos = move
            if from_pos and to_pos:
                captured_piece = self.board[to_pos[0]][to_pos[1]]  # Identify the captured piece (if any)
                special_move = None
    
                # Check if the move is a castling move
                if is_castling_move(self, move):
                    self.execute_castling(move)
                    special_move = "castling"
                    captured_piece = None  # Castling does not capture any piece
    
                    # Log the move
                    if player is not None:  # Only for human players
                        print(f"Executing castling move: {piece.get_notation()} from {from_pos} to {to_pos}")
                    self.log.append((piece, from_pos, to_pos, captured_piece, special_move))
                else:
                    # Check if the move is valid
                    is_valid, reason = is_valid_move(self, move)
                    if is_valid:
                        if player is not None:  # Only for human players
                            print(f"Executing move: {piece.get_notation()} from {from_pos} to {to_pos}")
    
                        # Handle en passant
                        if isinstance(piece, Pawn) and abs(to_pos[1] - from_pos[1]) == 1 and to_pos[0] - from_pos[0] == piece.color:
                            if self.board[to_pos[0]][to_pos[1]] == 0:
                                captured_piece = self.board[from_pos[0]][to_pos[1]]  # Pawn captured en passant
                                self.board[from_pos[0]][to_pos[1]] = 0
                                special_move = "en passant"
                                if player is not None:  # Only for human players
                                    print("En passant capture executed.")
    
                        # Move the piece to the new position
                        piece.move(from_pos, to_pos)
    
                        # Handle pawn promotion
                        if isinstance(piece, Pawn) and (to_pos[0] == 0 or to_pos[0] == 7):
                            self.board[to_pos[0]][to_pos[1]] = Queen(self, piece.color)  # Promote to Queen
                            if player is not None:  # Only for human players
                                print("Pawn promoted to Queen.\n")
    
                        # Change the player's turn
                        self.p_move *= -1
                        self.last_move = move
    
                        # Check for checkmate or stalemate
                        if is_checkmate(self, self.p_move):
                            if player is not None:  # Only for human players
                                print("Checkmate! The game is over.\n")
                            handle_end_game(self)
                        elif is_stalemate(self, self.p_move):
                            if player is not None:  # Only for human players
                                print("Stalemate! The game is over.\n")
                            handle_end_game(self)
                        else:
                            if player is not None:  # Only for human players
                                print("Move executed successfully!\n")
    
                        # Log the move
                        self.log.append((piece, from_pos, to_pos, captured_piece, special_move))
                    else:
                        if player is not None:  # Only for human players
                            print(f"Invalid move: {reason}\n")

    def get_legal_moves(self, player):
        """
        Gets all possible legal moves for the specified player.
        """
        legal_moves = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if isinstance(piece, Piece) and piece.color == player:
                    piece_moves = piece.movement(player, (y, x))
                    legal_moves.extend([(piece, (y, x), move) for move in piece_moves])
        
        castling_moves = [(None, from_pos, to_pos) for from_pos, to_pos in self.get_castling_moves()]
        legal_moves.extend(castling_moves)
        
        return legal_moves

    def get_castling_moves(self):
        """
        Generates castling moves for the current player.
        """
        castling_moves = []
        if self.p_move == 1:
            if self.castling[0]:  # Short castling for white
                if self.board[7][5] == 0 and self.board[7][6] == 0:
                    castling_moves.append(((7, 4), (7, 6)))  # Add the king's move
            if self.castling[1]:  # Long castling for white
                if self.board[7][1] == 0 and self.board[7][2] == 0 and self.board[7][3] == 0:
                    castling_moves.append(((7, 4), (7, 2)))  # Add the king's move
        else:
            if self.castling[2]:  # Short castling for black
                if self.board[0][5] == 0 and self.board[0][6] == 0:
                    castling_moves.append(((0, 4), (0, 6)))  # Add the king's move
            if self.castling[3]:  # Long castling for black
                if self.board[0][1] == 0 and self.board[0][2] == 0 and self.board[0][3] == 0:
                    castling_moves.append(((0, 4), (0, 2)))  # Add the king's move
        return castling_moves
    
    def execute_castling(game, move):
        piece, from_pos, to_pos = move
        if to_pos[1] == 2:  # Queenside castling
            rook_pos = (from_pos[0], 0)
            new_rook_pos = (from_pos[0], 3)
        else:  # Kingside castling
            rook_pos = (from_pos[0], 7)
            new_rook_pos = (from_pos[0], 5)
    
        # Move the rook
        game.board[new_rook_pos[0]][new_rook_pos[1]] = game.board[rook_pos[0]][rook_pos[1]]
        game.board[rook_pos[0]][rook_pos[1]] = 0
        game.board[new_rook_pos[0]][new_rook_pos[1]].has_moved = True
    
        # Move the king
        game.board[to_pos[0]][to_pos[1]] = game.board[from_pos[0]][from_pos[1]]
        game.board[from_pos[0]][from_pos[1]] = 0
        game.board[to_pos[0]][to_pos[1]].has_moved = True
    
        game.p_move *= -1
        print("Castling move executed!")

    def undo_last_move(self):
        if self.log:
            last_move = self.log.pop()
            piece, from_pos, to_pos, captured_piece, special_move = last_move
            
            # Restore player turn
            self.p_move *= -1
            print("Last move undone.\n")
            
            # Restore the board state
            self.board[from_pos[0]][from_pos[1]] = piece
            self.board[to_pos[0]][to_pos[1]] = captured_piece
    
            # Restore specific rules if applicable
            if special_move == "castling":
                # Restore the king's and rook's position based on the castling type
                if to_pos[1] == from_pos[1] + 2:  # Kingside castling
                    # King moved from from_pos to to_pos, and the rook also moved
                    self.board[from_pos[0]][from_pos[1] + 2] = 0  # Clear new king's position
                    self.board[from_pos[0]][from_pos[1] + 1] = 0  # Clear new rook's position
                    self.board[from_pos[0]][from_pos[1]] = piece  # Restore king to original position
                    self.board[from_pos[0]][from_pos[1] + 3] = Rook(self, piece.color)  # Restore rook to original position
                elif to_pos[1] == from_pos[1] - 2:  # Queenside castling
                    # King moved from from_pos to to_pos, and the rook also moved
                    self.board[from_pos[0]][from_pos[1] - 2] = 0  # Clear new king's position
                    self.board[from_pos[0]][from_pos[1] - 1] = 0  # Clear new rook's position
                    self.board[from_pos[0]][from_pos[1]] = piece  # Restore king to original position
                    self.board[from_pos[0]][from_pos[1] - 4] = Rook(self, piece.color)  # Restore rook to original position
    
            elif special_move == "en passant":
                # Restore the pawn that was captured en passant
                if piece.color == 1:  # White pawn
                    self.board[to_pos[0] + 1][to_pos[1]] = Pawn(self, 1)  # Restore white pawn
                else:  # Black pawn
                    self.board[to_pos[0] - 1][to_pos[1]] = Pawn(self, -1)  # Restore black pawn
    
            elif isinstance(piece, Queen) and (from_pos[0] == 0 or from_pos[0] == 7):
                # Undo pawn promotion: replace queen with pawn
                self.board[to_pos[0]][to_pos[1]] = Pawn(self, piece.color)
    
        else:
            print("No moves to undo.\n")
            
    def exit_game(self):
        print("Exiting the game.\n")
        handle_end_game(self)
