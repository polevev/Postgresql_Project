import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.players_table import *
from tables.Country_table import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        pt = PlayersTable()
        ctt = CountryTable()
        ctt.create()
        pt.create()
        return

    def db_drop(self):
        pt = PlayersTable()
        ctt = CountryTable()
        pt.drop()
        ctt.drop()
        return

    def db_insert_somethings(self):
        pt = PlayersTable()
        ctt = CountryTable()
        ctt.insert_one(['РУС', 'Россия', 'Сибирь'])
        ctt.insert_one(['США', 'Америка', 'Колорадо'])
        ctt.insert_one(['ЯПН', 'Япония', 'Хоккайдо'])
        ctt.insert_one(['ГРМ', 'Германия', 'Саксония'])
        ctt.insert_one(['ИТЛ', 'Италия', 'Романья'])
        pt.insert_one(['Сергиенко', 'Дмитрий', 1, 1])
        pt.insert_one(['Смит', 'Джон', 2, 2])
        pt.insert_one(['Ким', 'Джи-Хью', 3, 3])
        pt.insert_one(['Патчел', 'Расуль', 4, 4])
        pt.insert_one(['Грация', 'Леонардо', 5, 5])
        pt.insert_one(['Иванов', 'Алексей', 1, 4])
        pt.insert_one(['Джонсон', 'Майкл', 2, 5])

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр стран;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def show_country(self):
        self.ID = None
        menu = """Просмотр списка стран!
    №\tНазвание страны\tРегион"""
        print(menu)
        lst = CountryTable().all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3]))
        menu = """Дальнейшие операции: 
        0 - возврат в главное меню;
        3 - добавление новой страны;
        4 - удаление страны;
        5 - просмотр национальных игроков;
        9 - выход."""
        print(menu)
        return

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def delete_country(self):
        data = input("Введите номер строки, на которой находится страна: (0 - отмена): ").strip()
        if data == "0":
            return
        while len(data) == 0 or not(data.isdigit()) or not(CountryTable().find_by_position(int(data))):
            if len(data.strip()) == 0: string = 'Пустое значение!'
            elif not(data.isdigit()): string = 'Номер строки это число!'
            else: string = 'Ввели неправильный номер строки!'
            data = input(f"{string} Введите номер строки заново (0 - отмена): ").strip()
            if data == "0":
                return
        CountryTable().delete_by_ID(int(data))

    def add_country(self):
        data = []
        data.append(input("Ввведите код страны(3 заглавные буквы) (0 - отмена): ").strip())
        if data[0] == '0':
            return
        while len(data[0]) == 0 or len(data[0]) > 3:
            if len(data[0]) == 0:
                string = "Код страны не может быть пустым!"
            elif len(data[0]) > 3:
                string = "Код страны не превышает 3 символов!"
                data.pop()
                data = data[:-1]
            data.append(input(f"{string} Введите название кода страны заново (0 - отмена): ").strip())
            if data[0] == "0":
                return

        data.append(input("Ввведите название страны (0 - отмена): ").strip())
        if data[1] == '0':
            return
        while len(data[1]) == 0 or len(data[1]) > 30:
            if len(data[1]) == 0:
                string = "Название страны не может быть пустым!"
            elif len(data[1]) > 30:
                string = "Название страны не превышает 30 символов!"
                data.pop()
                data = data[:-1]
            data.append(input(f"{string} Введите название страны заново (0 - отмена): ").strip())
            if data[1] == "0":
                return

        data.append(input("Ввведите название региона страны (0 - отмена): ").strip())
        if data[2] == '0':
            return
        while len(data[2]) == 0 or len(data[2]) > 20 or CountryTable().select_by_name(data[2]):
            if len(data[2]) == 0:
                string = "Название региона страны не может быть пустым!"
            elif len(data[2]) > 20:
                string = "Название региона страны не превышает 20 символов!"
            else:
                string = "Такой регион уже  существует!"
                data.pop()
                data = data[:-1]
            data.append(input(f"{string} Введите название региона страны заново (0 - отмена): ").strip())
        if data[2] == "0":
            return
        CountryTable().insert_one(data)

    def after_show_country(self, next_step):
        while True:
            if next_step == "4":
                self.delete_country()
                return "1"
            elif next_step == "3":
                self.add_country()
                return "1"
            elif next_step == "5":
                cur = self.show_players_by_country()
                next_step = self.after_show_people(cur)
            elif next_step != "0" and next_step != "9" and next_step != "1":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def after_show_people(self, next_step):
        while True:
            if next_step == "6":
                self.add_players()
            elif next_step == "7":
                self.delete_players()
            elif next_step != "0" and next_step != "1" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
            else:
                return next_step
            return "5"

    def show_players_by_country(self):
        data = input("Укажите номер страны, в которой записаны интересующие вас игроки (0 - отмена):")
        if data == '0':
            return '1'
        while len(data) == 0 or not (data.isdigit()) or not (CountryTable().find_by_position(int(data))):
            if len(data.strip()) == 0:
                string = 'Пустое значение!'
            elif not (data.isdigit()):
                string = 'Номер строки это число!'
            else:
                string = 'Ввели неправильный номер строки!'
            data = input(f"{string} Введите номер строки заново (0 - отмена): ").strip()
            if data == "0":
                return
        th = CountryTable().select_by_id(data)
        self.c_id = th[0]
        self.c_name = th[1]
        print("Выбрана страна: " + self.c_name)
        print("Национальные игроки:")
        lst = PlayersTable().all_by_Country_id(self.c_id)
        menu = "№\tФамилия\tИмя"
        print(menu)
        for i in lst:
            print(str(i[0]), str(i[1]), str(i[2]))
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр стран;
    6 - добавление нового игрока;
    7 - удаление игрока;
    9 - выход."""
        print(menu)
        return self.read_next_step()

    def delete_players(self):
        data = input("Введите номер строки, на которой находится игрок: (0 - отмена): ").strip()
        if data == "0":
            return
        while len(data) == 0 or not (data.isdigit()) or not (PlayersTable().select_by_id(int(data))):
            if len(data.strip()) == 0:
                string = 'Пустое значение!'
            elif not (data.isdigit()):
                string = 'Номер строки это число!'
            else:
                string = 'Ввели неправильный номер строки!'
            data = input(f"{string} Введите номер строки заново (0 - отмена): ").strip()
            if data == "0":
                return
        PlayersTable().delete_by_ID(int(data))
        return "5"
    def add_players(self):
        data = input("Укажите номер страны, в которую вы хотите добавить игрока (0 - отмена):")
        if data == '0':
            return '1'
        while len(data) == 0 or not (data.isdigit()) or not (CountryTable().find_by_position(int(data))):
            if len(data.strip()) == 0:
                string = 'Пустое значение!'
            elif not (data.isdigit()):
                string = 'Номер строки это число!'
            else:
                string = 'Ввели неправильный номер строки!'
            data = input(f"{string} Введите номер строки заново (0 - отмена): ").strip()
            if data == "0":
                return
        th = CountryTable().select_name_by_id(int(data))
        print("Выбрана страна: " + th[0])
        bet = []
        bet.append(input("Укажите имя игрока:"))
        while len(bet[0]) == 0 :
            if len(bet[0].strip()) == 0:
                string = 'Пустое значение!'
            bet.append(input(f"{string} Введите имя заново (0 - отмена): "))
            if bet[0] == "0":
                return

        bet.append(input("Укажите фамилию игрока:"))
        while len(bet[1]) == 0:
            if len(bet[1].strip()) == 0:
                string = 'Пустое значение!'
            bet.append(input(f"{string} Введите фамилию заново (0 - отмена): "))
            if bet[1] == "0":
                return
        bet.append(data)
        PlayersTable().add_by_Country_id(int(data), bet)
        return "5"
    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_country()
                next_step = self.read_next_step()
                current_menu = self.after_show_country(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.add_country()
                current_menu = "1"
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# для теста
# соединения с БД
#m.test()
m.main_cycle()
    
