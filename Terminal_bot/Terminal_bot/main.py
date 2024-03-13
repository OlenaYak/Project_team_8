from classes import Address_book, Contact, Phone, Note_book, User_Info
from sorter import start
from start import logo, simulate_loanding
from random import choice
import webbrowser
import pathlib
import pickle

# Кеш для роботи програми
user_login = None
cache = Address_book()
note_cache = Note_book()

# Функція декоратор для обробки помилок
def input_error(inner): # Помилки які можуть виникати оброблено, декоратор для непередбачуваних випадків щоб програма аварійно не завершувала роботу
    def wrap(*args):
        try:
            return inner(*args)
        except IndexError:
            return "IndexError, use command 'about' to learn about the correctness of entering commands"
        except ValueError:
            return "ValueError, use command 'about' to learn about the correctness of entering commands"
        except KeyError:
            return "KeyError, use command 'about' to learn about the correctness of entering commands"
        except TypeError:
            return "TypeError, use command 'about' to learn about the correctness of entering commands"
        except ArithmeticError:
            return "ArithmeticError, use command 'about' to learn about the correctness of entering commands"
    return wrap


@ input_error
def greeting(data): # Функція привітання 
    greeting_list = [ # Список з фраз для привітання
"Congratulations! Welcome to your personal assistant.",
"Hello, how can I help?",
"Glad to see you, let's work together.",
"Hello You look good, you have a task for me?"
]
    return(choice(greeting_list))  # Повертає випадкову фразу з списку

@ input_error
def add_contact(data): # Фукція для додавання контакту в Address_book
    name = data # Приймає один аргумент імя
    result = cache.add_contact(Contact(name)) # Додає контакт до Address_book якщо це можливо
    if result:
        return result

@ input_error    
def add_phone(data): # Функція для додавання номеру телефону в контакт
    name, phone = data # Приймає список з двох аргументів та присвоює ці аргументи змінним name та phone 
    name = name.lower().capitalize() # Імя форматується в визначений формат для запису та взаємодії
    contact = cache.search_contact(name) # Пошук контакру в кеші
    if contact is None: # Якщо контакту незнайдено нічого не відбувається
        return 
    phone = Phone(phone) # Перевірка на валідність вказаного номеру
    if phone:
        return cache[name].add_phone(phone.value) # Додавання номену телефону для контакту


@ input_error
def edit_phone(data): # Функція для редагування номеру телефона визначеного контакту
    name, old_phone, new_phone = data # Приймає сприсок з трьох аргументів та присвоює ці аргументи змінним name, old_phone та new_phone
    name = name.lower().capitalize() # Імя форматується в визначений формат для запису та взаємодії
    contact = cache.search_contact(name) # Пошук контакру в кеші
    if contact is None: # Якщо контакту незнайдено нічого не відбувається
        return 
    contact.edit_phone(old_phone,new_phone) # Викликається функція класу Contact() яка перевіряє валідність номера та заміняє старий на новий

@ input_error
def del_phone(data): # Функція для видалення номеру телефона контакту
    name, phone = data # Приймає список з двох аргументів та присвоює ці аргументи змінним name та phone 
    name = name.lower().capitalize() # Імя форматується в визначений формат для запису та взаємодії
    contact = cache.search_contact(name) # Пошук контакру в кеші
    if contact is None: # Якщо контакту незнайдено нічого не відбувається
        return 
    phone = Phone(phone) # Перевірка на валідність вказаного номеру
    if phone is None: # Якщо Переврку не пройдено функція припиняє роботу
        return 
    elif cache[name].find_phone(phone.value): # Пошук номеру нелефону в вказаному контакті
        cache[name].remove_phone(phone.value) # Якщо такий існує видаляє його
        return f'Phone: {phone.value} for contact: {name} deleted' # Повідомлення
    return f'Contact: {name} not have this phone: {phone.value}\n{cache[name]}' # Якщо такого не існує повертає повідомлення 

@ input_error
def contact_output(data): # Пошук контакту
    return cache.search_contact(data) # Повертає всю інформацію про контакт

