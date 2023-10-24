# from django.core.management.base import BaseCommand
# from migration.models import SQLiteModel, PostgreSQLModel
#
#
# class Command(BaseCommand):
#     help = 'Выгрузка данных из SQLite в PostgreSQL'
#
#     def handle(self, *args, **options):
#         sqlite_data = SQLiteModel.objects.using('sqlite').all()
#
#         for obj in sqlite_data:
#             PostgreSQLModel.objects.create(
#                 field1=obj.field1,
#                 field2=obj.field2,
#                 # ... остальные поля
#             )
#
#         self.stdout.write(self.style.SUCCESS('Данные успешно выгружены и загружены в PostgreSQL.'))
