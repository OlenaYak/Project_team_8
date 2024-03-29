# Personal assistant bot FRANKIE - Code Warriors

Цей проект являє собою реалізацію персонального асистента з інтерфейсом командного рядка. Проект встановлюється як пакет Python і може бути викликаний з будь-якого місця в системі відповідною командою після встановлення.

Цей простий python-додаток допоможе вам керувати контактами, нотатками та сортувати файли на вашому комп'ютері.
Бот сумісний як з Windows, Linux так і з MacOS.
Протестовано на python 3.11, можливо, не сумісний з попередніми версіями.


**Встановлення**

Завантажте пакет, розпакуйте його і за допомогою наступної команди встановіть його з розпакованої теки:

    pip install -e .

або

$ python setup.py install



**Виклик**

    python main.py



## Опис

Особистий асистент може:

1.  Збереження контактів з іменами, адресами, номерами телефонів, електронними адресами та днями народження в контактній книзі;
2.  Відображення списку контактів, у яких буде день народження протягом певної кількості днів від поточної дати;
3.  Показувати, скільки днів залишилося до наступного дня народження контакту.
4.  Перевіряти коректність введеного номера телефону та електронної пошти при створенні або редагуванні запису і повідомляти користувача в разі некоректного введення;
5.  Пошук контактів в контактній книзі;
6.  Редагування та видалення даних з контактної книги;
7.  Ведення нотаток з текстовою інформацією;
8.  Пошук нотаток;
9.  Видалення нотаток;
10. Додавання "тегів" до нотаток, ключових слів, що описують тему і предмет запису;
11. Пошук нотаток за ключовими словами (тегами);
12. Сортування нотатків за тегами
13. Сортування файлів у вказаній папці за категоріями (зображення, документи, відео тощо).



## Як користуватися

При запуску бота потрібно залогуватися абож створити нового користувача.
Щоб залогуватися після <Enter your login or press enter to create a new user> потрібно ввести існуючий логін або натиснути <Enter> щоб створити нового користувача.
Якщо ми не користувалися ботом і створюємо нового користувача бот попросить ввести логін.<Enter your login to register>
Після введення логіну бот попросить придумати пароль.<Enter new password>(Пароль повинен бути довше 8 символі, мусить містити малі букви, великі букви, цифри)
Якщо пароль не буде відповідати вимогам бот попросить ще раз ввести пароль та виведе які з критеріїв валідації пароля невідповідні.
Бот знову попросить залогуватися <Enter your login or press enter to create a new user> вводимо наш логін.
Після того як введемо логін бот попросить пароль <Enter password for ...> у нас є 3 спроби для його введення в іншому випадку бот припинить роботу.
Якщо все вірно бот привітається з вами та ми можемо працювати з ним.

Щоб отримати короткі підказки щодо використання, ви можете викликати команду **about** у будь-який момент під час роботи з асистентом


### Адресна книга

За допомогою цього бота ви можете створити свою книгу контактів, в якій зберігати імена, телефони, електронні адреси, дні народження.
Нижче ви можете знайти інформацію про всі команди, які ви можете використовувати з прикладами. Команди не чутливі до регістру.

#### Команди:

- [ ] **_hello_** За допомогою цієї команди ви можете почати роботу з ботом

- [ ] **_add ..._** За допомогою цієї команди бот зберігає в пам'яті новий контакт. Замість **...** користувач вводить ім'я.

- [ ] **_add phone ..._** За допомогою цієї команди бот додає номер телефону до існуючого контакту. Замість **...** користувач вводить номер(и) телефону.

- [ ] **_add email ..._** За допомогою цієї команди бот додає електронну пошту до існуючого контакту. Замість **...** користувач вводить email

- [ ] **_edit phone ..._** За допомогою цієї команди бот видаляє старі телефони і зберігає в пам'яті новий номер телефону існуючого контакту. Замість **...** користувач вводить номер телефону, який потрібно змінити, і новий номер телефону, обов'язково через пробіл.
      (_приклад:_ edit phone 380971234567 380637654321)

- [ ] **_del phone ..._** За допомогою цієї команди бот видаляє номер телефону в існуючому контакті. Замість **...** користувач вводить номер телефону, обов'язково через пробіл.
      (_приклад:_ del phone 380661234567)

