class BoardClass:
    """A simple class to store and handle information about BoardClass.

        Attributes:
            own: Own username
            other: The other player's username
            last_player (str): Username of the last player to have a turn
            num_win (int): Number of wins
            num_tie (int): Number of ties
            num_loss (int): Number of losses
            move_index(int): The index on the board of the player's move
            board([str]): An empty board
    """

    def __init__(self, own: str = "", other: str = "", last_player: str = "", num_win: int = 0, num_tie: int = 0, num_loss: int = 0, move_index: int = 100,
                 board: [str] = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], total: int = 0) -> None:
        """Make a BoardClass.

        Args:
            own: Own username
            other: The other player's username
            last_player: Username of the last player to have a turn
            num_win: Number of wins
            num_tie: Number of ties
            num_loss: Number of losses
            board([str]): An empty board
            move_index(int): The index on the board of the player's move
            total: Number of total games played
        """
        self.own = own
        self.other = other
        self.last_player = last_player
        self.num_win = num_win
        self.num_tie = num_tie
        self.num_loss = num_loss
        self.move_index = move_index
        self.board = board
        self.total = total

    def updateGamesPlayed(self) -> None:
        """Keep track how many games have started."""
        self.total += 1

    def resetGameBoard(self) -> None:
        """Clear all the moves from game board."""
        # use when finish one round and want to start over
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    def updateGameBoard(self) -> None:
        """Update the game board with the player's move."""
        if self.last_player == 'player2':
            x_or_o = 'O'
        else:
            x_or_o = 'X'
        self.board[self.move_index] = x_or_o
        print(
            f"{self.board[0]}|{self.board[1]}|{self.board[2]}\n-+-+-\n{self.board[3]}|{self.board[4]}|{self.board[5]}\n-+-+-\n{self.board[6]}|{self.board[7]}|{self.board[8]}")


    def isWinner(self) -> bool:
        """Check if the latest move resulted in a win and update the wins and losses count."""
        if self.board[0] == self.board[1] == self.board[2] != ' ' or self.board[3] == self.board[4] == self.board[5] != ' ' or \
                self.board[6] == self.board[7] == self.board[8] != ' ':
            #check if the horizontal line has the same elements
            if self.last_player == self.other:
                #if the game ends at the other player's side, result in a loss
                self.num_loss += 1
            else:
                #if the game ends at current player's side, result in a win
                self.num_win += 1
            return True
        elif self.board[0] == self.board[3] == self.board[6] != ' ' or self.board[1] == self.board[4] == self.board[7] != ' ' or \
                self.board[2] == self.board[5] == self.board[8] != ' ' :
            # check if the vertical line has the same elements
            if self.last_player == self.other:
                # check if the game ends at the other player's side, if so, result in a loss
                self.num_loss += 1
            else:
                # if the game ends at current player's side, result in a win
                self.num_win += 1
            return True
        elif self.board[0] == self.board[4] == self.board[8] != ' ' or self.board[2] == self.board[4] == self.board[6] != ' ':
            #check if the diagonal line has the same elements
            if self.last_player == self.other:
                # check if the game ends at the other player's side, if so, result in a loss
                self.num_loss += 1
            else:
                # if the game ends at current player's side, result in a win
                self.num_win += 1
            return True
        else:
            return False

    def boardIsFull(self) -> bool:
        """Check if the board is full (I.e. no more moves to make - tie) and update the ties count."""
        full = True
        for element in self.board:
            if element == ' ':
                full = False
        if full == True:
            self.num_tie += 1
        return full

    def printStats(self) -> None:
        """Prints the following each on a new line:
        Print:
            the players' username
            the username of the last person to make a move
            the number of games
            the number of wins
            the number of losses
            the number of ties

        """
        print("Game over, here's your stats:)")
        print(f"User name {self.own}, today you played Tic Tac Toe with {self.other}")
        print(f"The person who made the last move is {self.last_player}")
        print(f"You played {self.total} games in total")
        print(f"You won {self.num_win} games.")
        print(f"You lost {self.num_loss} games.")
        print(f"You two has {self.num_tie} draws")
