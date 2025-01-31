import csv

from django.core.management import BaseCommand
from django.utils.dateparse import parse_datetime

from reviews.models import Comment, Review
from user.models import User


class Command(BaseCommand):
    help = 'Загрузка комментариев в БД из CSV'

    def handle(self, *args, **options):
        csv_file = 'static/data/comments.csv'
        model = Comment
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                try:
                    for row in reader:
                        self_id = int(row['id'])
                        review_id = self.get_review(int(row['review_id']))
                        text = row['text']
                        author = self.get_user(row['author'])
                        pub_date = self.get_datetime_object(row['pub_date'])
                        model.objects.update_or_create(
                            id=self_id,
                            defaults={
                                'review': review_id,
                                'text': text,
                                'author': author,
                                'pub_date': pub_date,
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
            user = User.objects.get(id=author_id)
            return user
        except User.DoesNotExist:
            raise ValueError(f'Пользователь ID {author_id} не найден.')

    @staticmethod
    def get_datetime_object(input_date):
        pub_date = parse_datetime(input_date)
        if not pub_date:
            raise ValueError('Некорректная дата')
        return pub_date

    @staticmethod
    def get_review(review_id):
        try:
            review = Review.objects.get(id=review_id)
            return review
        except Review.DoesNotExist:
            raise ValueError(f'Ревью ID {review_id} не найден.')
