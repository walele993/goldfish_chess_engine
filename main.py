from board import Chess
from rules import is_checkmate

def main():
    game = Chess()
    print("Welcome to Goldfish!")
    game.display()
    while True:
        while not is_checkmate(game, game.p_move):
            play_turn(game)

def parse_move(game, move_str):
    from_square = (8 - int(move_str[1]), ord(move_str[0]) - ord('a'))
    to_square = (8 - int(move_str[3]), ord(move_str[2]) - ord('a'))
    piece = game.board[from_square[0]][from_square[1]]
    if isinstance(piece, int):
        pass
    else:
        print("Piece at starting position:", piece, piece.color)
    return piece, from_square, to_square

def play_turn(game):
    player_color = "white" if game.p_move == 1 else "black"
    print(f"\n{player_color.capitalize()}'s turn")
    
    while True:
        move_str = input("Enter your move (e.g. e2e4): ")
        
        if len(move_str) == 4:
            if move_str[0] in 'abcdefgh' and move_str[1] in '12345678' and \
               move_str[2] in 'abcdefgh' and move_str[3] in '12345678':
                
                move = parse_move(game, move_str)
                
                if move is not None:
                    try:
                        game.move(move)
                        print("\n")
                        game.display()
                        break
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid move. Try again.")
            else:
                print("Invalid move format. Column letters should be between 'a' and 'h', and row numbers between '1' and '8'.")
        else:
            print("Invalid move format. Move should be in the format 'e2e4'.")
            
if __name__ == "__main__":
    main()