from datetime import datetime
from collections import UserDict
import re

# Функція декоратор для обробки помилок
def decorate_errors(inner):
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


class Field: # Батьківський клас для більшості класів для повернення значення в класі
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self)->str:
        return self._value

    @value.setter
    def value(self, value: str)-> None:
        self._value = value

    def __str__(self):
        return str(self.value)

class Name(Field): 
    def __init__(self, name: str)-> None:
        super().__init__(name.lower().capitalize())
        self.name = name.lower().capitalize()
    def __str__(self):
        return super().__str__()


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if self.validate_number() is False:
            print("Invalid phone number format. Try again!")

    def validate_number(self): # валідаці номеру телефону
        if len(self.value) == 10 and self.value.isdigit():
            return True
        else:
            return False

class Email(Field):
    def __init__(self, mail: str):
        super().__init__(mail)
        if self.validate_email() is False:
            print("Invalid email format. Try again!")

    def validate_email(self): # Валідація е-пошти
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, self.value):
            return True
        else:
            return False


class Address(Field):
    def __init__(self, address: str):
        super().__init__(address)

class Birthday(Field):
    @Field.value.setter
    def value(self, value: str = None):
        if value == None:
            self._value = ''
        else:
            try:
            # Спроба перетворити введене значення на об'єкт date
                self._value = datetime.strptime(value, '%d.%m.%Y')
                return
            except ValueError:
                pass
            try:
            # Якщо перша спроба не вдалася, то спробуємо інший формат дати
                self._value = datetime.strptime(value, '%d-%m-%Y')
                return
            except ValueError:
                pass
            # Якщо жоден з форматів не підходить, пишемо про помилку
            print("Date of birthday must be in dd.mm.yyyy or dd-mm-yyyy format")
    
    def __str__(self):
        return self.value.strftime('%d-%m-%Y')

