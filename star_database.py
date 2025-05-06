import sqlite3
import json


def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stars (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                full_name TEXT,
                description TEXT,
                language TEXT,
                stargazers_count INTEGER,
                forks_count INTEGER,
                open_issues_count INTEGER,
                created_at TEXT,
                updated_at TEXT,
                pushed_at TEXT
            )
        ''')
        conn.commit()
        print("Table created successfully or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")


def save_to_database(conn, stars):
    # 按 created_at 排序
    stars.sort(key=lambda x: x['created_at'])
    cursor = conn.cursor()
    for star in stars:
        try:
            cursor.execute('''
                INSERT INTO stars (name, full_name, description, language, stargazers_count, forks_count, open_issues_count, created_at, updated_at, pushed_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            ''', (
                star['name'],
                star['full_name'],
                star.get('description', ''),
                star['language'],
                star['stargazers_count'],
                star['forks_count'],
                star['open_issues_count'],
                star['created_at'],
                star['updated_at'],
                star['pushed_at']
            ))
            conn.commit()
            print(f"Successfully saved record: Name - {star['name']}")
        except sqlite3.IntegrityError:
            print(f"Skipped duplicate record: Name - {star['name']}")
        except Exception as e:
            print(f"Error saving record: Name - {star['name']}. Error: {e}")


if __name__ == "__main__":
    conn = sqlite3.connect('stars.db')
    create_table(conn)

    try:
        with open('star.json', 'r', encoding='utf-8') as f:
            stars = json.load(f)
        save_to_database(conn, stars)
        print("Stars data saved successfully to database")
    except FileNotFoundError:
        print("star.json file not found.")
    finally:
        conn.close()
