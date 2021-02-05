import pickle

class Guest:
    
    def __init__(self):
        self.last_name =  input('Введите фамилию: ')
        self.first_name = input('Введите имя    : ')
        self.city = input('Введите город  : ')
        self.status = input('Введите статус : ')
        
    # вывод данных о госте
    def show_info(self):
        return f'{self.first_name} {self.last_name}, г. {self.city}, статус "{self.status}"'


class DataBase:
    
    def __init__(self, filename):
        self.__path = filename
        self.__id = 0
        self.data = {}
        self.load_db()
    
    def load_db(self):
        try:
            with open(self.__path, 'rb') as f:
                self.data = pickle.load(f)
        except:
            self.data = {}
        self.__id = len(self.data)
    
    def save_db(self):
        try:
            with open(self.__path, 'wb') as f:
                pickle.dump(self.data, f)
                return True
        except:
            return False
            
    
    def add_Нguest(self, Guest):
        self.__id += 1
        self.data[self.__id] = Guest
    
    def guest_list(self):
        res = ''
        for guest in self.data.values():
            res += guest.show_info() + '\n'
        return res


db = DataBase('GuestsList.pydb')
new_guests = False

while input('Хотите добавить нового гостя? [Y-Да]: ') == 'Y':
    print('НОВЫЙ ГОСТЬ'.center(60,'-'))
    db.add_guest(Guest())
    print('-'*60,'\n')
    new_guests = True

if input('Вывести информацию о гостях? [Y-Да]: ') == 'Y':
    print('')
    print('СПИСОК ГОСТЕЙ'.center(60,'='))
    print(db.guest_list())

if new_guests and input('Сохранить в БД информацию о новых гостях? [Y-Да]: ') == 'Y' and db.save_db():
    print('БАЗА ДАННЫХ СОХРАНЕНА В ФАЙЛ'.center(60,'-'))