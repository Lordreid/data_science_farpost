import redis
import mysql.connector

# Подключение к Redis (если в Docker, замените host на 'redis')
r = redis.Redis(host='localhost', port=6379, db=0)

# Подключение к MySQL (если в Docker, замените host на 'mysql')
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydatabase"
)
cursor = db.cursor()

while True:
    # Чтение сообщения из Redis
    message = r.brpop('messages', timeout=0)
    if message:
        # Декодируем байты в строку и вставляем в MySQL
        text = message[1].decode('utf-8')
        cursor.execute("INSERT INTO messages (message) VALUES (%s)", (str(text),))
        db.commit()
        print(f"Inserted: {text}")        
