class Piece:
    def __init__(self, game, color, value, position=None):
        self.game = game
        self.color = color
        self.value = value
        self.position = position
        self.has_moved = False

    def get_notation(self):
        return self.notation

    def movement(self, player, pos, capture=True):
        raise NotImplementedError("This method should be overridden in derived classes")

    def move(self, from_pos, to_pos):
        # Update the piece's position
        if self.game.board[from_pos[0]][from_pos[1]] == self:
            self.game.board[to_pos[0]][to_pos[1]] = self
            self.game.board[from_pos[0]][from_pos[1]] = 0
            self.position = to_pos
            self.has_moved = True
            return True
        return False

class Pawn(Piece):
    def __init__(self, game, color, position=None):
        super().__init__(game, color, 1)
        self.notation = 'P'

    def movement(self, player, pos, capture=True):
        result = []

        direction = -1 if player == 1 else 1
        initial_rank = 6 if player == 1 else 1
        amt = 2 if pos[0] == initial_rank else 1

        # Pawn's forward movement
        for i in range(amt):
            next_row = pos[0] + ((i + 1) * direction)
            next_col = pos[1]
            next_pos = (next_row, next_col)
            if 0 <= next_row < 8:
                next_cell = self.game.board[next_row][next_col]
                if not isinstance(next_cell, Piece):
                    result.append((pos, next_pos))
                else:
                    break  # The pawn cannot move further if the next cell is occupied
            else:
                break  # The pawn cannot move beyond the board's edge   

        # Pawn's capture movement
        if capture:
            for i in [-1, 1]:
                next_row = pos[0] + direction
                next_col = pos[1] + i
                next_pos = (next_row, next_col)
                if 0 <= next_row < 8 and 0 <= next_col < 8:
                    next_cell = self.game.board[next_row][next_col]
                    if isinstance(next_cell, Piece) and next_cell.color != self.color:
                        result.append((pos, next_pos))
                elif self.game.en_passant and pos[0] == self.game.en_passant[0] and pos[1] + i == self.game.en_passant[1]:
                    result.append((pos, next_pos))

        return result

class Knight(Piece):
    def __init__(self, game, color, position=None):
        super().__init__(game, color, 2)
        self.notation = 'N'

    def movement(self, player, pos, capture=True):
        result = []
        for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x < 8 and 0 <= y < 8 and (not isinstance(self.game.board[x][y], Piece) or self.game.board[x][y].value * player < 0):
                result.append((pos, (x, y)))
        return result

class Bishop(Piece):
    def __init__(self, game, color, position=None):
        super().__init__(game, color, 3)
        self.notation = 'B'

    def movement(self, player, pos, capture=True):
        result = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
        for dx, dy in directions:
            x, y = pos
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break  # Out of board
                next_cell = self.game.board[x][y]
                if not isinstance(next_cell, Piece):  # Empty cell
                    result.append((pos, (x, y)))
                elif next_cell.color != self.color:  # Opponent's piece
                    result.append((pos, (x, y)))
                    break
                else:
                    break  # Own piece blocking
        return result

class Rook(Piece):
    def __init__(self, game, color, position=None):
        super().__init__(game, color, 4)
        self.notation = 'R'
        
    def movement(self, player, pos, capture=True):
        result = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Vertical and horizontal directions
        for dx, dy in directions:
            x, y = pos
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break  # Out of board
                next_cell = self.game.board[x][y]
                if not isinstance(next_cell, Piece):  # Empty cell
                    result.append((pos, (x, y)))
                elif next_cell.color != self.color:  # Opponent's piece
                    result.append((pos, (x, y)))
                    break
                else:
                    break  # Own piece blocking
        return result

    def move(self, player, from_pos, to_pos):
        move_result = super().move(from_pos, to_pos)
        if move_result:
            # Check if a rook is moved from its initial position
            if from_pos == (7 if player == -1 else 0, 0) or from_pos == (7 if player == -1 else 0, 7):
                if from_pos == (7 if player == -1 else 0, 0) and isinstance(self.game.board[7 if player == -1 else 0][0], Piece) and self.game.board[7 if player == -1 else 0][0].value == -4:  # Black rook
                    self.game.castling[1] = 0  # Disabling queen-side castling for black
                elif from_pos == (7 if player == -1 else 0, 7) and isinstance(self.game.board[7 if player == -1 else 0][7], Piece) and self.game.board[7 if player == -1 else 0][7].value == -4:  # Black rook
                    self.game.castling[0] = 0  # Disabling king-side castling for black
                elif from_pos == (0 if player == 1 else 7, 0) and isinstance(self.game.board[0 if player == 1 else 7][0], Piece) and self.game.board[0 if player == 1 else 7][0].value == 4:  # White rook
                    self.game.castling[1] = 0  # Disabling queen-side castling for white
                elif from_pos == (0 if player == 1 else 7, 7) and isinstance(self.game.board[0 if player == 1 else 7][7], Piece) and self.game.board[0 if player == 1 else 7][7].value == 4:  # White rook
                    self.game.castling[0] = 0  # Disabling king-side castling for white
        return move_result

class Queen(Piece):
    def __init__(self, game, color, position=None):
        super().__init__(game, color, 5)
        self.notation = 'Q'

    def movement(self, player, pos, capture=True):
        bishop_moves = Bishop(self.game, self.color).movement(player, pos, capture)
        rook_moves = Rook(self.game, self.color).movement(player, pos, capture)
        return bishop_moves + rook_moves

class King(Piece):
    def __init__(self, game, color, position=None):
        super().__init__(game, color, 6)
        self.notation = 'K'

    def movement(self, player, pos, capture=True):
        result = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # All directions
        for dx, dy in directions:
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                next_cell = self.game.board[x][y]
                if not isinstance(next_cell, Piece) or next_cell.color != self.color:
                    result.append((pos, (x, y)))
        return result

    def move(self, player, from_pos, to_pos):
        move_result = self.game.move((self.game.board[from_pos[0]][from_pos[1]], from_pos, to_pos))
        if move_result:
            # Disabling castling when the king is moved
            if from_pos == (7 if player == -1 else 0, 4):  # Initial position of the king
                self.game.castling[0] = 0  # Disabling king-side castling
                self.game.castling[1] = 0  # Disabling queen-side castling
        return move_result