@ input_error
def add_email(data): # Функція додавання е-пошти для контакту
    name, email = data # Приймає список з двох аргументів та присвоює ці аргументи змінним name та email
    name = name.lower().capitalize() # Імя форматується в визначений формат для запису та взаємодії
    contact = cache.search_contact(name) # Пошук контакру в кеші
    if contact is None: # Якщо контакту незнайдено нічого не відбувається
        return 
    contact.add_email(email) # Виклик функції класу Contact. Додавання е-пошти для контакту

@ input_error
def edit_email(data): # Функція для редагування е-пошти в вказаному контакті
    '''Для редагування е-пошти непотрібно вказувати стару пошту. Контакт не може мати більше ніж одну е-пошту'''
    name, new_email = data # Приймає список з двох аргументів та присвоює ці аргументи змінним name та email
    name = name.lower().capitalize() #
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.edit_email(new_email)  # Виклик функції класу Contact. Замінює стару е-пошту на нову

@ input_error
def add_address(data): # Функція для додавання адбеси для контакту 
    name, new_address = data[0] , '  '.join(i for i in data[1:]) # Приймає список з багатьма аргументами перший присвоюється для змінної name\
    name = name.lower().capitalize()                             # решту аргументів перетворює в одну строку та присвоюється для змінної new_address
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.add_address(new_address) # Виклик функції класу Contact. Додає адресу для контакту

@ input_error
def edit_address(data): # Функція для додавання нової адреси для контакту
    '''Для редагування адреси непотрібно вказувати стару пошту. Контакт не може мати більше ніж одну адресу'''
    name, new_address = data[0], ' '.join(i for i in data[1:])
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.edit_address(new_address)

@ input_error
def add_birthday(data): # Функція для додавання дня народження для контакту 
    name, birthday = data # Приймає список з двох аргументів та присвоює ці аргументи змінним name та birthday
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.add_birthday(birthday) # Виклик функції класу Contact. Перевіряє на вілідність вказаної дати та додає адресу для контакту

@ input_error
def about(data):
    commands = [['Command', 'Parameters', 'Description'],
                   ['hello', '', 'The bot greets the user'],
                   ['show all', '', 'list all information about users'],
                   ['add contact', '[Name]', 'create new user [Name] in adress book'],
                   ['del contact', '[Name]', 'remove user [Name] from adress book'],
                   ['add phone', '[Contact_id] [Phone]', 'add to user [Contact_id] a [Phone]'],
                   ['edit phone', '[Contact_id] [Phone] [new_Phone]', 'replace for user [Contact_id] a [Phone] by [new_Phone]'],
                   ['del phone', '[Name] [Phone]', 'remove phone [Phone] from user [Name]'],
                   ['add email', '[Contact_id] [Email]', 'add to user [Contact_id] an [Email]'],
                   ['edit email', '[Contact_id] [new_Email]', 'replace for user [Contact_id] by [new_Email]'],
                   ['add address', '[Contact_id] [Address]', 'set for user [Name] an address [Address]'],
                   ['edit address', '[Contact_id] [New address]', 'replace for user [Contact_id] an [New address]'],
                   ['add birthday', '[Contact_id] [Birthday]', 'set for user [Contact_id] a birthday at [Birthday]'],
                   ['next birthdays', '[int]', 'shows upcoming birthdays if exist in period from today till [int] days'],
                   ['days to birthday', '[Name]', 'shows upcoming birthdays for a contact [Name]'],
                   ['add note', '[string]', 'Add a note to Note Book'],
                   ['all notes', '', 'list all notes'],
                   ['del note', '[Title]', 'Remove [Note_id] note from Note Book'],
                   ['add tag', '[Title] [Tag]', 'add [Tag] to note [Title]'],
                   ['del tag', '[Title] [Tag]', 'remove [Tag] from note [Title]'],
                   ['find note', '[searchstring]', 'list all Notes with [searchstring] data in note and tags.[searchstring] must be 2 symbols minimum'],
                   ['find tag', '[searchstring]', 'list all Notes with [searchstring] data in tags.[searchstring] must be 2 symbols minimum'],
                   ['close, exit', '', 'exit the bot'],
                   ['about', '', 'list all bot commands'],
                   ['sort notes', '', 'sorting notes from tag'],
                   ['sorting', '[path to folder]', 'sorted files in folder by format'],
                   ['git', '', 'It will open the github page in the browser with track updates']
                   ]
    dashes = "{0:<14} + {1:50} + {2:^32} \n".format("-" * 14, "-" * 50, "-" * 32)
    help_string = ''

    for i in commands:
        help_string += f'{i[0]:^14} | {i[1]:^50} | {i[2]:^32} \n'
        help_string += dashes
    return help_string

