from object import *

canvas = Canvas()
playeng_field = PlayengField(6, 6)
playeng_field_ai = PlayengField(6, 6)

# big_ship это корабли на 3 ячейки, medium_ship это корабли на 2, small_ship это корабли на 1
big_ship = Ship(3,1)
medium_ship = Ship(2,2)
small_ship = Ship(1,3)

fleet = [big_ship, medium_ship, small_ship]

game = Game(fleet, canvas)

win = True

game.arrange_ships(playeng_field)
game.replacing_character(playeng_field, '-', 'O')
game.arrange_ships(playeng_field_ai, for_ai=True)
game.replacing_character(playeng_field_ai, '-', 'O')
game.replacing_character(playeng_field_ai, '■', 'O')

while win:
    canvas.clear_console()
    game.player_move(playeng_field, playeng_field_ai)
    if game.checking_victory(playeng_field_ai, '!!! -> Вы выиграли <- !!!'):
        win = False
        break
    game.ai_move(playeng_field)
    if game.checking_victory(playeng_field, '!!! -> Компьютер победил <- !!!'):
        win = False
        break
    