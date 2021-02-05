class Cat:
    def __init__(self, name, sex, age):
        self.name = name
        self.sex = sex
        self.age = age
    
    def get_info(self):
        return ['Имя: '+self.name + '\n'
                'Пол: '+self.sex + '\n'
                'Возраст: '+self.age]