from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King

def is_valid_move(game, move):
    """
    Checks if a move is valid in the current context of the game.
    Returns a tuple containing a boolean (indicating whether the move is valid or not)
    and a string that describes the reason for the invalidity.
    """
    piece, from_pos, to_pos = move
    
    # Check if the move is castling
    if is_castling_move(game, move):
        return True, "The move is valid."  # Assuming castling is always valid in terms of piece movement
    
    # Check if the starting position contains a piece of the current player
    if not isinstance(piece, Piece):
        return False, "The starting position is empty."
    if piece.color != game.p_move:
        return False, "The starting position does not contain a piece of the current player."
    
    # Check if the destination position is empty or contains an opponent's piece
    if isinstance(game.board[to_pos[0]][to_pos[1]], Piece) and piece.color == game.board[to_pos[0]][to_pos[1]].color:
        return False, "The destination position is occupied by a piece of the current player."
    
    # Get the legal moves for the piece at that position
    legal_moves = piece.movement(game.p_move, from_pos)
    print('The legal moves are', legal_moves)
    print('The move you are trying to make is', move[1:])
    
    # Check if the move is among the legal moves
    if move[1:] not in legal_moves:
        return False, "The move is not among the legal moves."
    
    # Simulate the move
    piece_to_move = game.board[from_pos[0]][from_pos[1]]
    piece_to_capture = game.board[to_pos[0]][to_pos[1]]
    game.board[to_pos[0]][to_pos[1]] = piece_to_move
    game.board[from_pos[0]][from_pos[1]] = 0
    
    # Check if the player's king remains in check after the simulation
    is_check_after_move = is_check(game, game.p_move)
    
    # Restore the board to the state before the simulation
    game.board[from_pos[0]][from_pos[1]] = piece_to_move
    game.board[to_pos[0]][to_pos[1]] = piece_to_capture
    
    if is_check_after_move:
        return False, "The move leaves your king in check."
    
    # En passant move validation
    if isinstance(piece, Pawn) and abs(to_pos[1] - from_pos[1]) == 1 and to_pos[0] - from_pos[0] == piece.color:
        if game.board[to_pos[0]][to_pos[1]] == 0 and game.last_move:
            last_piece, last_from, last_to = game.last_move
            if isinstance(last_piece, Pawn) and last_to == (from_pos[0], to_pos[1]):
                return True, "The move is valid."
    
    # Pawn promotion
    if isinstance(piece, Pawn) and (to_pos[0] == 0 or to_pos[0] == 7):
        return True, "The move is valid. Pawn promotion."

    # If all checks pass, the move is valid
    return True, "The move is valid."

def is_check(game, player):
    king_position = None
    # Find the position of the current player's king
    for y, row in enumerate(game.board):
        for x, piece in enumerate(row):
            if isinstance(piece, Piece) and piece.color == player and piece.value == 6:  # Check if piece is a king
                king_position = (y, x)
                break
        if king_position:
            break

    if not king_position:
        return False  # The current player's king is not on the board

    # Check if the king is threatened by the opponent's legal moves
    opponent = -player
    for move in game.get_legal_moves(opponent):
        _, _, (to_start, to_end) = move
        if to_end == king_position:
            return True

    return False  # The current player's king is not threatened

def is_checkmate(game, player):
    """
    Checks if the current player is in checkmate.
    """
    if not is_check(game, player):
        return False
    
    legal_moves = game.get_legal_moves(player)
    
    for move in legal_moves:
        piece, from_pos, (to_start, to_end) = move
        
        # Simulate the move
        original_piece = game.board[to_end[0]][to_end[1]]
        game.board[to_end[0]][to_end[1]] = piece
        game.board[from_pos[0]][from_pos[1]] = 0
        
        # Check if the move prevents check
        if not is_check(game, player):
            # Revert the simulated move
            game.board[to_end[0]][to_end[1]] = original_piece
            game.board[from_pos[0]][from_pos[1]] = piece
            return False
        
        # Revert the simulated move
        game.board[to_end[0]][to_end[1]] = original_piece
        game.board[from_pos[0]][from_pos[1]] = piece
    
    # If no legal moves are available to prevent checkmate, it's checkmate
    print("Checkmate! The game is over.")
    handle_end_game(game)
    return True

def is_stalemate(game, player):
    """
    Checks if the current player is in stalemate.
    """
    if is_check(game, player):
        return False
    
    legal_moves = game.get_legal_moves(player)
    
    for move in legal_moves:
        piece, from_pos, (to_start, to_end) = move
        
        # Simulate the move
        original_piece = game.board[to_end[0]][to_end[1]]
        game.board[to_end[0]][to_end[1]] = piece
        game.board[from_pos[0]][from_pos[1]] = 0
        
        if not is_check(game, player):
            # Revert the simulated move
            game.board[to_end[0]][to_end[1]] = original_piece
            game.board[from_pos[0]][from_pos[1]] = piece
            return False
        
        # Revert the simulated move
        game.board[to_end[0]][to_end[1]] = original_piece
        game.board[from_pos[0]][from_pos[1]] = piece
    
    # If no legal moves are available, it's stalemate
    print("Stalemate! The game is over.")
    handle_end_game(game)
    return True

def handle_end_game(self):
    print("Game over!")
    print("Options:\n[1] Start new game\n[2] Exit")
    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            self.reset()
            self.display()
            break
        elif choice == "2":
            print("Thanks for playing!")
            quit()
        else:
            print("Invalid choice. Please enter 1 or 2.")

def is_castling_move(game, move):
    piece, from_pos, to_pos = move
    if isinstance(piece, King) and abs(to_pos[1] - from_pos[1]) == 2:
        # Determine if it's a kingside or queenside castling
        rook_pos = (from_pos[0], 0) if to_pos[1] < from_pos[1] else (from_pos[0], 7)
        rook = game.board[rook_pos[0]][rook_pos[1]]
        
        if isinstance(rook, Rook) and not piece.has_moved and not rook.has_moved:
            if not is_check(game, game.p_move):
                # Check that there are no pieces between the king and rook
                step = 1 if to_pos[1] > from_pos[1] else -1
                for i in range(from_pos[1] + step, rook_pos[1], step):
                    if game.board[from_pos[0]][i] != 0:
                        return False
                # Check that the king does not move through or into check
                for i in range(from_pos[1], to_pos[1] + step, step):
                    if is_square_attacked(game, (from_pos[0], i), -game.p_move):
                        return False
                return True
    return False

def is_square_attacked(game, pos, color):
    for y, row in enumerate(game.board):
        for x, piece in enumerate(row):
            if isinstance(piece, Piece) and piece.color == color:
                if pos in piece.movement(game.p_move, (y, x)):
                    return True
    return False