@ input_error
def show_all(data): # Функія яка виводить в термінал всю книгу контактів
    return cache

@ input_error
def delete(data): # Функція для видалення контакту з кешу
    name = data.lower().capitalize()
    result = cache.search_contact(name)
    if result:
        cache.remove_contact(name) # Виклик функції класу Address_book яка видаляє контакт з кешу за імям
        print(f'Contact with name: {name} deleted')

@ input_error
def days_to_birthday(data): # Функція яка обчислює кількість днів до дня народження
    name = data[0].lower().capitalize()
    result = cache.search_contact(name)
    if result:
        days = result.days_to_birthday()
        result_string = f'{name}\'s birthday is in {days} days'
        if days > 1:
            print(result_string)
        else:
            print(result_string[:-1])

def next_birthdays(data): # Функція яка приймає число днів, та обчислює кількість днів до дня народження для кожного контакту,
    cache.days_to_birthday_with_days_left(data)  # якщо день народження від сьогодні до вказаної кількості днів повертає імя та кількість днів

@ input_error
def add_note(data): # Функція для створення нової нотатки
    text = ' '.join(i for i in data) # Всі аргументи які приходять в вигляді списку конкатинуються в строку
    note_cache.add_note(text) # Виклик функції класу Note_book для створення нової нотатки

@ input_error
def all_notes(data): # Функція що виводить в термінал всі існуючі нотатки
    return note_cache.__str__()

@ input_error
def del_note(data): # Функція для видалення нотатки за титулом
    title = data.lower().capitalize() # Титул форматується в визначений формат для запису та взаємодії
    notes = note_cache.search_note_with_title(title) # Виклив функції сласу Note_book для пошуку нотатки за титулом
    if notes is not str(): 
        print('{0:<70}'.format('-' * 70)) # Роздільна лінія 
        print(f'Found {len(notes)} notes with title or tag: {title}') # Інформаційна строка 
        for i in notes: # Цикл що виведе в термінал всі нотатки з даним титулом
            print(i) # Вивід однієї нотатки в термінал
            user_input = input('Delete this note?\n[input:"y"->Enter]->delete\n[Enter]->skip\n>>>')
            if user_input == 'y': #Якщо це нотатка яку користувач бажає видалити потрібно ввести в термінал 'y' та натиснути ввід
                note_cache.del_note(i) # Виклик функції класу Note_book для видалення нотатки з кешу
        return
    return notes

@ input_error
def add_tag(data): # Функція для додавання тегу в нотатку за титулом
    # !!!!!!!!!!!!!!!!!Потрібно доопрацювання є можливість існування декількох нотаток з однаковим титулом!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    title, tag = data # Приймає список з двох аргументів та присвоює ці аргументи змінним title та tag
    title = title.lower().capitalize() 
    note = note_cache.search_note_with_title(title)
    if note is not None:
        note[0].add_tag(tag) # Потрібно доопрацювати (тег буде добавлено в першу знайдену нотатку) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return f'Tag {tag} for {title}'
    return note

@ input_error
def del_tag(data): # Функція видалення тегу з нотатки за титулом
    # !!!!!!!!!!!!!!!!!Потрібно доопрацювання є можливість існування декількох нотаток з однаковим титулом!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    title, tag = data
    tag = tag .lower().capitalize()
    title = title.lower().capitalize()
    note = note_cache.search_note_with_title(title)
    if note is not None :
        note[0].remove_tag_in_note(tag) # Потрібно доопрацювати (тег буде видалено з першої знайденої нотатки) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return
    return note

@ input_error
def find_note(data): # Функцція пошуку нотатки за тегом або титулом
    title = data.lower().capitalize()
    note = note_cache.search_note_with_title(title) # Виклик функції класу Note_book для пошуку нотатки за титулом
    if note is not None:
        for n in note:
            print(n)
            return
    note = note_cache.search_note_with_tag(title) # Виклик функції класу Note_book для пошуку нотатки за тегом
    if note is not None:
        print(1)
        for n in note:
            print(n)
            return
    
