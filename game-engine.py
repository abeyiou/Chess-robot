import chess
from stockfish import Stockfish

def gameHandler(game_board, score_array, turn):
    if game_board.is_game_over():
        return gameFinisher(score_array, turn)
    elif game_board.is_check():
        if turn == "user":
            print("Computer is in check!")
        elif turn == "bot":
            print("You're in check!")
        return False

def gameFinisher(score_array, winner):
    score_array.append(winner)
    if winner == "tie":
        print("It's a tie!")
    else:
        print(f"Checkmate! The winner of this match is {winner}!")
    return True

def main():
    exe_path = "stockfish-windows-x86-64-avx2.exe"
    difficulty_selected = False
    game_end = False
    program_end = False
    game_score = []

    starting_difficulty = {
        'easy': 0,
        'medium': 10,
        'hard': 20
    }

    while not difficulty_selected:
        difficulty = input("Please choose your difficulty (easy, medium, hard): ").lower()
        if difficulty in starting_difficulty:
            difficulty_selected = True
        else:
            print("Invalid difficulty. Please try again.\n")

    stockfish = Stockfish(path=exe_path)
    stockfish.set_skill_level(starting_difficulty[difficulty])
    board = chess.Board()

    while not program_end:
        if not game_end:
            print("Current Board:\n")
            print(board)

            user_move = input("\nEnter your move in algebraic notation (or 'exit' to exit): ").strip()

            if user_move.lower() == 'exit':
                program_end = True
                continue
            
            try:
                user_move = board.parse_san(user_move)
            except ValueError:
                print("Invalid move format. Please try again.")
                continue
            
            if user_move not in board.legal_moves:
                print("Illegal move. Please try again.")
                continue

            board.push(user_move)
            print(f"\nYour move: {user_move}\n")
            print(board)

            game_end = gameHandler(board, game_score, "user")

            stockfish.set_fen_position(board.fen())
            bot_move = stockfish.get_best_move()
            
            if not bot_move:
                game_end = gameFinisher(game_score, "tie")
                continue

            bot_move = chess.Move.from_uci(bot_move)
            bot_move_san = board.san(bot_move)
            board.push(bot_move)
            print(f"\nBot's move: {bot_move_san}\n")

            game_end = gameHandler(board, game_score, "bot")

        else:
            response = input("Would you like to play another game? (Type 'yes' or 'no'): ")
            while True:
                if response.lower() == "yes":
                    board.reset()
                    print("Resetting the chess board...")
                    game_end = False
                    break
                elif response.lower() == "no":
                    program_end = True
                    break
                else:
                    print("Sorry, Please try again: ")

    print("\nThanks for playing!")
    if(len(game_score) != 0):
        print("Score record for this session: " + str(game_score))

if __name__ == "__main__":
    main()