class Contact():
    def __init__(self, name: Name, phone: Phone = None, email: Email = None, address: Address = None, birthday: Birthday = None):
        self.name = name.lower().capitalize()
        self.phones = []

        if phone is not None:
            new_phone = Phone(phone)
            if new_phone:
                self.phones.append(new_phone)
        if email is not None:
            self.email = Email(email)
        if address is not None:
            self.address = Address(address)
        if birthday is not None:
            self.birthday = Birthday(birthday)
    
    @decorate_errors
    def add_phone(self, phone_value: str = None): # Функція класу для додавання номеру телефону для контакту
        new_phone = Phone(phone_value) # Валідація номеру телефону
        if new_phone.validate_number():
            self.phones.append(new_phone) # Додавання номеру телефону для контакту
            return(f'Phone: {phone_value} for {self.name} added') # Повідомлення 

    @decorate_errors    
    def edit_phone(self, old_phone: str = None, new_phone: str = None): # Функція класу для зміни номера телефону
        find_phone = self.find_phone(old_phone) # Пошук потрібного номера телефону
        if not find_phone: # Якщо не знайдено такого номера телефону в контака поверне повідомлення 
            print(f'{old_phone} not exist')
            return
        new_phone_check = Phone(new_phone)  # валідація нового телефону
        if new_phone_check.validate_number() is not False:
            self.remove_phone(old_phone) # Видалення номера старого номера телефону 
            self.add_phone(new_phone) # Запис нового номера телефону
            print(f'Contact {self.name} changed his phone number from {old_phone} to {new_phone}')
    
    @decorate_errors 
    def remove_phone(self, phone_number: str = None): #Функція класу для видалення номеру телефону в контакту
        for element in self.phones: # Номері телефону в контакту може бути кілька тому проходимось циклом по списку телефонів
            if element.value == phone_number: # Якщо переданий користувачем номер існує в контакту
                self.phones.remove(element) # Видаляє цей номер
                return    

    @decorate_errors
    def find_phone(self, phone_number: str = None): # Функція класу для пошуку телефону в контакту 
        for phone in self.phones: # Цикл що проходить по списку телефонів контакту
            if phone.value == phone_number: # Якщо є відповідний 
                return phone # Повертає його 
        return None # Якщо немає номеру який ми шукали повертає None
    
    @decorate_errors
    def add_birthday(self, birthday: str = None): #Функція класу для додавання дня народження 
        new_birthday = Birthday(birthday) # Передаються дані в клас Birthday для валідації вводу дати
        if new_birthday.value is not None: # Якщо пройшла валідація 
            self.birthday = new_birthday # Контакт додає день народження 
            print(f'Birthday: {new_birthday} for {self.name} added')

    @decorate_errors
    def days_to_birthday(self): # Функція класу для підрахунку днів до наступного дня народження
        if self.birthday is None: # Перевірка на наявність дня народження в обєкра
            return
        today = datetime.now() # Сьогоднішня дата
        bday_date = self.birthday.value.replace(year=today.year) # Заміна року народження на теперішній рік 
        if today > bday_date: # Якщо день народження в цьому році вже минув
            bday_date = bday_date.replace(year=today.year + 1) # Розглянемо наступний рік
        days_to_next_bday = (bday_date - today).days # Обчислення днів до дня народження 
        return days_to_next_bday

    @decorate_errors
    def add_address(self, address: str = None): # Функція класу для додавання адреси
        new_address = Address(address) # Передані данні перетворюємо в клас Address
        if new_address is not None:  # Перевірка на наявність адреси в обєкта
            self.address = new_address  # Додавання адреси обєкту
            print(f'Address: {new_address} for {self.name} added')

    @decorate_errors
    def edit_address(self, new_address): # Функція класу для заміни адреси
        self.address = new_address
        print(f'Address for {self.name} is changed to {new_address}')

    @decorate_errors
    def add_email(self, email: str = None):# Функція класу для додавання е-пошти
        new_email = Email(email) # Перевірка на валідність переданої е-пошти
        if new_email.validate_email() is not False: 
            self.email = new_email # Додавання е-пошти обєкту
            print(f'Email: {new_email} for {self.name} added')

    @decorate_errors
    def edit_email(self, email: str = None): #Функція класу для зміни п-пошти
        new_email = Email(email) # Перевірка на валідність переданої е-пошти
        if new_email.validate_email() is not False:
            old_email = self.email # Стара е-пошта
            self.email = new_email # Додавання нової е-пошти
            print(f'Contact {self.name} change email from {old_email} to {self.email}')
    
    def __str__(self): # Функція класу для візуалізації обєкта класу як стоки
        self.contact_values = [] # Список всіх значень які має обєкт
        self.contact_values.append(self.name)# Додає імя до (списку всіх значень)
        if self.phones: # Якщо обєкт має номер телефону додає до (списку всіх значень)
            self.contact_values.append("; ".join(p.value for p in self.phones)) # Додає імя до (списку всіх значень)
        else: # Якщо немає номерів телефону додає " "
            self.contact_values.append(' ') 
        try: # Обробка помилки адже якщо в обєкта немає наступного значення винекне помилка
            if self.email : # Якщо обєкт має в наявності е-пошту
                self.contact_values.append(self.email.value) # Додає е-пошту до (списку всіх значень)
        except AttributeError:
            self.contact_values.append(' ')
        try: 
            if self.address: 
                self.contact_values.append(self.address.value)
        except AttributeError:
            self.contact_values.append(' ')
        try: 
            if self.birthday:
                self.contact_values.append('' + self.birthday.value.strftime('%d-%m-%Y')) # Додає дату народження в форматі дд-мм-рррр до (списку всіх значень)
        except AttributeError:
            self.contact_values.append(' ') 
        dashes = "+ {0:<14} + {1:<50} + {2:^32} + {3:32} + {4:18} +".format("-" * 14, "-" * 50, "-" * 32, "-" * 32, "-" * 18) 
        help_string = ''
        help_string += f'| {self.contact_values[0]:^14} | {self.contact_values[1]:^50} | {self.contact_values[2]:^32} | {self.contact_values[3]:^32} | {self.contact_values[4]:^18} |\n'
        help_string += dashes 
        return(help_string)
        

