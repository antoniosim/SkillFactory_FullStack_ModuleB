class Rectangle:
    def __init__(self, x, y):
        self.width = x
        self.height = y
    
    def get_area(self):
        return self.width * self.height
    
    def get_info(self):
        return __class__.__name__


rect = Rectangle(3, 4)

print(f'Класс: {rect.get_info()}, площадь: {rect.get_area()}')