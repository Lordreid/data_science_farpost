import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg2

fake = Faker()

conn = psycopg2.connect(
    dbname="forum_db",
    user="admin",
    password="secret",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

start_date = datetime.now() - timedelta(days=30)
existing_user_ids = []
existing_topic_ids = []  # Храним созданные topic_id

for day in range(30):
    current_date = start_date + timedelta(days=day)
    daily_users = []
    
    # 1. Регистрация пользователей
    for _ in range(random.randint(5, 10)):
        username = fake.user_name()
        cursor.execute(
            "INSERT INTO users (username, created_at) VALUES (%s, %s) RETURNING id",
            (username, current_date)
        )
        user_id = cursor.fetchone()[0]
        daily_users.append(user_id)
        cursor.execute(
            "INSERT INTO user_actions (user_id, action_type, action_time, status) VALUES (%s, 'register', %s, 'success')",
            (user_id, current_date)
        )
    
    existing_user_ids.extend(daily_users)
    
    # 2. Действия с темами
    total_topics = 5 + random.randint(0, 3)
    error_count = 2
    
    # Ошибочные попытки
    for _ in range(error_count):
        cursor.execute(
            "INSERT INTO user_actions (user_id, action_type, action_time, status, target_id) VALUES (%s, 'create_topic', %s, %s, %s)",
            (None, current_date, 'error', None)
        )
    
    # Успешные темы
    for _ in range(total_topics - error_count):
        user_id = random.choice(existing_user_ids)
        cursor.execute(
            "INSERT INTO topics (user_id, created_at) VALUES (%s, %s) RETURNING id",
            (user_id, current_date)
        )
        topic_id = cursor.fetchone()[0]
        existing_topic_ids.append(topic_id)  # Сохраняем ID темы
        cursor.execute(
            "INSERT INTO user_actions (user_id, action_type, action_time, status, target_id) VALUES (%s, 'create_topic', %s, 'success', %s)",
            (user_id, current_date, topic_id)
        )
    
    # 3. Сообщения (только к существующим темам)
    if existing_topic_ids:  # Проверяем наличие тем
        for _ in range(5 + random.randint(0, 5)):
            user_id = random.choice([None, random.choice(existing_user_ids)])  # 50/50 аноним
            topic_id = random.choice(existing_topic_ids)  # Берём только существующие темы
            
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