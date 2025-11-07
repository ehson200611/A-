from django.contrib import admin
from .models import FAQText, FAQPage

@admin.register(FAQText)
class FAQTextAdmin(admin.ModelAdmin):
    list_display = ("id",)
    search_fields = ("en__title",)


@admin.register(FAQPage)
class FAQPageAdmin(admin.ModelAdmin):
    list_display = ("id", "get_question_en")

    def get_question_en(self, obj):
        return obj.question.get("en", "")
    get_question_en.short_description = "Question (EN)"
