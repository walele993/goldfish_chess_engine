from board import Chess
from rules import is_checkmate
from ai import AI

def main():
    print("Welcome to Goldfish!\n")
    
    while True:
        print("Select game mode:\n[1] Fight the Goldfish\n[2] Two Player")
        choice = input("Enter your choice: ")
        if choice == "1":
            play_with_ai()
            break
        elif choice == "2":
            play_two_players()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.\n")

def play_with_ai():
    game = Chess()
    ai = AI(game, -1)
    game.display()
    while not is_checkmate(game, game.p_move):
        if game.p_move == ai.color:
            ai.make_move()
        else:
            play_turn(game, player="human")

def play_two_players():
    game = Chess()
    game.display()
    while not is_checkmate(game, game.p_move):
        play_turn(game, player="human")

def parse_move(game, move_str):
    from_square = (8 - int(move_str[1]), ord(move_str[0]) - ord('a'))
    to_square = (8 - int(move_str[3]), ord(move_str[2]) - ord('a'))
    piece = game.board[from_square[0]][from_square[1]]
    if piece == 0:
        return None, from_square, to_square
    return piece, from_square, to_square

def play_turn(game, player=None):
    while True:
        player_color = "white" if game.p_move == 1 else "black"
        print(f"\n{player_color.capitalize()}'s turn")
        
        move_str = input("Enter your move (e.g. e2e4), 'undo' to undo last move, or 'exit' to quit: ")
        
        if move_str.lower() == 'exit':
            game.exit_game()
        
        if move_str.lower() == 'undo':
            game.undo_last_move()
            game.display()
            continue
        
        if len(move_str) == 4:
            if move_str[0] in 'abcdefgh' and move_str[1] in '12345678' and \
               move_str[2] in 'abcdefgh' and move_str[3] in '12345678':
                
                move = parse_move(game, move_str)
                
                if move is not None:
                    try:
                        # Passa il parametro player solo se è il turno dell'umano
                        game.move(move, player=player)
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