@ input_error
def find_tag(data): # Функцція пошуку нотатки за тегом або тегом
    tag = data.lower().capitalize()
    note = note_cache.search_note_with_tag(tag)
    if note is not None:
        for n in note:
            print(n)

def sort_notes(data): # Виклик функції сортування нотаток за тегами (Нотатки з однаковими тегами будуть відсортовані один за одним)
    note_cache.sort_by_tags()

def sorting(data): # Функція для виклику сортувальника папок та файлів. Аргументом потрібно передати шлях до папки
    start(*data)

def create_new_user(): # Функція для створення користувача login password 
    print('Enter your login to register: ')
    new_login = input('>>>') # Ввід користувачем логіну який він хоче створити
    login_validator = True # Валідність логіну(можлива зміна на False якщо користувач з таким логіном існує)
    local_cache = None # Внутрішній кеш
    if pathlib.Path('cache.bin').exists(): # Перевірка на існування файлу з кешом
        with open('cache.bin', 'rb') as file: # Відкриття для читання файлу з кешом
            local_cache = pickle.load(file) # Дані з файлу з кешом передаються в локальну змінну
            for user in local_cache: # Цикл для перевірки кожного існуючого користувача в кеші
                if str(*user.keys()) == new_login: # Якщо введений користувачем логін вже існує в кеші валідність логіну змінюється на False
                    login_validator = False
    # Є можливість відсутності файлу з кешом в такому випадку валідність логіну завжди є True
    if login_validator:
        print('Enter new password: ')
        user_input = input('>>>')
        new_user = User_Info(new_login, user_input) # Виклик __init__ для класу User_Info в якому пароль проходить валідацію, якщо невалідний просить користувача ввести новий
        with open('cache.bin','wb') as file: # Додавання та запис нового користувача в кеш файл cache.bin(кеш з адресною книгою)
            if local_cache:
                local_cache.append({new_login:[new_user,Address_book()]})
            else:
                local_cache = [{new_login:[new_user,Address_book()]}]
            pickle.dump(local_cache, file)
        # Повторення попередніх дій з записом кешу в файл але в інший файл not_cache.bin(кеш з нотатками)
        local_note_cache = None
        if pathlib.Path('note_cache.bin').exists():
            with open('note_cache.bin', 'rb') as file:
                local_note_cache = pickle.load(file)
        if local_note_cache:
            local_note_cache.append({new_login:[new_user,Note_book()]})
        else:
            local_note_cache=[{new_login:[new_user,Note_book()]}]
        with open('note_cache.bin', 'wb') as file:
            pickle.dump(local_note_cache, file)
        print(f'New user: {new_login} created.')
        return True
    print('A user with such a login already exists')

def load_user_cache(login): # Вхід в прогаму за допомогою login та password
    local_cache = None
    password_validator = False # Валідація паролю за замовчуванням негативна
    if pathlib.Path('cache.bin').exists(): # Перевірка на існування файлу з кешом
        with open('cache.bin','rb') as file: # Відкриття для читання файлу з кешом
            local_cache = pickle.load(file) # Дані з файлу з кешом передаються в локальку змінну
    else: # Якщо кеш файлу не існує повертає повідомлення 
        print('There are currently no users')
    for user in local_cache: # Цикл для пошуку login серед записів в кеш файлі
        for key, value  in user.items():
            if key == login:
                trys_enter_password = 3
                while True: # Цикл що потребує від користувача ввести пароль
                    print(f'Enter password for {login}')
                    user_input = input('>>>')
                    if value[0].validate(user_input): # Якщо пароль для цього користувача вірний 
                        password_validator = True 
                        global cache
                        global user_login
                        cache = value[1] # Запис в глофальний кеш адресної книги всіх даних цього користувача 
                        user_login = key # Запис login в глобальну змінну для подпльшої роботи програми
                        break
                    else: # Якщо було введено хибний пароль кількість спроб зменшується на 1
                        trys_enter_password -= 1
                    if trys_enter_password < 1: # Якщо використано всі спроби вводу пароля зупинка логування 
                        print('Sorry. Wrong password try again later. Good bye.')
                        return False
                    else: # Повідомлення про ввід хибного пароля та залишок спроб для його введення
                        print(f'Sorry. Wrong password try again. You have {trys_enter_password} attempts')
        if password_validator:
            break
    if password_validator: # 
        global note_cache
        user_login = login
        with open('note_cache.bin', 'rb') as file:
            local_note_cache = pickle.load(file)
            for user in local_note_cache:
                for key, value in user.items():
                    if key == user_login:
                        note_cache = value[1]
        print(f'Welcome {login}')
        return True
    print('The login is incorrect or does not exist.')

