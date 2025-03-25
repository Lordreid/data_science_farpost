import sqlite3
import os
from typing import Iterator

class TableData:
    """Класс для работы с таблицей в базе данных SQLite"""
    
    def __init__(self, database_name: str, table_name: str):
        if not os.path.exists(database_name):
            raise FileNotFoundError(f"Файл {database_name} не найден") # Проверяем существует ли файл базы данных
        
        self.database_name = database_name
        self.table_name = table_name

    def _execute_query(self, query: str, params=None):
        """Выполняет SQL-запрос и возвращает результаты"""
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        connection.commit()
        return cursor

    def __len__(self) -> int:
        """Возвращает общее количество записей в таблице"""
        cursor = self._execute_query(f"SELECT COUNT(*) FROM {self.table_name}") # Выполняем запрос на подсчет строк
        count = cursor.fetchone()  # Получаем результат
        return count[0]  # Возвращаем первое значение из кортежа

    def __getitem__(self, name: str) -> tuple:
        """Возвращает запись по имени"""
        cursor = self._execute_query(
            f"SELECT * FROM {self.table_name} WHERE name = ?", 
            (name,)
        )
        result = cursor.fetchone()
        
        if not result:
            raise KeyError(f"Имя {name} не найдено")
        return result

    def __contains__(self, name: str) -> bool:
        """Проверяет существует ли запись с указанным именем"""
        cursor = self._execute_query(
            f"SELECT 1 FROM {self.table_name} WHERE name = ?", 
            (name,)
        )
        return cursor.fetchone() is not None

    def __iter__(self) -> Iterator[tuple]:
        """Возвращает итератор для прохода по всем записям"""
        cursor = self._execute_query(f"SELECT * FROM {self.table_name}")
        
        while True:
            row = cursor.fetchone()
            if row is None:  # Когда записи закончатся
                break
            yield row

    def close_connection(self):
        """Закрывает соединение с базой данных"""
        self.connection.close()
        
        
#------------Проверяем работу кода------------

presidents = TableData("11.03\\example.sqlite", "presidents")

print("Всего записей:", len(presidents))

print("Информация о Байдене:", presidents["Trump"])

if "Vladimir Putin" in presidents:
    print("Путин найден в базе")
else: print("Путин не найден в базе")

for president in presidents:
    print(president)