class Address_book(UserDict): # Клас реалізований я кеш для обєктів класу Contact

    def add_contact(self, contact: Contact):
        self.data[contact.name] = contact
        return f'Contact with name: {contact.name} created'

    def remove_contact(self, contact_name: str):
        if contact_name in self.data:
            del self.data[contact_name]

    def search_contact(self, contact_name: str):
        if contact_name in self.data:
            return self.data[contact_name]
        else:
            print(f'Contact with name: {contact_name} not detected in cache,\n\
use command "add" to added new contact')
            return None
    
    def days_to_birthday_with_days_left(self, days_left):
        days_left = int(days_left)
        result = []
        for key, value in self.data.items():
            try:
                days_to_birthday = value.days_to_birthday()
                if days_to_birthday <= days_left:
                    result.append({key:days_to_birthday})
            except AttributeError:
                continue
        if result:
            for contact in result:
                result_string = f'{str(*contact.keys())}\'s birthday is in {str(*contact.values())} days'
                if int(*contact.values()) == 1:
                    result_string = result_string[:-1]
                print(result_string)
        else:
            result_string = f'There are no contacts whose birthday is in {days_left} days'
            if days_left > 1:
                print(result_string)
            else:
                print(result_string[:-1])
        
    iter_records = 3

    def __iter__(self):
        self.idx = 0
        self.page = 0
        self.list_of_records = [record for record in self.data]

        return self

    def __next__(self):

        if self.idx >= len(self.data):
            raise StopIteration
        self.count_records = 1
        self.page += 1
        self.result = f'Page: {self.page}'
        self.result += f"\n| {'Name':^14} | {'Phone':^50} | {'Email':^32} | {'Address':^32} | {'Birthday':^18} |\n"
        self.result += "+ {0:<14} + {1:<50} + {2:^32} + {3:32} + {4:18} +".format("-" * 14, "-" * 50, "-" * 32, "-" * 32, "-" * 18)

        while self.count_records <= self.iter_records:
            if self.idx >= len(self.data):
                return self.result
            
            self.result += f'\n{self.data[self.list_of_records[self.idx]]}'
            self.count_records += 1
            self.idx += 1
                
        return self.result
    
    def set_iter_records(self, iter_records):
        self.iter_records = iter_records
   
    def __str__(self):

        if not self.data:
            print('The contact book is empty')
        else:
            self.result = 'Сontacts that are in the contact book:'
            self.result += f"\n| {'Name':^14} | {'Phone':^50} | {'Email':^32} | {'Address':^32} | {'Birthday':^18} |\n"
            self.result += "+ {0:<14} + {1:<50} + {2:^32} + {3:32} + {4:18} +".format("-" * 14, "-" * 50, "-" * 32, "-" * 32, "-" * 18)
            for record in self.data:
                self.result += f'\n{str(self.data[record])}'
            self.result += '\n'

            return self.result

class Note(Field):
    @decorate_errors
    def __init__(self, note: str = None, title: str = None, tag: str = None):
        self.title = list()
        self.tag = list()
        if tag and len(tag) > 30:
            print('The length of the tag should not exceed 30 characters')
        elif tag:
            self.tag.append(tag.lower().capitalize())
        if title is not None:
            self.title.append(title.capitalize())
        if note is not None and title is None:
            word_list = note.split()
            self.title.append(word_list[0].capitalize())
            if len(word_list) > 2:
                self.note = word_list[1].capitalize() + ' '.join(i for i in word_list[2:])
            else:
                self.note = word_list[0].capitalize()
        elif note is not None:
            self.note = note.capitalize()
        if self.title:
            print(f'New note with title {str(*self.title)} created')
    
    @decorate_errors
    def add_tag(self, tag):
        if tag and len(tag) > 30:
            print('The length of the tag should not exceed 30 characters')
        elif tag:
            self.tag.append(tag.lower().capitalize())

    @decorate_errors
    def remove_tag_in_note(self, tag = None):
        if self.tag and tag in self.tag:
            self.tag.pop(self.tag.index(tag))
            print(f'Tag {tag} for note: {self.title} deleted')
        elif self.tag and tag not in self.tag:
            print(f'Тo such tag: {tag} exists in this note,\n here is a list of tags for this note {str(*self.tag)}')
        elif self.tag and tag is None:
            self.tag = []

    def __str__(self):
        try:
            if self.tag:
                return f'{'_' * 70 + '\n'}Title: {", ".join(i for i in self.title)}\nTag: {", ".join(i for i in self.tag)}\nNote:\n{self.note}\n'
        except AttributeError:
            pass
        return f'{'_' * 70 + '\n'}Title: {", ".join(i for i in self.title)}\nNote:\n{self.note}\n'
        
