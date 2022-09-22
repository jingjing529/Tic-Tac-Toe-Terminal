import socket
from gameboard import BoardClass


# HOST = 'localhost'  # Standard loopback interface address (localhost)
# PORT = 50000  # Port to listen on (non-privileged ports are > 1023)


def get_user_name() -> str:
    """Prompt the user for the username."""
    client_username = input("Please give yourself an awsome username:")
    while not client_username.isalnum():
        print("Error: Please enter an alphanumeric username with no special characters\n")
        client_username = input("Please give yourself an awsome username:")
    return client_username


def get_user_move() -> int:
    """Get the user's move."""
    client_move = input("Please choose a number based on the board indices to make a move:\n")
    while client_move not in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
        print("Error: Please choose a number between 0-8\n")
        client_move = input("Please choose a number based on the board indices to make a move:\n")
    return int(client_move)


def continue_or_not(P1_board, s1) -> None:
    """When a game is over, ask if the user wants to play again."""
    while True:
        y_or_n = input("This game has finished, do you want to play again? Please enter y or n\n")
        while y_or_n not in ['Y', 'y', 'N', 'n']:
            y_or_n = input("Want to play again? Please reply y for yes, n for no\n")
        if y_or_n == 'Y' or y_or_n == 'y':
            s1.sendall("Play Again".encode())
            game_started(P1_board, s1)
        else:
            s1.sendall("Fun Times".encode())
            break


def game_started(P1_board, s1) -> None:
    """Start the game."""
    board_indices = '0|1|2\n-+-+-\n3|4|5\n-+-+-\n6|7|8'
    print("Take a look at the board_indices.")
    print(board_indices)
    # print out board indices to make it clear for players to make a move
    P1_board.resetGameBoard() #to make the board clean
    P1_board.updateGamesPlayed() #once game started, update games played count
    while True:
        print("Your turn")
        client_move = get_user_move() #get player1's step
        while P1_board.board[client_move] != ' ': #check if the index on the board is taken, if so, get the move again
            print("Sorry this one has been taken.")
            client_move = get_user_move()
        P1_board.move_index = client_move
        P1_board.last_player = P1_board.own #last player is player1
        P1_board.updateGameBoard() #place player1's move on the board
        s1.sendall(str(client_move).encode()) #send player2 player1's move
        if P1_board.isWinner():
            print("Congratulations! You won!")
            break
        if P1_board.boardIsFull():
            print("Oh, it's a tie.")
            break
        print(f"{P1_board.other}'s turn")
        server_move = s1.recv(1024).decode() #get player2's step
        P1_board.move_index = int(server_move)
        P1_board.last_player = P1_board.other
        P1_board.updateGameBoard() #place player2's move on player1's board
        if P1_board.isWinner():
            print("Sorry but you lost.")
            break


def run_client() -> None:
    """Run the client's code."""
    while True:
        try:
            host_address = input("Please enter host:\n")
            host_port = int(input("Please enter port:\n"))
            print("Establishing Connection to server (HOST: {}, Port: {}".format(host_address, host_port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host_address, host_port))
            break
        except:
            response = input("Connection cannot be made, do you want to try again?\n")
            if response == 'y' or response == 'Y':
                continue
            elif response == 'n' or response == 'N':
                quit()

    client_username = get_user_name()
    s.sendall(client_username.encode())  # use .encode() when sending data
    server_username = s.recv(1024).decode()  # use .decode() when recieving data
    print("You have successfully connected to {}!".format(server_username))

    P1 = BoardClass(own=client_username, other=server_username)
    game_started(P1, s)
    continue_or_not(P1, s)
    P1.printStats()
    s.close()


if __name__ == "__main__":
    run_client()