# Функція для запису кешу в окремі файли для зберігання данних                
def exit(data):
    local_cache = None
    local_note_cache = None
    cache_saving = False
    note_cache_saving = False
    with open('cache.bin','rb') as file:
        local_cache = pickle.load(file)
    with open('note_cache.bin', 'rb') as file:
        local_note_cache = pickle.load(file)
    for user in local_cache:
        for key , value in user.items():
            if key == user_login:
                user[key][1] = cache
                with open('cache.bin','wb') as file:
                    pickle.dump(local_cache, file)
                cache_saving = True
                break
            if cache_saving:
                break
    for user in local_note_cache:
        for key , value in user.items():
            if key == user_login:
                user[key][1] = note_cache
                with open('note_cache.bin','wb') as file:
                    pickle.dump(local_note_cache, file)
                note_cache_saving = True
                break
            if note_cache_saving:
                break

def git(data):
    webbrowser.open('https://github.com/Krom4rd/Terminal_bot', new=2)

# Словник ключ = Функція, значення= Ключові слова для запуску функцій
COMMANDS = {
    greeting: 'hello',#
    add_contact: 'add contact',#
    add_phone: 'add phone',#
    edit_phone: 'edit phone',#
    del_phone: 'del phone',#
    contact_output: 'contact',#
    add_email: 'add email',#
    edit_email: 'edit email',#
    add_address: 'add address',#
    edit_address: 'edit address',#
    add_birthday: 'add birthday',#
    show_all: 'show all',#
    exit: ['exit', 'good bye', 'close'],#
    delete: 'del contact',#
    about: 'about',#
    days_to_birthday: 'days to birthday',#
    next_birthdays: 'next birthdays',#
    add_note: 'add note',#
    all_notes: 'all notes',#
    del_note: 'del note',#
    find_note: 'find note',#
    add_tag: 'add tag',#
    del_tag: 'del tag',#
    find_tag: 'find tag',#
    sorting: 'sorting',#
    sort_notes: 'sort notes',#
    git: 'git'#
}

def commands(data):
    # Поділ переданих данних користувачем через пробіл
    comand_list = data.lower().split()
    for key, value in COMMANDS.items():
        if len(comand_list) == 1:
            if comand_list[0] == value:
                return key, None
            elif comand_list[0] in COMMANDS[exit]:
                return exit, None
        elif len(comand_list) == 2:
            if comand_list[0] == value:
                return key, comand_list[1:]
            elif comand_list[0] + ' ' + comand_list[1] == value:
                return key, None
            elif comand_list[0] + ' ' + comand_list[1] in COMMANDS[exit]:
                return exit, None
        elif len(comand_list) == 3:
            if comand_list[0] == value:
                return key, comand_list[1:]
            if comand_list[0] + ' ' + comand_list[1] == value:
                return key, comand_list[2]
        elif len(comand_list) > 3:
            if ' '.join(comand_list[0:2]) == value:
                return key, comand_list[2:]
            if ' '.join(comand_list[0:3]) == value:
                return key, comand_list[3:]
    # Якщо не було знайдено переданої команди
    return None, None

def main():
    print(logo)
    simulate_loanding()   
    while True:
        print('Enter your login or press enter to create a new user.')
        user_input = input('>>>')
        if user_input in COMMANDS[exit]:
            exit(None)
        if user_input != '':
            if load_user_cache(user_input):
                break
        else:
            create_new_user()        
    # Цикл для тривалої роботи програми
    if user_login:
        simulate_loanding()
        print(greeting(None))
        while True:
            # Отримання даних від користувачаa
            user_input = input('>>>')
            if user_input:
                func, data = commands(user_input)
            if func == None:
                continue
            elif func == exit:
                # Вихід з програми та запис кешу в окремий файл
                func(data)
                print('Good bye')
                break
            else:
                # Запуск команд
                result = func(data)
                if result is None:
                    continue
                try:
                    print(result)
                except TypeError:
                    continue


if __name__ == '__main__':
    main()
