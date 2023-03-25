from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

MESSAGE = """
При необходиомсти загрузить данные из CSV файла,
сперва удалить db.sqlite3 для сброса БД.
Далее, использовать команду "python/python3 manage.py migrate --run-syncdb"
для создания новых таблиц."""


class Command(BaseCommand):
    """Отображет юзеру информацию при вводе help."""
    help = """
    Загружает данные из titles.csv, category.csv,
    genre.csv, genre_title.csv,
    users.csv, review.csv, comments.csv """

    def handle(self, *args, **options):
        print(MESSAGE)

        """Отображет информацию о начале процесса импорта данных в БД."""
        print('Начинаем импортировать данные в БД.')

        """Код для импорта данных в БД."""
        for row in DictReader(open('./static/data/users.csv')):
            users = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
            users.save()

        for row in DictReader(open('./static/data/category.csv')):
            categories = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            categories.save()

        for row in DictReader(open('./static/data/genre.csv')):
            genres = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genres.save()

        for row in DictReader(open('./static/data/titles.csv')):
            titles = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category']))
            titles.save()

        for row in DictReader(open('./static/data/genre_title.csv')):
            genre_title = GenreTitle(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                genre=Genre.objects.get(id=row['genre_id'])
            )
            genre_title.save()

        for row in DictReader(open('./static/data/review.csv')):
            reviews = Review(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            reviews.save()

        for row in DictReader(open('./static/data/comments.csv')):
            comments = Comment(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date']
            )
            comments.save()

        """Отображет информацию об окончании процесса импорта данных в БД."""
        print('Закончили импортировать данные в БД.')
