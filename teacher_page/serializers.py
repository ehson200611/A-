from rest_framework import serializers
from .models import Teacher, TeachersPage

class TeacherSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ["id", "imageUrl", "name", "experience", "description", "video"]

    def get_name(self, obj):
        return {
            "ru": obj.name_ru,
            "en": obj.name_en,
            "tj": obj.name_tj,
        }

    def get_description(self, obj):
        return {
            "ru": obj.description_ru,
            "en": obj.description_en,
            "tj": obj.description_tj,
        }

class TeachersPageSerializer(serializers.ModelSerializer):
    englishLanguage = serializers.SerializerMethodField()
    online = serializers.SerializerMethodField()
    from990 = serializers.SerializerMethodField()
    weMonitor = serializers.SerializerMethodField()
    changeGoals = serializers.SerializerMethodField()
    selectTutor = serializers.SerializerMethodField()
    teachersData = TeacherSerializer(source="teachers", many=True)

    class Meta:
        model = TeachersPage
        fields = [
            "englishLanguage",
            "online",
            "from990",
            "weMonitor",
            "changeGoals",
            "selectTutor",
            "teachersData",
        ]

    def get_englishLanguage(self, obj):
        return {
            "ru": obj.englishLanguage_ru,
            "en": obj.englishLanguage_en,
            "tj": obj.englishLanguage_tj,
        }

    def get_online(self, obj):
        return {
            "ru": obj.online_ru,
            "en": obj.online_en,
            "tj": obj.online_tj,
        }

    def get_from990(self, obj):
        return {
            "ru": obj.from990_ru,
            "en": obj.from990_en,
            "tj": obj.from990_tj,
        }

    def get_weMonitor(self, obj):
        return {
            "ru": obj.weMonitor_ru,
            "en": obj.weMonitor_en,
            "tj": obj.weMonitor_tj,
        }

    def get_changeGoals(self, obj):
        return {
            "ru": obj.changeGoals_ru,
            "en": obj.changeGoals_en,
            "tj": obj.changeGoals_tj,
        }

    def get_selectTutor(self, obj):
        return {
            "ru": obj.selectTutor_ru,
            "en": obj.selectTutor_en,
            "tj": obj.selectTutor_tj,
        }
