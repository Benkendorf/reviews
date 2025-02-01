import csv

from django.core.management import BaseCommand

from api.constants import STATIC_PATH_CSV_FILES
from reviews.models import Category, Title


class Command(BaseCommand):
    help = 'Загрузка заголовков в БД из CSV'

    def handle(self, *args, **options):
        csv_file = STATIC_PATH_CSV_FILES + 'titles.csv'
        model = Title

        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                try:
                    for row in reader:
                        self_id = int(row['id'])
                        name = row['name']
                        year = int(row['year'])
                        category_id = self.get_category(int(row['category']))
                        model.objects.update_or_create(
                            id=self_id,
                            defaults={
                                'name': name,
                                'year': year,
                                'category': category_id
                            }
                        )
                except ValueError as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка в строке {row}: {e}')
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))

    @staticmethod
    def get_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
            return category
        except Category.DoesNotExist:
            return ValueError('Категория не найдена')
