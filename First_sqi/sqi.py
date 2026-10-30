import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
""")

def add_user(username):
	try:
		cursor.execute(
			"INSERT INTO users (name) VALUES (?)",
			(username, )
		)
		print("Пользователь добавлен")
		conn.commit()
	except sqlite3.IntegrityError:
		print("Ошибка: Имя уже есть в базе данных")

def read_all_users():
	cursor.execute("SELECT * FROM users;")
	users = cursor.fetchall()
	
	if not users:
		print("База данных пуста")
		return

	print("\nСписок всех пользователей:")
	for user in users:
		# user[0] — это id, user[1] — это имя
		print(f"ID: {user[0]} | Имя: {user[1]}")

def user_is_real(username):
	cursor.execute(
		"SELECT name FROM users WHERE name = ?",
		(username,)
	)
	user = cursor.fetchone()	
	if user is None:
		print("Ошибка: пользователь не найден")
	else:
		print("Пользователь найден")

def update_user(old_name, new_name):
	try:
		cursor.execute(
			"UPDATE users SET name = ? WHERE name = ?",
			(new_name, old_name)
		)
		
		# Проверяем, изменилась ли хоть одна строка
		if cursor.rowcount > 0:
			print(f"Имя успешно изменено с '{old_name}' на '{new_name}'")
			conn.commit() # Фиксируем изменения в БД
		else:
			print(f"Ошибка: Пользователь с именем '{old_name}' не найден")
			
	except sqlite3.IntegrityError:
		# Перехватываем ошибку, если новое имя уже занято кем-то другим
		print(f"Ошибка: Имя '{new_name}' уже занято другим пользователем")

def delete_user(username):
	# Выполняем SQL-запрос на удаление
	cursor.execute(
		"DELETE FROM users WHERE name = ?",
		(username,)
	)
	
	# Проверяем, удалилось ли что-нибудь
	if cursor.rowcount > 0:
		print(f"Пользователь '{username}' успешно удален")
		conn.commit() # Сохраняем изменения в файле БД
	else:
		print(f"Ошибка: Пользователь '{username}' не найден в базе")

def count_users():
	cursor.execute("SELECT COUNT(*) FROM users;")
	# fetchone() возвращает кортеж, например: (5,)
	result = cursor.fetchone()
	print(f"Всего пользователей в базе данных: {result[0]}")

running = True
while running:
	print("\nКоманды: 0 - Выход, 1 - Добавить, 2 - Показать всех, 3 - Найти, 4 - Изменить имя, 5 - Удалить, 6 - Кол-во пользователей")
	try:
		ops = int(input("Номер команды: "))
		if ops == 0:
			running = False
		elif ops == 1:
			add_user(input("Добавить пользователя: "))
		elif ops == 2:
			read_all_users()
		elif ops == 3:
			user_is_real(input("Найти пользователя: "))
		elif ops == 4:
			update_user(input("Какое имя изменить: "), input("На какое имя изменить: "))
		elif ops == 5:
			delete_user(input("Имя пользователя для удаления: "))
		elif ops == 6:
			count_users()
		else:
			print("Неверный номер команды")
	except ValueError:
		print("Пожалуйста, введите число.")
conn.close()