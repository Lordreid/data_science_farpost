import psycopg2
import csv
import sys
from datetime import datetime

def generate_report():
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
            DATE(ua.action_time) AS day,
            COUNT(DISTINCT CASE WHEN ua.action_type = 'register' THEN ua.user_id END) AS new_users,
            
            COUNT(DISTINCT CASE WHEN ua.action_type = 'create_topic' AND ua.status = 'success' THEN ua.target_id END) AS new_topics,
        
            COUNT(DISTINCT CASE WHEN ua.action_type = 'create_message' THEN ua.target_id END) AS total_messages,
            
            COUNT(DISTINCT CASE 
                WHEN ua.action_type = 'create_message' 
                AND EXISTS (
                    SELECT 1 FROM messages m 
                    WHERE m.id = ua.target_id AND m.user_id IS NULL
                ) 
                THEN ua.target_id 
            END) AS anonymous_messages
        FROM user_actions ua
        WHERE DATE(ua.action_time) BETWEEN '2025-04-01' AND '2025-04-30'
        GROUP BY DATE(ua.action_time)
    )
    SELECT
        day,
        new_users,
        COALESCE((anonymous_messages * 100.0 / NULLIF(total_messages, 0))::NUMERIC(5,2), 0) AS pct_anonymous,
        total_messages,
        COALESCE(
            ((new_topics - LAG(new_topics, 1) OVER (ORDER BY day)) * 100.0 / 
            NULLIF(LAG(new_topics, 1) OVER (ORDER BY day), 0)), 
            0
        ) AS topic_growth_pct
    FROM daily_stats
    ORDER BY day;
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            print("No data found for the selected period")
            return

        # Генерация отчета
        filename = f"forum_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Day', 'New Users', '% Anonymous', 'Total Messages', 'Topic Growth %'])
            
            for row in rows:
                formatted_row = (
                    row[0].strftime('%Y-%m-%d'),
                    row[1],
                    f"{row[2]:.2f}%" if row[2] is not None else "0.00%",
                    row[3],
                    f"{row[4]:.2f}%" if row[4] is not None else "0.00%"
                )
                writer.writerow(formatted_row)
            
        print(f"Report saved as {filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: python etl.py")
        sys.exit(1)
        
    generate_report()