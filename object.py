import re, random, os
from sys import platform
    
class Cell:
    __char = 'O'
    __status = None

    @property
    def get_char(self):
        return self.__char
    
    @property
    def get_status(self):
        return self.__status

    @get_status.setter
    def set_status(self, status):

        self.__status = status

        if status == 'ship':
            self.__char = '■'
        elif status == 'ship_nearby':
            self.__char = '-'
        elif status == 'downed':
            self.__char = 'X'
        elif status == 'past':
            self.__char = 'T'

    @get_char.setter
    def set_char(self, char):
        self.__char = char


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
    def draw_playing_field(playing_field: PlayengField):
        first_row = [i for i in range(1, playing_field.get_width + 1)]
        colum = iter(range(1, playing_field.get_height + 1))

        print(' ',*first_row, sep = '|', end = '|\n')
        for row in playing_field.get_playing_field:
            print(next(colum),'|', end = '', sep = '')
            for cell in row:
                print(cell.get_char, end='|')
            print()

    @staticmethod
    def clear_console():
        if platform == "linux" or platform == "linux2":
            os.system('clear')
        elif platform == "win32":
            clear = lambda: os.system('cls')
            clear()

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

    __fleet = {}

    def __init__(self, ships: list, canvas: Canvas):
        for ship in ships:
            self.__fleet[ship.get_size] = ship.get_count
        self.__canvas = canvas

    def __coordinates_validate(self, coordinates: str, size: int, direction: str, playing_field: PlayengField):
        if re.fullmatch(r'[0-9],[0-9]', coordinates):
            coor = list(map(lambda cor: int(cor) - 1, coordinates.split(',')))
            try:
                for i in range(size):
                    x = coor[0] + i if direction == 'v' else coor[0]
                    y = coor[1] + i if direction == 'h' else coor[1]
                    if playing_field.get_playing_field[x][y].get_status is not None:
                            return False
                return True 
            except IndexError:
                return False
        else:
            return False

    @staticmethod
    def __change_status_around(playing_field: PlayengField, x: int, y: int):
        for _x in range(-1, 2):
            for _y in range(-1, 2):
                try:
                    no_ship = playing_field.get_playing_field[x + _x][y + _y].get_status !='ship'
                    cell_available = x + _x >= 0 and y + _y >= 0

                    if cell_available and no_ship:
                        playing_field.get_playing_field[x + _x][y + _y].set_status = "ship_nearby"

                except IndexError:
                    pass #Хитрый ход что бы необрабатывать выход за границы поля
    
    def __place_ship_on_playing(self, playing_field: PlayengField, size: int, direction:str, x: int, y: int):
        for i in range(size):
            _x = x + i if direction == 'v' else x
            _y = y + i if direction == 'h' else y

            playing_field.get_playing_field[_x][_y].set_status = 'ship'
            self.__change_status_around(playing_field, _x, _y)
      

    def __deliver_ship(self, size: int, playing_field: PlayengField, direction: str = 'h'):

        self.__canvas.clear_console()
        self.__canvas.draw_playing_field(playing_field)

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
                self.__place_ship_on_playing(playing_field, size, direction, coor[0], coor[1])                                                                         
            else:
                print('Неверная команда!!! Либо вы указали несущестующие координаы\nили часть коробля попала за пределы поля.')
                self.__deliver_ship(size, playing_field, direction)

    def __deliver_ship_ai(self, size: int, playing_field: PlayengField):
        random_coor: list
        random_direction: str
        sorting_coordinates = True

        while sorting_coordinates:
            random_coor = [random.randint(1, playing_field.get_width + 1), random.randint(1, playing_field.get_height + 1)]
            random_direction = 'h' if random.randint(0, 2) else 'v'
            sorting_coordinates = not self.__coordinates_validate(','.join(list(map(str, random_coor))), size, random_direction, playing_field)
        
        self.__place_ship_on_playing(playing_field, size, random_direction, random_coor[0] - 1, random_coor[1] - 1)        

    @staticmethod
    def replacing_character(playing_field: PlayengField, char_old: str, char_new: str):
        for row in playing_field.get_playing_field:
            for cell in row:
                if cell.get_char == char_old:
                    cell.set_char = char_new


    def arrange_ships(self, playing_field: PlayengField, for_ai: bool = False):
        for ship in self.__fleet.keys():
            for i in range(self.__fleet[ship]):
                if not for_ai:
                    self.__deliver_ship(ship, playing_field)
                else:
                    self.__deliver_ship_ai(ship, playing_field)

    @staticmethod
    def __validation_shot_coordinates(coordinates: str, playing_field: PlayengField):
        if re.fullmatch(r'[0-9],[0-9]', coordinates):
            coor = list(map(lambda cor: int(cor) - 1, coordinates.split(',')))
            try:
                status_cell = playing_field.get_playing_field[coor[0]][coor[1]].get_status
                if status_cell == 'downed' or status_cell == 'past':
                    return False
                return True 
            except IndexError:
                return False
        else:
            return False

    @staticmethod
    def __shot(playing_field: PlayengField, x: int, y: int):
        playing_field.get_playing_field[x][y].set_status = 'downed' if playing_field.get_playing_field[x][y].get_status =='ship' else 'past'
            

    def player_move(self, playing_field_pl: PlayengField, playing_field_ai: PlayengField):
        print('Игра', end = '\n\n')
        print('Ваши корабли:')
        self.__canvas.draw_playing_field(playing_field_pl)
        print('\nКорабли противника:')
        self.__canvas.draw_playing_field(playing_field_ai)
        print()
        coor = input('Введите координаты (пример 1,1) куда выстрелить: ')

        while not self.__validation_shot_coordinates(coor, playing_field_ai):
            coor = input('Введите координаты (пример 1,1) куда выстрелить: ')

        coor = list(map(lambda cor: int(cor) - 1, coor.split(',')))
        self.__shot(playing_field_ai, coor[0], coor[1])

    def ai_move(self, playing_field: PlayengField):
        random_coor = [random.randint(0, playing_field.get_width), random.randint(0, playing_field.get_height)]

        while not self.__validation_shot_coordinates(','.join(list(map(lambda a: str(a + 1), random_coor))), playing_field):
            random_coor = [random.randint(0, playing_field.get_width), random.randint(0, playing_field.get_height)]

        self.__shot(playing_field, random_coor[0], random_coor[1])

    @staticmethod
    def checking_victory(playing_field: PlayengField, message: str):
        cell_ship = 0
        for row in playing_field.get_playing_field:
            for cell in row:
                if cell.get_status == 'ship':
                    cell_ship += 1
        
        if cell_ship == 0:
            print(message)
            return True

        return False
    
    @property
    def get_big_ship(self):
        return self.__big_ship
    
    @property
    def get_medium_ship(self):
        return self.__medium_ship
    
    @property
    def get_small_ship(self):
        return self.__small_ship

    