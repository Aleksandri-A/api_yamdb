import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User

DICT = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    TitleGenre: 'genre_title.csv',
    User: 'users.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Импортирует данные из csv в базу данных'

    def handle(self, *args, **options):
        for model, base in DICT.items():
            with open(
                f'static/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)

                objs_to_create = []
                for data in reader:
                    if model.objects.filter(id=data['id']).exists():
                        raise Exception(
                            'БД не пустая, удалите БД и сделайте миграции.'
                        )
                    obj = model(**data)
                    objs_to_create.append(obj)
                model.objects.bulk_create(objs_to_create)
            self.stdout.write(self.style.SUCCESS(
                f'{base} imported successfully'
            ))
