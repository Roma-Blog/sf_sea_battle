import re
    
class Cell:
    __char = 'O'
    __state = None

    @property
    def get_char(self):
        return self.__char
    
    @property
    def get_state(self):
        return self.__state

    @get_state.setter
    def set_state(self, state):

        self.__state = state

        if state == 'ship':
            self.__char = '■'
        elif state == 'ship_nearby':
            self.__char = '-'


class PlayengField:
    __playing_field: list
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__playing_field = self.__generate_playing_field()

    def __generate_playing_field(self):
        list_cell: list = []
        for row in range(self.__height):
            list_cell.append([Cell() for i in range(self.__width)])
        return list_cell
    
    @property
    def get_playing_field(self):
        return self.__playing_field
    
    @property
    def get_width(self):
        return self.__width
    
    @property
    def get_height(self):
        return self.__height
    

class Canvas:
    
    @staticmethod
    def draw_canvas(playing_field: PlayengField):
        first_row = [i for i in range(1, playing_field.get_width + 1)]
        colum = iter(range(1, playing_field.get_height + 1))

        print(' ',*first_row, sep = '|', end = '|\n')
        for row in playing_field.get_playing_field:
            print(next(colum),'|', end = '', sep = '')
            for cell in row:
                print(cell.get_char, end='|')
            print()


class Ship:
    def __init__(self, size: int, count: int):
        self.__size = size
        self.__count = count

    @property
    def get_size(self):
        return self.__size
    
    @property
    def get_count(self):
        return self.__count


class Game:
    
    __ship_list = []
    __fleet = {}

    def __init__(self, ships: list, canvas: Canvas):
        for ship in ships:
            self.__fleet[ship.get_size] = ship.get_count
        self.__canvas = canvas

    def __coordinates_validate(self, coordinates: str, size: int, direction: str, playing_field: PlayengField):
        format = re.fullmatch(r'[0-9],[0-9]', coordinates)
        coordinate_limits = False

        if format:
            coor = list(map(lambda cor: int(cor) - 1, coordinates.split(',')))

            if coor[0] <= playing_field.get_height and coor[1] <= playing_field.get_width:
                if direction == 'h':
                    if coor[1] + size <= playing_field.get_height:
                        coordinate_limits = True
                else:
                    if coor[0] + size <= playing_field.get_width:
                        coordinate_limits = True
            else:
                return False
            
            for i in range(size):
                if direction == 'h':
                    if playing_field.get_playing_field[coor[0]][coor[1] + i].get_state is not None:
                        return False
                else:
                    if playing_field.get_playing_field[coor[0] + i][coor[1]].get_state is not None:
                        return False

        return coordinate_limits and format

    @staticmethod
    def __change_status_around(playing_field: PlayengField, x: int, y: int):
        for _x in range(-1, 2):
            for _y in range(-1, 2):
                try:
                    no_ship = playing_field.get_playing_field[x + _x][y + _y].get_state !='ship'
                    cell_available = x + _x >= 0 and y + _y >= 0

                    if cell_available and no_ship:
                        playing_field.get_playing_field[x + _x][y + _y].set_state = "ship_nearby"

                except IndexError:
                    pass #Хитрый ход что бы необрабатывать выход за границы поля

    def __deliver_ship(self, size: int, playing_field: PlayengField, direction: str = 'h'):

        self.__canvas.draw_canvas(playing_field)

        print('Куда поставить корабль?\n')
        if direction == 'h':
            print(direction)
            print( '■','|■' * (size-1), sep="", end= "\n\n")
        else:
            print(direction)
            print('■\n' * size, end= "\n\n") 

        comand = input('Напишите координаты погоризонтали потом вертикали(так: 1,1), если нужно развернуть корабли напишите "R":')
        
        if comand == 'R' or comand == 'r':
            self.__deliver_ship(size, playing_field, 'v' if direction == 'h' else 'h')
        else:
            if self.__coordinates_validate(comand, size, direction, playing_field):
                coor = list(map(lambda item: int(item) - 1, comand.split(',')))
                for i in range(size):
                    if direction == 'h':
                        playing_field.get_playing_field[coor[0]][coor[1] + i].set_state ='ship'
                        self.__change_status_around(playing_field, coor[0], coor[1] + i)
                    else:
                        playing_field.get_playing_field[coor[0] + i][coor[1]].set_state ='ship'
                        self.__change_status_around(playing_field, coor[0] + i, coor[1])
                    
                                                                                 
            else:
                print('Неверная команда!!! Либо вы указали несущестующие координаы\nили часть коробля попала за пределы поля.')
                self.__deliver_ship(size, playing_field, direction)

    def arrange_ships(self, playing_field: PlayengField, for_ai: bool = False):
        for ship in self.__fleet.keys():
            for i in range(self.__fleet[ship]):
                if not for_ai:
                    self.__deliver_ship(ship, playing_field)
                else:
                    pass

    @property
    def get_big_ship(self):
        return self.__big_ship
    
    @property
    def get_medium_ship(self):
        return self.__medium_ship
    
    @property
    def get_small_ship(self):
        return self.__small_ship

    