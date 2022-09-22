import socket
from gameboard import BoardClass


# HOST = 'localhost'  # Standard loopback interface address (localhost)
# PORT = 50000  # Port to listen on (non-privileged ports are > 1023)


def get_server_move() -> int:
    """Get player2's move."""
    server_move = input("Please choose a number based on the board indices to make a move:\n")
    while server_move not in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
        print("Error: Please choose a number between 0-8\n")
        server_move = input("Please choose a number based on the board indices to make a move:\n")
    return int(server_move)


def game_started(P2_board, conn1) -> None:
    """Start the game."""
    board_indices = '0|1|2\n-+-+-\n3|4|5\n-+-+-\n6|7|8'
    print("Take a look at the board_indices.")
    print(board_indices)
    # print out board indices to make it clear for players to make a move
    P2_board.resetGameBoard() #to make the board clean
    P2_board.updateGamesPlayed() #once game started, update games played count
    while True:
        print(f"{P2_board.other}'s turn")
        client_move = conn1.recv(1024).decode() #get player1's move
        P2_board.move_index = int(client_move)
        P2_board.last_player = P2_board.other #last player is player1
        P2_board.updateGameBoard() #place player1's move on player2's board
        if P2_board.isWinner():
            print("Sorry but you lost.")
            break
        if P2_board.boardIsFull():
            print("Oh, it's a tie.")
            break
        print("Your turn")
        server_move = get_server_move() #get player2's move
        while P2_board.board[server_move] != ' ': #check if the index on the board is taken, if so, get the move again
            print("Sorry this one has been taken.")
            server_move = get_server_move()
        P2_board.move_index = server_move
        P2_board.last_player = P2_board.own #last player is player2
        P2_board.updateGameBoard() #place player2's move on the board
        conn1.sendall(str(server_move).encode())
        if P2_board.isWinner():
            print("Congratulations! You won!")
            break


def run_server() -> None:
    """Run the server's code."""
    host_address = input("Please enter host:\n")
    host_port = int(input("Please enter port:\n"))
    print("Setting up server (HOST: {}, Port: {})".format(host_address, host_port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host_address, host_port))
    s.listen(1)

    conn, addr = s.accept()
    client_username = conn.recv(1024).decode()
    conn.sendall("player2".encode())
    print("You have successfully connected to {}!".format(client_username))

    P2 = BoardClass(other=client_username, own="player2")
    game_started(P2, conn)
    while True:
        P1_response = conn.recv(1024).decode()
        if P1_response == "Play Again":
            print(f"{P2.other} wants to play again")
            game_started(P2, conn)
        elif P1_response == "Fun Times":
            print("Game over, what a fun time!")
            break
    P2.printStats()
    conn.close()


if __name__ == "__main__":
    run_server()
