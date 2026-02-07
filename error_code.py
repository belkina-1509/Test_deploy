import sqlite3
import os

# Уязвимость 1: Жёстко закодированные учётные данные в коде
DB_PASSWORD = "12345"
DATABASE = "test.db"

# Уязвимость 2: Небезопасное соединение без проверок
def create_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

# Уязвимость 3: SQL-инъекция через конкатенацию строк
def get_user_data(username):
    conn = create_connection()
    cursor = conn.cursor()
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ: прямой ввод в SQL-запрос
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()  # Потенциальная утечка соединения при исключении
    return results

# Уязвимость 4: Невалидируемый ввод
def insert_user():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Уязвимость: нет проверки ввода
    user_id = input("Enter user ID: ")
    username = input("Enter username: ")
    
    # Ещё одна SQL-инъекция
    cursor.execute(f"INSERT INTO users VALUES ({user_id}, '{username}')")
    conn.commit()
    conn.close()

# Уязвимость 5: Избыточные права и небезопасные запросы
def delete_user():
    conn = create_connection()
    cursor = conn.cursor()
    
    user_id = input("Enter user ID to delete: ")
    
    # Уязвимость: удаление без подтверждения и валидации
    cursor.execute("DELETE FROM users WHERE id = " + user_id)
    conn.commit()
    conn.close()

# Уязвимость 6: Небезопасное логирование с конфиденциальными данными
def log_sensitive_data(data):
    print(f"[DEBUG] User data: {data}")  # Конфиденциальные данные в логах

# Уязвимость 7: Глобальная переменная с состоянием
global_user_list = []

def fetch_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Уязвимость: выборка всех данных без лимитов
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    
    # Уязвимость: сохранение в глобальную переменную
    global global_user_list
    global_user_list = all_users
    
    conn.close()
    return all_users

# Уязвимость 8: Обработка ошибок с избыточной информацией
def unsafe_query(query):
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)  # Прямое выполнение любого SQL
        return cursor.fetchall()
    except Exception as e:
        # Уязвимость: раскрытие внутренней информации
        print(f"Database error: {str(e)}")
        print(f"Query was: {query}")
        return None
    finally:
        conn.close()

# Уязвимость 9: Слабый пароль в коде
def admin_login(password):
    if password == "admin123":  # Слабый пароль в коде
        return True
    return False

# Главная функция с множеством проблем
def main():
    print("=== Vulnerable User Database System ===")
    
    # Создаём тестовую таблицу
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()
    
    # Пример использования уязвимых функций
    while True:
        print("\n1. Search user")
        print("2. Add user")
        print("3. Delete user")
        print("4. Show all users")
        print("5. Exit")
        
        choice = input("Select: ")
        
        if choice == "1":
            # Уязвимый поиск
            username = input("Enter username to search: ")
            results = get_user_data(username)
            print(f"Results: {results}")
            
        elif choice == "2":
            # Уязвимое добавление
            insert_user()
            
        elif choice == "3":
            # Уязвимое удаление
            delete_user()
            
        elif choice == "4":
            # Небезопасная выборка всех данных
            users = fetch_all_users()
            for user in users:
                print(user)
                
        elif choice == "5":
            break
            
        else:
            print("Invalid choice")

# Уязвимость 10: Запуск с избыточными правами
if __name__ == "__main__":
    main()