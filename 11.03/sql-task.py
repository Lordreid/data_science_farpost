import sqlite3

class TableData:
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def __len__(self) -> int:
        """Возвращает количество записей в таблице"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            return cursor.fetchone()[0]

    def __getitem__(self, key: str) -> dict:
        """Возвращает запись по ключу (поле name)"""
        with sqlite3.connect(self.database_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE name = ?", 
                (key,)
            )
            row = cursor.fetchone()
            if not row:
                raise KeyError(f"Запись '{key}' не найдена")
            return dict(row)

    def __contains__(self, key: str) -> bool:
        """Проверяет наличие записи по ключу"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT 1 FROM {self.table_name} WHERE name = ?", 
                (key,)
            )
            return bool(cursor.fetchone())

    def __iter__(self):
        """Итератор по всем записям таблицы"""
        with sqlite3.connect(self.database_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            for row in cursor:
                yield dict(row)

# Пример использования
if __name__ == "__main__":
    # Подключаемся к базе данных
    db = TableData("example.sqlite", "books")

    # Получаем количество записей
    print(f"Всего книг: {len(db)}")

    # Получаем книгу по названию
    try:
        print("Информация о книге '1984':", db["1984"])
    except KeyError as e:
        print(e)

    # Проверяем наличие книги
    print("Есть ли 'Мастер и Маргарита'?", "Мастер и Маргарита" in db)

    # Выводим все книги
    print("\nВсе книги:")
    for book in db:
        print(f"{book['name']} ({book['author']})")