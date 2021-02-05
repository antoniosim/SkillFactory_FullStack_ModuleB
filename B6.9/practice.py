from Classes import Rectangle, Square, Circle

rect_1 = Rectangle(3, 4)
rect_2 = Rectangle(12, 5)

sqre_1 = Square(5)
sqre_2 = Square(10)

cirl_1 = Circle(3)
cirl_2 = Circle(7)

figures = [rect_1, rect_2, sqre_1, sqre_2, cirl_1, cirl_2]

for figure in figures:
    if isinstance(figure, Rectangle):
        print('Площадь прямоугольника:',figure.get_area_rec())
    elif isinstance(figure, Square):
        print('Площадь квадрата:',figure.get_area_sqr())
    else:
        print('Площадь круга:',figure.get_area_cir())