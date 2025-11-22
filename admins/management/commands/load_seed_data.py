import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from admins.models import AdminUser, NotificationAdmin, AdminForSuperAdmin, TestAdmin

class Command(BaseCommand):
    help = 'Load seed data from data.json'

    def handle(self, *args, **options):
        with open('admins/seeds/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # =============================
        # Load AdminUser
        # =============================
        for item in data.get('usersAdmin', []):
            joinDate = parse_datetime(item['joinDate']) if item.get('joinDate') else None
            AdminUser.objects.update_or_create(
                id=item['id'],
                defaults={
                    'name': item['name'],
                    'phoneNumber': item['phoneNumber'],
                    'role': item['role'],
                    'joinDate': joinDate
                }
            )

        # =============================
        # Load NotificationAdmin
        # =============================
        for item in data.get('notificationAdmin', []):
            date = parse_datetime(item['date']) if item.get('date') else None
            NotificationAdmin.objects.update_or_create(
                id=item['id'],
                defaults={
                    'title': item['title'],
                    'phoneNumber': item['phoneNumber'],
                    'type': item['type'],
                    'status': item['status'],
                    'date': date
                }
            )

        # =============================
        # Load AdminForSuperAdmin
        # =============================
        for item in data.get('adminsForSuperAdmin', []):
            joinDate = parse_datetime(item['joinDate']) if item.get('joinDate') else None
            AdminForSuperAdmin.objects.update_or_create(
                id=item['id'],
                defaults={
                    'name': item['name'],
                    'phone': item['phone'],
                    'role': item['role'],
                    'joinDate': joinDate
                }
            )

        # =============================
        # Load TestAdmin
        # =============================
        for item in data.get('testAdmin', []):
            dateCompleted = parse_datetime(item['dateCompleted']) if item.get('dateCompleted') else None
            TestAdmin.objects.update_or_create(
                id=item['id'],
                defaults={
                    'userName': item['userName'],
                    'level': item['level'],
                    'dateCompleted': dateCompleted,
                    'timeSpent': item.get('timeSpent'),
                    'totalQuestions': item['totalQuestions'],
                    'correctAnswers': item.get('correctAnswers'),
                    'incorrectAnswers': item.get('incorrectAnswers'),
                    'score': item.get('score'),
                    'status': item['status']
                }
            )

        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully!'))
