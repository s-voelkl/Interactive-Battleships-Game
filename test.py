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
min_diagonal_distance1, _, _ = get_min_distances_between_ships(ship1, ship2)
print("distance:", min_diagonal_distance1)
print("worst case", result1)

print()
ship3 = Ship(3, 5, 5, 10, 12, 2)
ship4 = Ship(4, 9, 9, 20, 24, 3)
result2 = determine_ship_hit(game, ship3, ship4)
min_diagonal_distance2, min_vertical_distance2, min_horizontal_distance2 = (
    get_min_distances_between_ships(ship3, ship4)
)

print("distance (diagonal):", min_diagonal_distance2)
print("distance (vertical):", min_vertical_distance2)
print("distance (horizontal):", min_horizontal_distance2)
print("medium case", result2)


print()
ship5 = Ship(2, 0, 0, 0, 1, 2)
ship6 = Ship(5, 2, 2, 0, 4, 5)
result3 = determine_ship_hit(game, ship5, ship6)
min_diagonal_distance3, _, _ = get_min_distances_between_ships(ship5, ship6)

print("distance:", min_diagonal_distance3)
print("best case", result3)


print("\n\ndetermine_max_directional_ship_movement")
print("only south with 1")
determine_max_directional_ship_movement(
    game, Ship(5, 0, 0, 0, 4), determine_max_ship_movement(5)
)

print("only north with 3")
determine_max_directional_ship_movement(
    game, Ship(2, 5, 5, 8, 9), determine_max_ship_movement(2)
)

print("east and west with 2, start and end swapped")
determine_max_directional_ship_movement(
    game, Ship(3, 12, 10, 5, 5), determine_max_ship_movement(3)
)

print("north with 3 and south with 2, start and end swapped")
determine_max_directional_ship_movement(
    game, Ship(2, 5, 5, 7, 6), determine_max_ship_movement(2)
)

print("\n\ndetermine_if_ship_crash")
print(
    "no crash, as too far distanced: ",
    determine_if_ship_crash(Ship(5, 0, 0, 0, 4), Ship(2, 5, 5, 7, 8)),
)
print(
    "no crash, as diagonally aligned: ",
    determine_if_ship_crash(Ship(5, 0, 0, 0, 4), Ship(2, 1, 2, 5, 5)),
)
print(
    "crash as vertically == 1 and horizontally == 0 aligned: ",
    determine_if_ship_crash(Ship(5, 0, 0, 0, 4), Ship(2, 1, 2, 3, 3)),
)
print(
    "crash as vertically == 0 and horizontally == 1 aligned: ",
    determine_if_ship_crash(Ship(5, 0, 0, 0, 4), Ship(2, 0, 0, 5, 6)),
)
print(
    "crash as vertically == 0 and horizontally == 0 aligned: ",
    determine_if_ship_crash(Ship(5, 0, 0, 0, 4), Ship(2, 0, 0, 4, 5)),
)
print(
    "crash as completely aligned: ",
    determine_if_ship_crash(Ship(5, 0, 0, 0, 4), Ship(5, 0, 0, 0, 4)),
)

print("\n\nact_single_ship_movement - normal movement")
act_single_ship_movement(game, Ship(5, 0, 0, 0, 4), 2, 1)

print("act_single_ship_movement - crash happening in the same row")
game.ingame_players[0].ships.append(Ship(3, 0, 0, 6, 7, 2))
act_single_ship_movement(game, Ship(5, 0, 0, 0, 4), 2, 1)
