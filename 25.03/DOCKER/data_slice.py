# SQL Ver
'''
import mysql.connector
import time
from datetime import datetime

# Настройки подключения к базе данных
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'mydatabase',
}

def fetch_data():
    # Подключение к базе данных
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute("SELECT * FROM messages")  
    data = cursor.fetchall()

    # Закрытие соединения
    cursor.close()
    conn.close()

    return data

def save_to_file(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_slice_{timestamp}.txt"
    with open(filename, 'w') as f:
        for row in data:
            f.write(','.join(map(str, row)) + '\n')

if __name__ == "__main__":
    while True:
        data = fetch_data()
        save_to_file(data)
        time.sleep(300)  # 5 минут
'''
#clickhouse ver
import mysql.connector
import time
from datetime import datetime
from clickhouse_driver import Client
import clickhouse_connect
import redis

r = redis.Redis(host='localhost', port=6379, db=0)


config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'mydatabase',
}


db = clickhouse_connect.get_client(
    host= 'localhost',
    port= 8123,
    user= 'user',
    password= 'password',
    database= 'mydatabase',
    
)
    


def fetch_data():
    # Подключение к базе данных
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute("SELECT * FROM messages")
    data = cursor.fetchall()

    # Закрытие соединения
    cursor.close()
    conn.close()

    return data

def save_to_file(data): # это мы теперь не используем
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_slice_{timestamp}.txt"
    with open(filename, 'w') as f:
        for row in data:
            f.write(','.join(map(str, row)) + '\n')
            
def save_to_clickhouse(data):
    data = data #не очень красиво, но тут только так
    db.insert(
        "messages", data
    ) 


if __name__ == "__main__":
    while True:
        data = fetch_data()
        save_to_clickhouse(data)
        print("Данные сохранены в ClickHouse")
        time.sleep(300)  # 5 минут
