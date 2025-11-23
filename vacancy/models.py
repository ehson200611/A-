from django.db import models

class VacancyQuestion(models.Model):
    question_en = models.TextField()
    question_ru = models.TextField()
    question_tj = models.TextField()

    answer_en = models.TextField()
    answer_ru = models.TextField()
    answer_tj = models.TextField()

    def __str__(self):
        return f"Question {self.id}"


class VacancyUser(models.Model):
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_tj = models.CharField(max_length=255)

    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_tj = models.CharField(max_length=255)

    description_en = models.TextField()
    description_ru = models.TextField()
    description_tj = models.TextField()

    image = models.ImageField(upload_to='vacancy/', blank=True, null=True)

    def __str__(self):
        return self.name_en
