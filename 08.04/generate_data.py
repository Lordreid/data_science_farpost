import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg2

fake = Faker()

# Подключение к БД
conn = psycopg2.connect(
    dbname="forum_db",
    user="admin",
    password="secret",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Генерация данных за 30 дней
start_date = datetime.now() - timedelta(days=30)

for day in range(30):
    current_date = start_date + timedelta(days=day)
    
    # 1. Регистрация пользователей (минимум 5)
    for _ in range(random.randint(5, 10)):
        username = fake.user_name()
        cursor.execute(
            "INSERT INTO users (username, created_at) VALUES (%s, %s) RETURNING id",
            (username, current_date)
        )
        user_id = cursor.fetchone()[0]
        
        # Логируем действие "регистрация"
        cursor.execute(
            "INSERT INTO user_actions (user_id, action_type, action_time, status) VALUES (%s, 'register', %s, 'success')",
            (user_id, current_date)
        )
    
    # 2. Действия с темами (минимум 5, из них 2 ошибки)
    for _ in range(5 + random.randint(0, 3)):
        user_id = random.choice([None, random.randint(1, 100)])  # 2 ошибки гарантированно
        status = 'success' if user_id else 'error'
        
        if status == 'success':
            cursor.execute(
                "INSERT INTO topics (user_id, created_at) VALUES (%s, %s) RETURNING id",
                (user_id, current_date)
            )
            topic_id = cursor.fetchone()[0]
        else:
            topic_id = None
            
        cursor.execute(
            "INSERT INTO user_actions (user_id, action_type, action_time, status, target_id) VALUES (%s, 'create_topic', %s, %s, %s)",
            (user_id, current_date, status, topic_id)
        )
    
    # 3. Сообщения (50/50 анонимы)
    for _ in range(5 + random.randint(0, 5)):
        user_id = random.choice([None, random.randint(1, 100)])
        topic_id = random.randint(1, 50)
        
        cursor.execute(
            "INSERT INTO messages (user_id, topic_id, created_at) VALUES (%s, %s, %s) RETURNING id",
            (user_id, topic_id, current_date)
        )
        message_id = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO user_actions (user_id, action_type, action_time, status, target_id) VALUES (%s, 'create_message', %s, 'success', %s)",
            (user_id, current_date, message_id)
        )

conn.commit()
cursor.close()
conn.close()