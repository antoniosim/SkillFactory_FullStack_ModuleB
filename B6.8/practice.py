from Classes import Cat

cats = [
    {"name": "Барон", "gender": "мальчик", "age": "2 года"},
    {"name": "Сэм", "gender": "мальчик", "age": "2 года"}]

for c in cats:
    cat = Cat(*c.values())
    print(*cat.get_info(),'\n', '*' * 10)