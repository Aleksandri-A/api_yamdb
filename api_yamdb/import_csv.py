import csv
import sqlite3

from reviews.models import Category

# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
file_name = input('Введите имя cvs-таблицы, которую хотите импортировать: ')
# print(conn)
# print(cursor)

with open('static/data/' + file_name + '.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        obj, created = Category.objects.update_or_create(
            id=row[0],
            defaults={'name': row[1], 'slug': row[2]}
        )
