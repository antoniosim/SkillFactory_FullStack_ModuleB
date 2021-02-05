import random


def choose_side():
    while True:
        next_move = input('Давай сыграем! Выбери свою сторону X/O [Выход - Q]: ')
        if next_move == 'X':
            print('Хорошо, ты играешь за крестики. Твой ход будет первым!')
            break
        elif next_move == 'O':
            print('Хорошо, ты играешь за нолики. Ходить первым буду я!')
            break
        elif next_move == 'Q':
            print('До новых встреч. Сыграем в другой раз.')
            break
        else:
            print('Сделай адекватный выбор, пожалуйста!')
    return next_move


def draw_board():
    print(' Текущая ситуация на поле')
    print(' ------- ------- ------- ')
    print('|      7|      8|      9|')
    print('|   ', board[7], '   |   ', board[8], '   |   ', board[9], '   |', sep='')
    print('|       |       |       |')
    print(' ------- ------- ------- ')
    print('|      4|      5|      6|')
    print('|   ', board[4], '   |   ', board[5], '   |   ', board[6], '   |', sep='')
    print('|       |       |       |')
    print(' ------- ------- ------- ')
    print('|      1|      2|      3|')
    print('|   ', board[1], '   |   ', board[2], '   |   ', board[3], '   |', sep='')
    print('|       |       |       |')
    print(' ------- ------- ------- ')


def comp_choice(playboard):  # выбор хода компьютером
    available_cells = set([i for i, v in enumerate(playboard) if v == ' '])
    
    #проверка возможности победить следующим ходом
    
    for i in range(3):  # проверка горизонтальных линий на возможность победить
        all_cells = set([j + 1 + i * 3 for j, x in enumerate(playboard[i * 3 + 1:i * 3 + 4])])
        own_cells = set([j + 1 + i * 3 for j, x in enumerate(playboard[i * 3 + 1:i * 3 + 4]) \
                          if playboard[0][1] and x == 'X' or not playboard[0][1] and x == 'O'])
        if len(own_cells) == 2 and len(available_cells.intersection(all_cells)) > 0: # в линии два значка
            fix_cells = available_cells.intersection(all_cells.difference(own_cells))
            return list(fix_cells)[0]

    for i in range(3):  # проверка вертикальных линий на возможность победить
        all_cells = set([j * 3 + i + 1 for j, x in enumerate(playboard[i + 1::3])])
        own_cells = set([j * 3 + i + 1 for j, x in enumerate(playboard[i + 1::3]) \
                          if playboard[0][1] and x == 'X' or not playboard[0][1] and x == 'O'])
        if len(own_cells) == 2 and len(available_cells.intersection(all_cells)) > 0:  # в линии два значка
            fix_cells = available_cells.intersection(all_cells.difference(own_cells))
            return list(fix_cells)[0]
    
    # проверка диагонали 1 на возможность победить
    all_cells = {1, 5, 9}
    own_cells = set([j*4 + 1 for j, x in enumerate(playboard[1::4]) \
                      if playboard[0][1] and x == 'X' or not playboard[0][1] and x == 'O'])
    if len(own_cells) == 2 and len(available_cells.intersection(all_cells)) > 0:  # в линии два значка
        fix_cells = available_cells.intersection(all_cells.difference(own_cells))
        return list(fix_cells)[0]

    # проверка диагонали 2 на возможность победить
    all_cells = {3, 5, 7}
    own_cells = set([j * 2 + 3 for j, x in enumerate(playboard[3:8:2]) \
                      if playboard[0][1] and x == 'X' or not playboard[0][1] and x == 'O'])
    if len(own_cells) == 2 and len(available_cells.intersection(all_cells)) > 0:  # в линии два значка
        fix_cells = available_cells.intersection(all_cells.difference(own_cells))
        return list(fix_cells)[0]

    # проверка возможности проиграть следующим ходом

    for i in range(3):  # проверка горизонтальных линий на возможность проиграть
        all_cells = set([j + 1 + i * 3 for j, x in enumerate(playboard[i * 3 + 1:i * 3 + 4])])
        own_cells = set([j + 1 + i * 3 for j, x in enumerate(playboard[i * 3 + 1:i * 3 + 4]) \
                          if playboard[0][1] and x == 'O' or not playboard[0][1] and x == 'X'])
        if len(own_cells) == 2 and len(available_cells.intersection(all_cells)) > 0:  # в линии два значка
            fix_cells = available_cells.intersection(all_cells.difference(own_cells))
            return list(fix_cells)[0]

    for i in range(3):  # проверка вертикальных линий на возможность проиграть
        all_cells = set([j * 3 + i + 1 for j, x in enumerate(playboard[i + 1::3])])
        own_cells = set([j * 3 + i + 1 for j, x in enumerate(playboard[i + 1::3]) \
                          if playboard[0][1] and x == 'O' or not playboard[0][1] and x == 'X'])
        if len(own_cells) == 2 and len(available_cells.intersection(all_cells)) > 0:  # в линии два значка
            fix_cells = available_cells.intersection(all_cells.difference(own_cells))
            return list(fix_cells)[0]

    # проверка диагонали 1 на возможность проиграть
    all_cells = {1, 5, 9}
    own_cells = set([j * 4 + 1 for j, x in enumerate(playboard[1::4]) \
                      if playboard[0][1] and x == 'O' or not playboard[0][1] and x == 'X'])
    if len(own_cells) == 2 and len(available_cells.intersection(all_cells)) > 0:  # в линии два значка
        fix_cells = available_cells.intersection(all_cells.difference(own_cells))
        return list(fix_cells)[0]

    # проверка диагонали 2 на возможность проиграть
    all_cells = {3, 5, 7}
    own_cells = set([j * 2 + 3 for j, x in enumerate(playboard[3:8:2]) \
                      if playboard[0][1] and x == 'O' or not playboard[0][1] and x == 'X'])
    if len(own_cells) == 2 and len(available_cells.intersection(all_cells)) > 0:  # в линии два значка
        fix_cells = available_cells.intersection(all_cells.difference(own_cells))
        return list(fix_cells)[0]
        
    # Попытаемся занять один из углов, если они свободны
    corners = list(available_cells.intersection({1, 3, 7, 9}))
    if corners:
        return random.choice(corners)
    
    # Занимаем центр, если он свободен
    if 5 in available_cells:
        return 5
    
    # Попытаемся занять одну из сторон
    sides = list(available_cells.intersection({2, 4, 6, 8}))
    if sides:
        return random.choice(sides)


