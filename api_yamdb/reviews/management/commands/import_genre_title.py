import csv

from django.core.management import BaseCommand

from api.constants import STATIC_PATH_CSV_FILES
from reviews.models import GenreTitle


class Command(BaseCommand):
    help = 'Загрузка жанров связанных с заголовками в БД из CSV'

    def handle(self, *args, **options):
        csv_file = STATIC_PATH_CSV_FILES + 'genre_title.csv'
        model = GenreTitle

        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                try:
                    for row in reader:
                        self_id = int(row['id'])
                        title_id = int(row['title_id'])
                        genre_id = int(row['genre_id'])
                        model.objects.update_or_create(
                            id=self_id,
                            defaults={
                                'title_id': title_id,
                                'genre_id': genre_id
                            }
                        )
                except ValueError as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка в строке {row}: {e}')
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
