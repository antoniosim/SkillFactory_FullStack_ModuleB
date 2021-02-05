from math import pi


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def get_area_rec(self):
        return self.width * self.height


class Square:
    def __init__(self, side):
        self.side = side
    
    def get_area_sqr(self):
        return self.side ** 2


class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def get_area_cir(self):
        return pi * self.radius ** 2