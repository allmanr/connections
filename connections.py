import os
import sys

YELLOW = 0
GREEN = 1
BLUE = 2
PURPLE = 3

COLOR_CHARS = ['y', 'g', 'b', 'p']


ANSWERS = ['a', 'a', 'a', 'a',
           'b', 'b', 'b', 'b',
           'c', 'c', 'c', 'c',
           'd', 'd', 'd', 'd']

SUBMIT_GUESS = -101

MAX_MISTAKES = 4


def get_color_list(guess_set: dict) -> list:
        return [c.color for c in guess_set.values()]


class Tile:
    def __init__(self, text: str, color: str) -> None:
        self.text = text
        self.color = color
        self.selected = False
        self.has_been_solved = False


class Board:
    def __init__(self, tiles: list[Tile]) -> None:
        self.tiles = tiles
        self.number_selected = 0
        self.selected_tiles = dict()
        self.mistake_count = 0
        self.guess_history = []
        self.colors_solved = list()
        self.game_over = False

    def print_board(self) -> None:
        for i, tile in enumerate(self.tiles):
            if i%4 == 0:
                print()

            print(tile.text, tile.color, tile.selected, tile.has_been_solved, "    ")

        print("\nMistakes remaining: {}".format(4 - self.mistake_count))

    def handle_game_over(self) -> bool:
        win = bool()
        # Win case
        if self.mistake_count < 4:
            print("You win!")
            win = True
        else:
            print("You suck!")
            win = False

        self.print_guesses()

        return win

    def print_guesses(self):
        for guess in self.guess_history:
            print(get_color_list(guess))
    
    def update(self) -> bool:
        self.print_board()

        if self.game_over:
            self.handle_game_over()

    def process_guess(self) -> bool:
        if self.number_selected != 4:
            return False
        
        self.guess_history.append(self.selected_tiles)

        colors = [c.color for c in self.selected_tiles.values()]

        print("guess submitted: ", colors)

        # This check determines whether the guess was successful
        if colors.count(colors[0]) == len(colors):
            self.colors_solved.append(colors[0])
            # Clears guess history
            self.process_correct_guess()
            return True
        # Incorrect guess case
        else:
            self.mistake_count += 1
            if self.mistake_count == MAX_MISTAKES:
                self.game_over = True
            # Guess was processed successfully - return true
            return True

    def process_correct_guess(self):
        for i in self.selected_tiles.keys():
            self.tiles[i].selected = False
            self.tiles[i].has_been_solved = True
        
        self.number_selected = 0
        self.selected_tiles.clear()

        if len(self.colors_solved) == MAX_MISTAKES:
            self.game_over = True

    def select_tile(self, index: int) -> bool:
        if index < 0 or index > 15:
            raise ValueError
        
        tile = self.tiles[index]
        currently_selected = tile.selected

        # De-select tile if currently selected
        if currently_selected:
            self.tiles[index].selected = False
            # Remove from selected list and update count
            self.selected_tiles.pop(index)
            self.number_selected -= 1
            # DEBUG
            assert self.number_selected == len(self.selected_tiles)
            # Return True - operation succeeded
            return True
        
        # Only select if user hasn't already selected 4 tiles
        elif self.number_selected < 4:
            self.tiles[index].selected = True
            # Update selected_tiles dict with index (from total board) as key
            self.selected_tiles[index] = self.tiles[index]
            self.number_selected += 1
            return True
        
        else:
            # Return False - operation did not succeed
            return False
        



class ConnectionsGame:
    def __init__(self, answer_key: list) -> None:
        self.answers = answer_key
        self.tiles = list()
        self.create_tiles()

        self.board = Board(self.tiles)
        self.color_map = dict()
        self.color_map = self.initialize_color_map()

        self.mistakes_remaining = 4
        self.guess_history = list(list())
    
    def initialize_color_map(self):
        for i, set in enumerate(self.answers):
            for a in set:
                self.color_map[a] = COLOR_CHARS[i%4]

    def create_tiles(self):
        for i, set in enumerate(self.answers):
            for a in set:
                self.tiles.append(Tile(a, COLOR_CHARS[int(i / 4)]))

    def user_input(self, selection: int):
        if self.board.select_tile(selection):
            # self.update_board()
            pass

    def process_guess(self):
        if self.board.process_guess():
            self.update_board()

        if self.board.game_over:
            self.board.handle_game_over()

    def update_board(self):
        self.board.update()


def user_input_simulator(g: ConnectionsGame, commands: list):
    for cmd in commands:
        if type(cmd) == int:
            g.user_input(cmd)
        elif cmd == 'g':
            g.process_guess()


def main():
    G = ConnectionsGame(ANSWERS)
    """
    G.user_input(1)
    G.user_input(6)
    G.user_input(15)
    G.user_input(8)
    G.user_input(8)
    G.user_input(9)
    print(G.board.selected_tiles.items())
    G.user_input(0)
    G.user_input(1)
    G.user_input(2)
    G.user_input(5)
    G.process_guess()
    """
    user_input_simulator(G, [0, 1, 2, 3, 'g',
                             4, 5, 6, 7, 'g',
                             8, 9, 10, 11, 'g',
                             12, 13, 14, 15, 'g'])


if (__name__ == '__main__'):
    sys.exit(main())