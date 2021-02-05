import random
import time

E = ' - '  # обозначение пустой клетки
S = ' + '  # обозначение клетки с выстрелом
D = '[ ]'  # обозначение палубы корабля
W = '[+]'  # обозначение раненного корабля
K = '[X]'  # обозначение убитого корабля


#   при создании объекта класса указывается размер игрового поля
#   получаемый объект представляет собой список из двух списков
#   (0 - поле игрока, 1 - поле компьютера). Каждое из полей содержит
#   список списков с ячейками поля, нулевые строки и столбы содержат заголовки

class BattleField:
    
    def __init__(self):
        #   выбор размера поля
        while True:
            size = input('Укажи размер поля от 5 до 15: ')
            try:
                if int(size) > 15:
                    print('Побереги глаза, играть будем два дня!')
                elif int(size) < 5:
                    print('А стоит ли вообще начинать?')
                else:
                    self.scale = int(size)
                    break
            except (TypeError, ValueError):
                print('Надо ввести число от 5 до 15')
        
        #   добавление типов кораблей в игру
        self.ship_types = [0, 0, 0, 0]
        while True:
            for ship_type in range(4):
                while True:
                    ship_quantity = input(f'Укажи количество {ship_type + 1}-палубных кораблей: ')
                    try:
                        if not (0 <= int(ship_quantity) <= 5):
                            print('Не думаю, что это хорошая идея!\n')
                        else:
                            self.ship_types[ship_type] = int(ship_quantity)
                            break
                    except (TypeError, ValueError):
                        print('Количество кораблей надо указывать цифрами\n')
            ships_total = 0
            for i in self.ship_types:
                ships_total += i
            if ships_total > 4:
                break
            else:
                print(f'А стоит ли вообще начинать? Всего {ships_total}? Это несерьёзно!\n')
                continue
                
            
            
        
        print(f'\nТипы кораблей заданы! В игре {self.scale}x{self.scale} участвуют:')
        for ship_type in range(4):
            print(f'{ship_type + 1}-палубных кораблей - {self.ship_types[ship_type]} ед.')
        
        #   список координат кораблей для каждого игрока
        #   в каждом из списков будут храниться записи для кораблей
        #   каждая запись корабля это набор списков палуб,
        #   каждый из которых содержит статус палубы и её координаты
        self.ships = [[], []]
        
        self.field = [[], []]  # поле игрока и компьютера соответственно
        
        # заполнение списка нулевой строки - заголовка
        for field_num in (0, 1):
            new_row = ['   ']
            for i in range(1, self.scale + 1):
                new_row.append(str(i).center(3, ' '))
            
            self.field[field_num].append(new_row)
            
            # заполнение остальных строк, где 0-й символ - буква
            for i in range(0, self.scale):
                new_row = [chr(65 + i).center(3, ' ')]  # добавление буквы в 0-й символ
                for j in range(1, self.scale + 1):  # заполнение ряда начальными элементами
                    new_row.append(E)
                self.field[field_num].append(new_row)
    
    #   вывод игрового поля
    def show_field(self, show_both):
        print('\n')

        header = 'ВАШЕ ПОЛЕ'.center((self.scale + 1) * 3, '=')
        if show_both:
            header += ' ' * 12 + 'ПОЛЕ ПРОТИВНИКА'.center((self.scale + 1) * 3, '=')
            
        print(header)
        
        for x in range(self.scale + 1):
            print_row = ''.join(self.field[0][x])
            if show_both:
                print_row += ' ' * 12 + ''.join(self.field[1][x])
            print(print_row)
    
    #   конвертация координат формата буква-цифра в кортеж
    def convert_str_address(self, address_str):
        try:
            letter = address_str[0]
            digits = address_str[1:]
            x = ord(letter.upper()) - 64
            y = int(digits)
            if any([x < 1, x > self.scale + 1, y < 1, y > self.scale + 1]):
                raise TypeError
        except IndexError:
            raise ValueError('Необходимо указать полные координаты')
        except ValueError:
            raise ValueError('Формат координат БУКВАЧИСЛО')
        except TypeError:
            raise ValueError('Координаты выходят за пределы поля')
        else:
            return x, y

    #   конвертация координат из кортежа в строку
    @staticmethod
    def convert_dig_address(address_tpl):
        letter = chr(address_tpl[0] + 64).upper()
        digits = str(address_tpl[1])
        if not digits:
            raise ValueError('Неполные координаты!')
        return letter + digits
    
    #   установление значения ячейки поля по кортежу координат
    def set_cell_value(self, field_num, address, value):
        try:
            self.field[field_num][address[0]][address[1]] = value
        except IndexError:
            pass
    
    #   получение значения ячейки поля по кортежу координат
    def get_cell_value(self, field_num, address):
        try:
            res = self.field[field_num][address[0]][address[1]]
        except IndexError:
            res = None
        return res
    
    #   проверка ячеек корабля и радиуса в 1 ячейку на нахождение в пределах поля и доступность для размещения
    def check_position(self, field_num, new_ship):
        res = True
        for one_deck in new_ship.decks:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    #   если соседняя ячейка за пределами поля - пропускаем
                    if any([one_deck[1][0] + dx > self.scale, one_deck[1][0] + dx < 1,
                            one_deck[1][1] + dy > self.scale, one_deck[1][1] + dy < 1]):
                        if all([dx == 0, dy == 0]):
                            res = False
                            break
                        else:
                            continue
                    #   если ячейка в пределах поля - проверяем на пустоту
                    else:
                        res = self.get_cell_value(field_num, (one_deck[1][0] + dx, one_deck[1][1] + dy)) == E
                        if not res:
                            break
                if not res:
                    break
            if not res:
                break
        return res
    
    #   добавление корабля на карту и в список играющих кораблей
    def add_ship(self, field_num, new_ship):
        if not (0 < new_ship.x <= self.scale):
            raise ValueError('Первая координата неверная')
        elif not (0 < new_ship.y <= self.scale):
            raise ValueError('Вторая координата неверная')
        elif not self.check_position(field_num, new_ship):
            raise ValueError('Тут нельзя разместить корабль')
        else:
            self.ships[field_num].append(new_ship.decks)
            #   на карту наносятся только корабли игрока
            for one_deck in new_ship.decks:
                self.set_cell_value(field_num, one_deck[1], D)
    
    #   изменение статуса палубы корабля
    def set_ship_deck(self, field_num, address, value):
        for one_ship in self.ships[field_num]:
            for one_deck in one_ship:
                if one_deck[1] == address:
                    one_deck[0] = value
    
    #   автоматическая расстановка кораблей
    def place_ships_randomly(self, field_num):
        tries = 0
        for ship_type in enumerate(self.ship_types):
            for i in range(ship_type[1]):
                while True:
                    coord_x = random.choice(range(1, self.scale + 1))
                    coord_y = random.choice(range(1, self.scale + 1))
                    vector = random.choice((False, True))
                    size = ship_type[0] + 1
                    ship_to_add = BattleShip(coord_x, coord_y, size, vector)
                    try:
                        self.add_ship(field_num, ship_to_add)
                    except ValueError:
                        tries += 1
                        if tries > 100000:
                            raise OverflowError(
                                'Слишком сложно расставить корабли, попробуйте задать другие параметры...\n')
                        else:
                            continue
                    else:
                        break
        if field_num:  # если это поле противника, то затираем значения после расстановки кораблей
            for i in range(1, self.scale + 1):
                for j in range(1, self.scale + 1):
                    self.field[1][i][j] = E
    
    #   ручная расстановка кораблей
    def place_ships_manually(self):
        self.show_field(False)
        for ship_type in enumerate(self.ship_types):
            for i in range(ship_type[1]):
                while True:  # цикл для установки корабля
                    
                    while True:  # цикл для получения точки установки корабля
                        try:
                            selected_address = input(f'Укажи координаты установки {ship_type[0] + 1}'
                                                     f'-палубного корабля [Q - заново]: ')
                            if selected_address == 'Q':
                                raise OverflowError('Что ж, попробуем ещё раз...\n')
                            ship_bow = self.convert_str_address(selected_address)
                            break
                        except ValueError as ex:
                            print(ex)
                    
                    ship_len = ship_type[0] + 1
                    if ship_len > 1:
                        direct = input(f'Установить корабль вертикально? [+/-]: ')
                        ship_dir = direct == '+'
                    else:
                        ship_dir = True
                    ship_to_add = BattleShip(ship_bow[0], ship_bow[1], ship_len, ship_dir)
                    
                    try:
                        self.add_ship(0, ship_to_add)
                    except ValueError as err:
                        print(err)
                        continue
                    else:
                        print(f'Корабль установлен в точку {selected_address.upper()} \n')
                        self.show_field(False)
                        break
    
    #   получение целеуказания от игрока
    def player_aims(self):
        selected_address = input(f'Укажи координаты выстрела: ')
        while True:  # цикл для получения координат выстрела
            try:
                aim_address = self.convert_str_address(selected_address)
                if self.get_cell_value(1, aim_address) == S:
                    selected_address = input('Там точно никого нет, нужна другая цель: ')
                    continue
                elif self.get_cell_value(1, aim_address) == W:
                    selected_address = input('Даже если попасть дважды, он не утонет - попробуй рядом: ')
                    continue
                elif self.get_cell_value(1, aim_address) == K:
                    selected_address = input('Неплохой контрольный выстрел, давай поищем новую жертву: ')
                    continue
                else:
                    break
            except ValueError as err:
                print(err)
                selected_address = input(f'Укажи координаты выстрела: ')
        return aim_address
    
    #   получение целеуказания от компьютера
    def computer_aims(self):
        aim_address = None
        free_cells = []  # список доступных для выстрела ячеек
        near_cells = []  # список ячеек с ранеными кораблями
        for row in range(1, self.scale + 1):
            for col in range(1, self.scale + 1):
                if self.get_cell_value(0, (row, col)) in (E, D):
                    free_cells.append((row, col))
                elif self.get_cell_value(0, (row, col)) == W:
                    near_cells.append((row, col))
        
        #   если нет ячеек с ранеными кораблями, то выбирает случайную из свободных
        if not near_cells:
            aim_address = random.choice(free_cells)
        else:
            
            #   если раненая одна, то выбираем любую свободную соседнюю ячейку по прямой
            if len(near_cells) == 1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        neighbor_cell = near_cells[0][0] + dx, near_cells[0][1] + dy
                        if self.get_cell_value(0, neighbor_cell) in (E, D) and (dx == 0 or dy == 0):
                            aim_address = neighbor_cell
            
            #   если раненых несколько, то выбираем продолжение общей координате
            else:
                x = near_cells[0][0]
                y = near_cells[0][1]
                in_horizontal = [cell for cell in near_cells if cell[0] == x]
                in_vertical = [cell for cell in near_cells if cell[1] == y]
                
                # продвигаемся по горизонтали
                if len(in_horizontal) == len(near_cells):
                    for x in (near_cells[0][1] - 1, near_cells[-1][1] + 1):
                        neighbor_cell = (near_cells[0][0], x)
                        if self.get_cell_value(0, neighbor_cell) in (E, D):
                            aim_address = neighbor_cell
                            break
                
                # продвигаемся по вертикали
                elif len(in_vertical) == len(near_cells):
                    for x in (near_cells[0][0] - 1, near_cells[-1][0] + 1):
                        neighbor_cell = (x, near_cells[0][1])
                        if self.get_cell_value(0, neighbor_cell) in (E, D):
                            aim_address = neighbor_cell
                            break
                else:
                    aim_address = random.choice(free_cells)
        return aim_address
    
    #   расчёт успешности выстрела
    def shot_success(self, field_num, aim):
        shot_result = 0
        self.set_cell_value(field_num, aim, S)
        for ship_idx, ship_ent in enumerate(self.ships[field_num]):
            decks = len(ship_ent)
            shots = 0
            for one_deck in ship_ent:  # проверяем палубы корабля на координаты и попадания
                if one_deck[0] == W:  # если статус "ранен", то добавляем попадание
                    shots += 1
                if one_deck[1] == aim:  # если координаты совпали, то устанавливаем статус "ранен"
                    one_deck[0] = W
                    shots += 1
                    self.set_cell_value(field_num, one_deck[1], W)
                    shot_result = 1
            
            if decks == shots:  # если количество палуб = количеству попаданий - статус "убит"
                for one_deck in ship_ent:
                    self.set_cell_value(field_num, one_deck[1], K)
                    shot_result = 2
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            #   отмечаем соседние ячейки как отстрелянные
                            neighbor_cell = one_deck[1][0] + dx, one_deck[1][1] + dy
                            if self.get_cell_value(field_num, neighbor_cell) == E:
                                self.set_cell_value(field_num, neighbor_cell, S)
                
                self.ships[field_num].pop(ship_idx)  # удаление корабля из списка кораблей
                if not len(self.ships[field_num]):
                    shot_result = 3
            
            if shot_result:
                break
        
        return shot_result


