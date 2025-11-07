import json
from django.core.management.base import BaseCommand
from home_page.models import HomePage

class Command(BaseCommand):
    help = "Seed HomePage data"

    def handle(self, *args, **kwargs):
        with open('home_page/seed_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        homepage, created = HomePage.objects.get_or_create(id=1)
        homepage.data = data
        homepage.save()

        self.stdout.write(self.style.SUCCESS("HomePage data seeded successfully."))
