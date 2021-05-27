import sqlite3

# Удаление конкретного элемента с истории браузера
conn = sqlite3.connect('C:/Users/it11/AppData/Local/Google/Chrome/User Data/Default/History') # Путь к истории браузера

# Установка курсора
c = conn.cursor()

# Создание переменной id
# присвоим ей 0
id = 0

# создание переменной result

result = True

# Создаем цикл

while result:

    result = False

    # Создаем пустой список

    ids = []

    # Ищем ключевое слово в истории браузера
    for rows in c.execute("SELECT id,url FROM urls\
    WHERE url LIKE '%gosuslugi.ru%'"):
        # Выведем эту строку
        print(rows)

        # Выбираем id
        id = rows[0]

        ids.append((id,))

    # Выполним команду на удаление
    c.executemany('DELETE from urls WHERE id = ?', ids)

    # Подтверждаем изменения
    conn.commit()

# Закрываем соединение
conn.close()