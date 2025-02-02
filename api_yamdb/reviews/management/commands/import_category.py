import csv

from django.core.management import BaseCommand

from api.constants import STATIC_PATH_CSV_FILES
from reviews.models import Category


class Command(BaseCommand):
    help = 'Загрузка данных категорий в БД из CSV'

    def handle(self, *args, **options):
        csv_file = f'{STATIC_PATH_CSV_FILES}category.csv'
        model = Category
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                try:
                    for row in reader:
                        self_id = int(row['id'])
                        name = row['name']
                        slug = row['slug']
                        model.objects.update_or_create(
                            id=self_id,
                            defaults={
                                'name': name,
                                'slug': slug
                            }
                        )
                except ValueError as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка в строке {row}: {e}')
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
