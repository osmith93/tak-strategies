from typing import List
from numbers import Integral

WHITE = 'white'
BLACK = 'black'
CAP = 'cap'
FLAT = 'flat'
WALL = 'wall'
STONE_TYPES = [CAP, FLAT, WALL]


class Piece:

    def __init__(self, color: str, piece_type: str = FLAT):
        assert (color in [BLACK, WHITE]), "Color must be either 'black' or 'white'."
        assert (piece_type in STONE_TYPES), "Type must be either 'cap', 'wall' or 'flat'."
        self.color: str = color
        self.type: str = piece_type

    def flatten(self):
        assert (type != CAP), 'Capstones cannot be flattened.'
        self.type = FLAT

    @property
    def is_capstone(self):
        return self.type == CAP


class Field:
    def __init__(self):
        self._stack: List[Piece] = []

    @property
    def top(self):
        return self._stack[-1]

    @property
    def empty(self) -> bool:
        return len(self._stack) == 0

    @property
    def height(self):
        return len(self._stack)

    @property
    def controlled_by(self):
        return self.top.color

    def add_stone(self, piece: Piece):
        self.add_stack([piece])

    def add_stack(self, stack: List[Piece]):
        if not self.empty:
            if stack[0].is_capstone:
                self.top.flatten()
            assert (self.top.type == FLAT), "Can only play pieces onto flat stones."
        self._stack += stack

    def take_stones(self, count: int) -> List[Piece]:
        assert (self.height >= count)
        new_stack = self._stack[-count:]
        self._stack = self._stack[:-count]
        return new_stack


class Action:
    pass


class Place(Action):
    def __init__(self, x: int, y: int, color: str, piece_type: str):
        self.piece: Piece = Piece(color, piece_type)
        self.x = x
        self.y = y

    def __str__(self):
        raise NotImplemented


class Move(Action):
    UP = 'up'
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'
    DIRECTION_DICT = {UP: (0, 1), DOWN: (0, -1), LEFT: (-1, 0), RIGHT: (1, 0)}

    def __init__(self, x: int, y: int, move_list: List[int], direction: str):
        assert (x >= 0 and y >= 0)
        assert (direction in [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT])
        assert (min(move_list) >= 0)
        self.x: int = x
        self.y: int = y
        self.move_list: List[int] = move_list
        self.direction: str = direction

    @property
    def height(self) -> int:
        return sum(self.move_list)

    @property
    def direction_vector(self):
        return Move.DIRECTION_DICT[self.direction]

    def __str__(self):
        raise NotImplemented


class Board:
    def __init__(self, size: int):
        self._size: int = size
        self._fields = [[Field() for _ in range(size)] for _ in range(size)]

    def field(self, x: int, y: int):
        assert (0 <= x < self._size) and (0 <= y < self._size)
        return self._fields[x][y]

    def apply(self, action: Action):
        if isinstance(action, Place):
            assert self.field(action.x, action.y).empty
            self.field(action.x, action.y).add_stone(action.piece)
        elif isinstance(action, Move):
            assert action.height <= self._size
            stack = self.field(action.x, action.y).take_stones(action.height)
            x = action.x
            y = action.y
            dx, dy = action.direction_vector
            for i in action.move_list:
                self.field(x, y).add_stack(stack[:i])
                stack = stack[i:]
                x += dx
                y += dy
        else:
            raise TypeError

    @property
    def full(self):
        return not any([self.field(x, y).empty for x in range(self._size) for y in range(self._size)])


class Player:
    def __init__(self):
        self.name = ""
        self.color = None

    def request_action(self) -> Action:
        raise TypeError

    def assign_color(self, color: str):
        self.color = color


class Human(Player):
    def __init__(self, name):
        self.name = name
        self.color = None

    def request_action(self) -> Action:
        x = int(input("input a column"))
        y = int(input("input a row"))
        return Place(x, y, self.color, FLAT)


class Bot(Player):
    def request_action(self) -> Action:
        pass


class Game:
    RULES = {
        3: dict(flatstones=10, capstones=0),
        4: dict(flatstones=15, capstones=0),
        5: dict(flatstones=21, capstones=1),
        6: dict(flatstones=30, capstones=1),
        7: dict(flatstones=40, capstones=2),
        8: dict(flatstones=50, capstones=2),
    }

    def __init__(self, size, player1: Player, player2: Player, starting_color: str):
        self.starting_color: str = starting_color
        self.current_player: Player = player1
        player1.assign_color(starting_color)
        player2.assign_color(BLACK if starting_color == WHITE else WHITE)
        self.players = [player1, player2]
        self._size: int = size
        self._board: Board = Board(size)
        self._pieces_left = {player1: Game.RULES[size], player2: Game.RULES[size]}

    def next_action(self):
        print(f"Player '{self.current_player.name}', please choose your next action.")
        action = self.current_player.request_action()
        self._board.apply(action)
        if isinstance(action, Place):
            stone_type = 'capstones' if action.piece.is_capstone else 'flatstones'
            assert self._pieces_left[self.current_player][stone_type] > 0
            self._pieces_left[self.current_player][stone_type] -= 1

        if self.is_game_over():
            self.evaluate_game()
        else:
            self.switch_players()

    def switch_players(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def is_game_over(self) -> bool:
        pass

    def evaluate_game(self):
        pass