class Note_book():
    def __init__(self) -> None:
        self.data = []
    def tag_checker(tag: str):
        if tag is None:
            return
        if len(tag) > 30:
            print('The length of the tag should not exceed 30 characters')
        else:
            return tag.lower().capitalize()
    
    @decorate_errors
    def del_note(self, note: Note):
        self.data.remove(note)
        print('Note deleted')

    @decorate_errors    
    def add_note(self,  note: str = None):
        new_note = Note(note)
        if new_note:
            self.data.append(new_note)

    @decorate_errors
    def search_note_with_tag(self, word) -> list:
        result = []
        for item in self.data:
            if word.lower().capitalize() in item.tag:
                result.append(item)
        if result:
            return result
        print(f'No notes found for this tag: {word}')
    
    @decorate_errors
    def search_note_with_title(self, word) -> list:
        result = []
        for item in self.data:
            if word.lower().capitalize() in item.title:
                result.append(item)
        if result:
            return result
        print(f'No notes found for this title: {word}')
    
    @decorate_errors
    def search_word_in_note(self, word) -> list:
        result = []
        for item in self.data:
            if item.note.lower().find(word.lower()) != -1:
                result.append(item)
        if result:
            return result
        return f'No notes found for this word: {word}'
    
    @decorate_errors
    def remove_tag_for_all_notes(self, tag):
        if tag is not None:
            note_list = self.search_note_with_tag_or_title(tag)
        if note_list is str():
            return note_list
        else:
            for note in note_list:
                note.remove_tag_in_note(tag)
                return f'Tag removed for all notes'
    
    def sort_by_tags(self):
        """
        Сортує нотатки за тегами.
        """

        self.data.sort(key=lambda note: note.tag)


    iter_records = 1

    def __iter__(self):
        self.idx = 0
        self.page = 0
        self.list_of_records = [record for record in self.data]

        return self

    def __next__(self):

        if self.idx >= len(self.data):
            raise StopIteration
        self.count_records = 1
        self.page += 1
        self.result = f'Note: {self.page}'

        while self.count_records <= self.iter_records:
            if self.idx >= len(self.data):
                return self.result
            
            self.result += f'\n{self.data[self.list_of_records[self.idx]]}'
            self.count_records += 1
            self.idx += 1
                
        return self.result
    
    def set_iter_records(self, iter_records):
        self.iter_records = iter_records
   
    def __str__(self):
        if not self.data:
            print('The note book is empty')
        else:
            self.result ='Notes that are in the note book:\n'
            index = 0

            for record in self.data:
                self.result += f'\n{self.data[index]}'
                index += 1
            # self.result += '\n'

            return self.result
        
class User_Info(Field):
    def __init__(self, login, password) -> None:
        self.login = login
        self.__password = None
        if self.password_validator(password):
            self.password = password

    @property
    def password(self):
            print('Sorry you not hawe a acces to return password.')

    @password.setter
    def password(self, value):
        try:
            old_password, new_password = value
        except ValueError:
            new_password = value
            old_password = ''
        if self.__password is None:
            if self.password_validator(new_password):
                self.__password = new_password
        else:
            if not old_password:
                print('The old password must be transferred.')
            elif self.validate(old_password):
                if self.password_validator(new_password):
                    self.__password = new_password
                    print('The password has been changed.')

    def validate(self,value):
        if self.__password == value:
            return True
        print("Wrong old password.")
        return False

    def password_validator(self, value:str):
        if len(value) < 8:
            print('The password must contain at least 8 characters.')
        upper_simbol = []
        lower_simbol = []
        num = []
        special_simbols = ['~',' ','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','}','[',']','|',':',';','\"','\'','<',',','>',',','?','/','.']
        for s in range(0,len(value)):
            s_copy = ord(value[s])
            if s_copy in range(97,122):
                lower_simbol.append(s_copy)
            elif s_copy in range(65,92):
                upper_simbol.append(s_copy)
            elif s_copy in range(48,58):
                num.append(s_copy)
            else:
                if value[s] not in special_simbols:
                    print(f'Only the following special characters can be used: {"".join(i for i in special_simbols)} Not "{value[s]}".')
        if upper_simbol and lower_simbol and num:
            return value
        if not num:
            print('The password must contain at least one digit.')
        if not upper_simbol:
            print('The password must contain at least one lowercase letter.')
        if not lower_simbol:
            print('The password must contain at least one capital letter.')
        self.password_validator(input('>>>'))

