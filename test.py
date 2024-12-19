from ui import *
import os

os.system("")

# test_colors_and_styling()


from interaction import *


ship1 = Ship(5, 0, 0, 0, 4, 1)
ship2 = Ship(2, 9, 9, 22, 24, 2)
game = Game()
game.set_quick_start_settings()

result1 = determine_ship_hit(game, ship1, ship2)
print("distance:", get_min_diagonal_distance_between_ships(ship1, ship2))
print("worst case", result1)

print()
ship3 = Ship(3, 5, 5, 10, 12, 2)
ship4 = Ship(4, 9, 9, 20, 24, 3)
result2 = determine_ship_hit(game, ship3, ship4)
print("distance:", get_min_diagonal_distance_between_ships(ship3, ship4))
print("medium case", result2)


print()
ship3 = Ship(2, 0, 0, 0, 1, 2)
ship4 = Ship(5, 2, 2, 0, 4, 5)
result3 = determine_ship_hit(game, ship3, ship4)
print("distance:", get_min_diagonal_distance_between_ships(ship3, ship4))
print("best case", result3)
