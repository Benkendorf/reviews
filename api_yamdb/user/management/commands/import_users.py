import csv

from django.core.management import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = 'Загрузка пользовательских данных в БД из CSV'

    def handle(self, *args, **options):
        csv_file = 'static/data/users.csv'
        model = User

        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                try:
                    for row in reader:
                        self_id = int(row['id'])
                        username = str(row['username'])
                        email = str(row['email'])
                        role = str(row['role'])
                        bio = str(row['bio'])
                        first_name = str(row['first_name'])
                        last_name = str(row['last_name'])

                        model.objects.update_or_create(
                            id=self_id,
                            defaults={
                                'username': username,
                                'email': email,
                                'role': role,
                                'bio': bio,
                                'first_name': first_name,
                                'last_name': last_name
                            }
                        )
                except ValueError as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка в строке {row}: {e}')
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