# при создании корабля указываются координаты его носа, длина и направление
# возвращаемому объекту присваивается свойство decks, которое
# представляет собой список из кортежа с координатами каждой палубы и её состоянием
class BattleShip:
    
    def __init__(self, x, y, size=1, horizontal=True):
        self.x = x
        self.y = y
        self.decks = []
        
        if horizontal:
            for i in range(size):
                self.decks.append([D, (x + i, y)])
        else:
            for i in range(size):
                self.decks.append([D, (x, y + i)])


print('Добро пожаловать в игру "Морской бой"\n')

#   ОБЩИЙ ЦИКЛ ИГРЫ
while True:
    try:
        game_field = BattleField()
        
        #   расстановка кораблей
        if input('\nХочешь расставить корабли самостоятельно [+/-]? ') == '+':
            game_field.place_ships_manually()
        else:
            print('\nСлучайная расстановка твоих кораблей...')
            time.sleep(2)
            game_field.place_ships_randomly(0)
        
        print('\nРасстановка кораблей противника...\n\n')
        time.sleep(2)
        game_field.place_ships_randomly(1)
    except OverflowError as e:
        print(e)
        continue
    
    print('\n[Противник]: Нас атакуют, все по местам, отбить атаку!\n')
    game_field.show_field(True)
    #   цикл обмена выстрелами до победы
    while True:
        player_shot = 1
        comp_shot = 1
        
        #   стреляет игрок
        while 0 < player_shot < 3:
            new_shot = game_field.player_aims()
            print(f'\n[Наводчики]: Запускаем ракету по координатам {game_field.convert_dig_address(new_shot)} ...')
            player_shot = game_field.shot_success(1, new_shot)
            #time.sleep(2)
            
            if player_shot == 1:
                print('[Наводчики]: Корабль подбит, но ещё на плаву! Надо добивать!!!')
                game_field.show_field(True)
            elif player_shot == 2:
                print('[Наводчики]: Корабль потоплен, команда в шлюпках! Давай ещё раз жахнем!')
                game_field.show_field(True)
            elif player_shot == 3:
                print('\n' * 3,
                      'Лучшего морского волка в наших землях не сыскать! С ПОБЕДОЙ!'.center(game_field.scale * 8, '='),
                      '\n' * 3)
                break
            else:
                print('[Наводчики]: Командир, там никого не было! По нам стреляют!')
            
            if player_shot == 3:
                break
        
        if player_shot == 3:
            break
        
        #   стреляет компьютер
        while 0 < comp_shot < 3:
            print("\n[Противник]: Орудие к бою! Пли!")
            new_shot = game_field.computer_aims()
            print(f'[Противник]: Ракета запущена в квадрат {game_field.convert_dig_address(new_shot)} ...')
            comp_shot = game_field.shot_success(0, new_shot)
            #time.sleep(2)
            
            if comp_shot == 1:
                print('[Противник]: Получи! Скоро добью его, будь уверен')
            elif comp_shot == 2:
                print('[Противник]: Пошёл на дно с отрицательным дифферентом!')
            elif comp_shot == 3:
                print('\n' * 3,
                      'Командир, нашего флота больше нет, налегайте на вёсла!'.center(game_field.scale * 8, '='),
                      '\n' * 3)
                break
            else:
                print('[Противник]: Что-то мой радар барахлит, или может это всё туман!')
            
        if comp_shot == 3:
            break
        else:
            game_field.show_field(True)
            
    #   дезавуирование оставшихся кораблей противника
    for ship in game_field.ships[1]:
        for deck in ship:
            game_field.set_cell_value(1, deck[1], deck[0])
    
    game_field.show_field(True)
    
    #  запрос на повторную игру
    while True:
        once_more = input('\nХочешь сыграть ещё раз? [+/-]: ')
        if once_more not in ('+', '-'):
            print('\nТебе придётся принять решение!')
        elif once_more == '-':
            print('\n\nНадеюсь тебе понравилось! До новых встреч')
            exit(0)
        else:
            break