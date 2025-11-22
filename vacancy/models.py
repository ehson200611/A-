from django.db import models

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
