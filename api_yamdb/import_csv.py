import csv
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

from users.models import User
from reviews.models import Category, Comment, Genre, Review, Title


DICT = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    User: 'users.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

for model, base in DICT.items():
    with open(
        f'static/data/{base}',
        'r', encoding='utf-8'
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        objs_to_create = []
        for data in reader:
            if not model.objects.filter(id=data['id']).exists():
                obj = model(**data)
                objs_to_create.append(obj)
        model.objects.bulk_create(objs_to_create)
