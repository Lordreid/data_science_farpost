import sqlite3

class TableData:
    """
    Обёртка для таблицы SQLite, реализующая протокол коллекций.
    При каждом обращении к данным выполняется SQL-запрос, поэтому данные всегда актуальны.
    """
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def __len__(self):
        # Получаем количество записей в таблице
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM " + self.table_name
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        if result is not None:
            return result[0]
        return 0

    def __getitem__(self, key: str):
        # Получаем запись, где столбец name равен key
        conn = sqlite3.connect(self.database_name)
        conn.row_factory = sqlite3.Row  # чтобы можно было обращаться к колонкам по имени
        cursor = conn.cursor()
        query = "SELECT * FROM " + self.table_name + " WHERE name = ?"
        cursor.execute(query, (key,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            raise KeyError("Запись с именем '" + key + "' не найдена.")
        # Преобразуем sqlite3.Row в обычный словарь
        row_dict = {}
        for col in row.keys():
            row_dict[col] = row[col]
        return row_dict

    def __contains__(self, key: str):
        # Проверяем, существует ли запись с указанным name
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM " + self.table_name + " WHERE name = ?"
        cursor.execute(query, (key,))
        result = cursor.fetchone()
        conn.close()
        if result is not None and result[0] > 0:
            return True
        return False

    def __iter__(self):
        # Итератор, который возвращает записи по одной, не загружая всю таблицу в память
        conn = sqlite3.connect(self.database_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM " + self.table_name
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            row_dict = {}
            for col in row.keys():
                row_dict[col] = row[col]
            yield row_dict
            row = cursor.fetchone()
        conn.close()


# Пример использования:
if __name__ == "__main__":
    # Предполагаем, что база данных example.sqlite содержит таблицу books с колонками name и author,
    # и в таблице хранятся следующие записи:
    #   name: Farenheit 451, Brave New World, 1984
    #   author: Bradbury, Huxley, Orwell
    books = TableData(database_name='example.sqlite', table_name='books')
    
    print("Количество книг в базе данных:", len(books))
    
    # Попытка получить запись для книги "1984"
    try:
        book = books['1984']
        print("Запись для книги '1984':", book)
    except KeyError as e:
        print(e)
    
    # Проверяем наличие книги "Farenheit 451"
    if 'Farenheit 451' in books:
        print("'Farenheit 451' присутствует в базе данных.")
    else:
        print("'Farenheit 451' отсутствует в базе данных.")
    
    # Выводим все книги из таблицы
    print("Список всех книг:")
    for record in books:
        print("Название:", record['name'], "| Автор:", record['author'])
