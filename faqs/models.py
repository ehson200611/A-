from django.db import models


class FAQText(models.Model):
    en = models.JSONField(default=dict)
    ru = models.JSONField(default=dict)
    tj = models.JSONField(default=dict)

    def __str__(self):
        return self.en.get("title", "FAQ Text")


class FAQPage(models.Model):
    question = models.JSONField(default=dict)
    answer = models.JSONField(default=dict)

    def __str__(self):
        return self.question.get("en", "FAQ Question")
