# content/management/commands/seed_teachers.py
import json
import os
from django.core.management.base import BaseCommand
from teacher_page.models import Teacher, TeachersPage

class Command(BaseCommand):
    help = "Seed teachers page and teachers"

    def handle(self, *args, **kwargs):
        # Ҷойгир кардани path нисбат ба файли command
        file_path = os.path.join(os.path.dirname(__file__), "teachers_seed.json")
        
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        # Дастрасӣ ба teachersData дар дохили teachersPage
        teachers_data = data["teachersPage"]["teachersData"]

        # Эҷод кардани Teacher objects
        teacher_objs = []
        for t in teachers_data:
            teacher = Teacher.objects.create(
                name_ru=t["name"]["ru"],
                name_en=t["name"]["en"],
                name_tj=t["name"]["tj"],
                experience=t.get("experience", 0),
                imageUrl=t.get("imageUrl", ""),
                video=t.get("video", ""),
                description_ru=t["description"]["ru"],
                description_en=t["description"]["en"],
                description_tj=t["description"]["tj"],
            )
            teacher_objs.append(teacher)

        # Эҷод кардани TeachersPage
        page_data = data["teachersPage"]
        page = TeachersPage.objects.create(
            englishLanguage_ru=page_data["englishLanguage"]["ru"],
            englishLanguage_en=page_data["englishLanguage"]["en"],
            englishLanguage_tj=page_data["englishLanguage"]["tj"],
            online_ru=page_data["online"]["ru"],
            online_en=page_data["online"]["en"],
            online_tj=page_data["online"]["tj"],
            from990_ru=page_data["from990"]["ru"],
            from990_en=page_data["from990"]["en"],
            from990_tj=page_data["from990"]["tj"],
            weMonitor_ru=page_data["weMonitor"]["ru"],
            weMonitor_en=page_data["weMonitor"]["en"],
            weMonitor_tj=page_data["weMonitor"]["tj"],
            changeGoals_ru=page_data["changeGoals"]["ru"],
            changeGoals_en=page_data["changeGoals"]["en"],
            changeGoals_tj=page_data["changeGoals"]["tj"],
            selectTutor_ru=page_data["selectTutor"]["ru"],
            selectTutor_en=page_data["selectTutor"]["en"],
            selectTutor_tj=page_data["selectTutor"]["tj"],
        )

        page.teachers.set(teacher_objs)
        page.save()

        self.stdout.write(self.style.SUCCESS("Teachers page successfully seeded!"))
