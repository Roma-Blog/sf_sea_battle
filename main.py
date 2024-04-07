from object import *

canvas = Canvas()
playeng_field = PlayengField(6, 6)

# big_ship это корабли на 3 ячейки, medium_ship это корабли на 2, small_ship это корабли на 1
big_ship = Ship(3,1)
medium_ship = Ship(2,2)
small_ship = Ship(1,3)

fleet = [big_ship, medium_ship, small_ship]

game = Game(fleet, canvas)


game.arrange_ships(playeng_field)

