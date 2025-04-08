import psycopg2
import csv
import sys
from datetime import datetime

def generate_report(start_date, end_date):
    conn = psycopg2.connect(
        dbname="forum_db",
        user="admin",
        password="secret",
        host="localhost",
        port="5432"
    )
    
    query = """
    WITH daily_stats AS (
        SELECT
            DATE(action_time) AS day,
            COUNT(DISTINCT CASE WHEN action_type = 'register' THEN user_id END) AS new_users,
            COUNT(DISTINCT CASE WHEN action_type = 'create_topic' AND status = 'success' THEN target_id END) AS new_topics,
            COUNT(DISTINCT CASE WHEN action_type = 'create_message' THEN target_id END) AS total_messages,
            COUNT(DISTINCT CASE WHEN action_type = 'create_message' AND user_id IS NULL THEN target_id END) AS anonymous_messages
        FROM user_actions
        WHERE DATE(action_time) BETWEEN %s AND %s
        GROUP BY DATE(action_time)
    )
    SELECT
        day,
        new_users,
        COALESCE((anonymous_messages * 100.0 / NULLIF(total_messages, 0))::NUMERIC(5,2), 0) AS pct_anonymous,
        total_messages,
        COALESCE(((new_topics - LAG(new_topics, 1) OVER (ORDER BY day)) * 100.0 / NULLIF(LAG(new_topics, 1) OVER (ORDER BY day), 0)), 0) AS topic_growth_pct
    FROM daily_stats
    ORDER BY day;
    """
    
    try:
        cursor = conn.cursor()
        # Выполняем запрос с параметрами
        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()
        
        if not rows:
            print("No data found for the selected period")
            return

        with open('forum_report.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Day', 'New Users', '% Anonymous', 'Total Messages', 'Topic Growth %'])
            # Преобразуем None в 0 и форматируем даты
            formatted_rows = [
                (
                    row[0].strftime('%Y-%m-%d'),
                    row[1],
                    f"{row[2]:.2f}%" if row[2] is not None else "0.00%",
                    row[3],
                    f"{row[4]:.2f}%" if row[4] is not None else "0.00%"
                )
                for row in rows
            ]
            writer.writerows(formatted_rows)
            
        print("Report generated successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <start_date> <end_date> (YYYY-MM-DD)")
        sys.exit(1)
        
    generate_report(sys.argv[1], sys.argv[2])
    
    #ЗАПРОС выглядит как: python aggregate_data.py '2025-04-01' '2025-04-30', т.е используется текущая дата