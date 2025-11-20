# home_page/management/commands/seed_testimonials.py
import os
import json
from django.core.management.base import BaseCommand
from home_page.models import Testimonial
from django.conf import settings

class Command(BaseCommand):
    help = "Seed Testimonial items from JSON file"

    def handle(self, *args, **kwargs):
        # Пайдо кардани роҳи пурраи файли JSON
        json_path = os.path.join(settings.BASE_DIR, "home_page/seed/testimonials.json")
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"JSON file not found: {json_path}"))
            return

        # Хондани файл бо UTF-8-SIG барои пешгирии BOM
        try:
            with open(json_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON: {e}"))
            return

        # Хориҷ кардани ҳамаи Testimonial-ҳои қаблӣ
        Testimonial.objects.all().delete()

        # Эҷоди объекти нав
        created_count = 0
        for item in data:
            try:
                # Агар поле image вуҷуд надошта бошад, барои Model CharField
                image = item.get("image", "")

                # Ҷойгир кардани номи JSON
                name_dict = item.get("name", {})
                name_en = name_dict.get("en", "")
                name_ru = name_dict.get("ru", "")
                name_tj = name_dict.get("tj", "")

                # Ҷойгир кардани review ба текст
                review_dict = item.get("review", {})
                review_text = review_dict.get("en", "")  # Агар дар Model танҳо як поле text вуҷуд дошта бошад

                # Эҷоди объекти Testimonial
                Testimonial.objects.create(
                    order=int(item.get("id", created_count + 1)),
                    name=name_en,
                    video=image  # Агар шумо видеоро истифода мекунед, агар не, метавонед поле дигари CharField созед
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating item: {item}. Exception: {e}"))

        self.stdout.write(self.style.SUCCESS(f"{created_count} Testimonial items seeded successfully!"))
