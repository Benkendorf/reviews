import csv

from django.core.management import BaseCommand
from django.utils.dateparse import parse_datetime

from api.constants import STATIC_PATH_CSV_FILES
from reviews.models import Review, Title
from user.models import User


class Command(BaseCommand):
    help = 'Загрузка ревью в БД из CSV'

    def handle(self, *args, **options):
        csv_file = f'{STATIC_PATH_CSV_FILES}review.csv'
        model = Review

        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        self_id = int(row['id'])
                        title = self.get_title(int(row['title_id']))
                        text = str(row['text'])
                        author = self.get_user(int(row['author']))
                        score = int(row['score'])
                        pub_date = self.get_datetime_object(row['pub_date'])
                        model.objects.update_or_create(
                            id=self_id,
                            defaults={
                                'title': title,
                                'text': text,
                                'author': author,
                                'score': score,
                                'pub_date': pub_date
                            }
                        )
                    except ValueError as e:
                        self.stdout.write(
                            self.style.ERROR(f'Ошибка в строке {row}: {e}')
                        )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))

    @staticmethod
    def get_user(author_id):
        try:
            return User.objects.get(id=author_id)
        except User.DoesNotExist:
            raise ValueError(f'Пользователь {author_id} не найден.')

    @staticmethod
    def get_datetime_object(input_date):
        pub_date = parse_datetime(input_date)
        if not pub_date:
            raise ValueError('Некорректная дата')
        return pub_date

    @staticmethod
    def get_title(title_id):
        try:
            return Title.objects.get(id=title_id)
        except Title.DoesNotExist:
            raise ValueError(f'Заголовок {title_id} не найден.')
