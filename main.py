from src.game import Game, Human, BLACK, WHITE

player1 = Human('Me')
player2 = Human('You')

game = Game(6, player1, player2, WHITE)


while True:
    game.next_action()