- [ ] **_address ..._** За допомогою цієї команди бот додає адресу до існуючого контакту. Замість **...** користувач вводить адресу, обов'язково через пробіл.

- [ ] **_show all_** За допомогою цієї команди бот показує всі контакти з вашої адресної книги.

- [ ] **_birthday ..._** За допомогою цієї команди бот додає день народження до існуючого контакту. Замість **...** користувач вводить день народження у форматі: рррр-мм-дд, обов'язково з пробілом.
      (_приклад:_ birthday 1991-02-19)

- [ ] **_next birthdays ..._** За допомогою цієї команди бот показує всі контакти, у яких буде день народження у вказаний період часу, починаючи з сьогоднішнього дня. Замість **...** користувач вводить період у днях.
      (_приклад:_ days to birthday 8)

- [ ] **_days to birthday ..._** За допомогою цієї команди бот виведе скільки днів до дня народження існуючого контакту. Замість **...** користувач вводить імя, обов'язково через пробіл.

- [ ] **_git_** За допомогою цієї команди відкивається сторінка на GitHub де розміщено цього бота, для відслідковування оновлень.

- [ ] **_exit, close, good bye_** Ви можете використовувати будь-яку з цих команд для виходу з програми. Всі зміни будуть збережені автоматично.



## Сортування файлів

Функція переглядає папку, вказану під час виклику функції, перевіряє розширення файлу і, залежно від розширення, приймає рішення, до якої категорії віднести цей файл, і переміщує його до відповідної папки:

**"Аудіо":** [".mp3", ".aac", ".ac3", ".wav", ".amr", ".ogg"],

**"Відео "**: [".mp4", ".mov", ".avi", ".mkv"],

**"Зображення "**: [".jpg", ".jpeg", ".png", ".svg", ".gif"],

**"Документи "**: [".doc", ".docx", ".txt", ".pdf", ".xls", ".xlsx", ".pptx", ".rtf"],

**"Архіви "**: [".zip", ".rar", ".tar", ".gz"].

Всі інші файли залишаються без змін.




## Нотатки

За допомогою цього бота ви можете створювати власні текстові нотатки з тегами та керувати ними.
Нижче ви можете знайти інформацію про всі команди, які ви можете використовувати з прикладами. Команди не чутливі до регістру.


#### Команди:

- [ ] **_add note ..._** _<текст нотатки\>_ - За допомогою цієї команди бот додає нову нотатку. (_приклад_: add note Недобре зациклюватися на мріях і забувати жити).
Перше слово яке буде вписано в нотатку буде титулом нотатки. (Одне з слів для взаємодії з нотаткою)

- [ ] **_del note ..._** _<Title\> - команда для видалення нотаток. Бот виведе в термінал кількість нотаток з подібними титулами та по черзі пропонуватите
кожну нотатку до водалення(якщо передати в термінал 'y' нотатку буде видалено, якщо натиснути ввід перейде до наступної нотатки з подібни титулом)

- [ ] **_all notes_** - За допомогою цієї команди бот показує всі нотатки з їх "id" і тегами.

- [ ] **_add tag ..._** <id\> <tag1 tag2 tag3...\> - команда для додавання тегів до нотатки. Теги додаються до нотатки і зберігаються у вигляді списку. Теги в команді відокремлюються пробілами. Ви можете додати необмежену кількість тегів.

- [ ] **_del tag ..._**_<Title\> <Tag> - команда для видалення тегів в нотатках. Бот виведе в термінал кількість нотаток з подібними титулами та по черзі пропонуватите
кожну нотатку до водалення(якщо передати в термінал 'y' нотатку буде видалено, якщо натиснути ввід перейде до наступної нотатки з подібни титулом)

- [ ] **_find note ..._** - За допомогою цієї команди бот шукає нотатки за тегами та титулами та виводить в термінал всі збіги.

- [ ] **_sort notes_** - За допомогою цієї команди бот відсортєю всі нотатки за тегами.

- [ ] **_find_tag ..._** <Tag\> - команда для пошуку нотатки за тегом. Буде показано всі нотатки, які матимуть збіги з введеним тегом.



## Ліцензія
Цей проект поширюється за ліцензією MIT. Дивіться [ЛІЦЕНЗІЯ] (https://opensource.org/license/mit/) для деталей.