def check_finish(playboard):
    res = 0
    
    if not [cell for cell in playboard if cell == ' ']:  # проверка заполнения всех ячеек
        res = 2
    
    for i in range(3):  # проверка горизонтальных линий
        if playboard[i * 3 + 1] == playboard[i * 3 + 2] == playboard[i * 3 + 3] != ' ':
            res = 3 if playboard[0][1] and playboard[i * 3 + 1] == 'X' else 1
    
    for i in range(3):  # проверка вертикальных линий
        if playboard[i + 1] == playboard[i + 4] == playboard[i + 7] != ' ':
            res = 3 if playboard[0][1] and playboard[i + 1] == 'X' else 1
    
    # проверка диагонали 1
    if playboard[1] == playboard[5] == playboard[9] != ' ':
        res = 3 if playboard[0][1] and playboard[1] == 'X' else 1

    # проверка диагонали 2
    if playboard[3] == playboard[5] == playboard[7] != ' ':
        res = 3 if playboard[0][1] and playboard[3] == 'X' else 1
    
    return res


print('Играем в Крестики-нолики. Добро пожаловать!\n')

while True:
    game_result = 0
    # первый элемент (чей следующий ход: комп/игрок - 0/1, какой значок у игрока: 0/1 - O/X)
    board = [[0, 0], ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    player_side = 0
    start_choice = choose_side()
    if start_choice == 'O':
        board[0] = [0, 0]  # игрок за нолики, ходит комп
    elif start_choice == 'X':
        board[0] = [1, 1]  # игрок за крестики, ходит игрок
    else:
        break  # выбрана опция выхода
    draw_board()
    
    while True:  # цикл одной игры
        
        if board[0][1]:
            while True:
                try:
                    player_move = int(input('Выбери ячейку для хода: '))
                    if all([player_move > 9, player_move < 1]):
                        print('Нужно ввести целое число от 1 до 9!')
                    elif board[int(player_move)] != ' ':
                        print('Для хода необходимо выбирать свободную ячейку')
                    else:
                        break
                except:
                    print('Нужно ввести целое число от 1 до 9!')
                    
            
            if board[0][0]:
                board[int(player_move)] = 'X'
            else:
                board[int(player_move)] = 'O'
        else:
            comp_move = comp_choice(board)
            print('Я выбираю ячейку', comp_move)
            if board[0][0]:
                board[int(comp_move)] = 'O'
            else:
                board[int(comp_move)] = 'X'
        
        game_result = check_finish(board)
        
        if board[0][0]:
            draw_board()
        
        if game_result == 1:
            print('Ты проиграл! В следующий раз должно получиться')
            break
        elif game_result == 2:
            print('У нас ничья! Можно попробовать ещё раз')
            break
        elif game_result == 3:
            print('Ты выиграл! Давай сыграем ещё разок?')
            break
        else:
            board[0][1] = 0 if board[0][1] == 1 else 1