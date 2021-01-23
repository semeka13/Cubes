def load_level(filename):
    filename = "../levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    new_level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    print(new_level)
    return new_level


load_level('level_test')
load_level('level_1')