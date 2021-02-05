import pickle


class Account:
    
    def __init__(self):
        self.last_name =  input('Введите фамилию: ')
        self.first_name = input('Введите имя    : ')
        self.__balance = 0
        # login = input('Придумайте логин для входа: ')
        # while not login:
        #    login = input('Логин не может быть пустым: ')
        # self.__login = login
        # Account.set_password(self)
    
    # операции с балансом счёта
    @property
    def balance(self):
        return self.__balance
    
    def set_balance(self, balance):
        if isinstance(balance, int):
            self.__balance = balance
    
    # процедура установления пароля пользователя
    # def set_password(self):
    #     while True:
    #         pwd = input('Придумайте пароль для входа: ')
    #         while len(pwd) < 6:
    #             pwd = input('Пароль должен быть более 6 символов: ')
    #
    #         if pwd == raw_input('Повторите свой  пароль: '):
    #             self.__password = pwd
    #             print('Пароль установлен')
    #             break
    #         else:
    #             print('Пароли не совпадают')
    
    # вывод имени пользователя, логина и баланса
    def show_info(self):
        return f'Клиент: {f"{self.last_name} {self.first_name}".ljust(30," ")} [Баланс: {str(self.balance).rjust(6," ")} руб.]'


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
            
    
    def add_account(self, Account):
        self.__id += 1
        self.data[self.__id] = Account
    
    def client_list(self):
        res = ''
        for client in self.data.values():
            res += client.show_info() + '\n'
        return res


db = DataBase('E-Wallet.pydb')
new_users = False

while input('Хотите добавить нового клиента? [Y-Да]: ') == 'Y':
    print('НОВЫЙ КЛИЕНТ'.center(60,'-'))
    db.add_account(Account())
    print('-'*60,'\n')
    new_users = True

if input('Вывести информацию о клиентах? [Y-Да]: ') == 'Y':
    print('')
    print('ИНФОРМАЦИЯ ПО КЛИЕНТАМ'.center(60,'='))
    print(db.client_list())

if new_users and input('Сохранить в БД информацию о новых клиентах? [Y-Да]: ') == 'Y' and db.save_db():
    print('БАЗА ДАННЫХ СОХРАНЕНА В ФАЙЛ'.center(60,'-'))