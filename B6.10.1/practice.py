class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def get_info(self):
        return self.width * self.height
    
    def __repr__(self):
        return f'{__class__.__name__} {str((self.x, self.y, self.width, self.height))}'

rect = Rectangle(3, 4, 10, 20)

print(repr(rect), '=', rect.get_info())