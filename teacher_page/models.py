from django.db import models

class Teacher(models.Model):
    name_ru = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    name_tj = models.CharField(max_length=100)

    experience = models.PositiveIntegerField()
    imageUrl = models.CharField(max_length=255, blank=True)
    video = models.CharField(max_length=255, blank=True, null=True)

    description_ru = models.TextField()
    description_en = models.TextField()
    description_tj = models.TextField()

    def __str__(self):
        return self.name_en  # default display

class TeachersPage(models.Model):
    englishLanguage_ru = models.CharField(max_length=255)
    englishLanguage_en = models.CharField(max_length=255)
    englishLanguage_tj = models.CharField(max_length=255)

    online_ru = models.TextField()
    online_en = models.TextField()
    online_tj = models.TextField()

    from990_ru = models.CharField(max_length=50)
    from990_en = models.CharField(max_length=50)
    from990_tj = models.CharField(max_length=50)

    weMonitor_ru = models.TextField()
    weMonitor_en = models.TextField()
    weMonitor_tj = models.TextField()

    changeGoals_ru = models.TextField()
    changeGoals_en = models.TextField()
    changeGoals_tj = models.TextField()

    selectTutor_ru = models.CharField(max_length=100)
    selectTutor_en = models.CharField(max_length=100)
    selectTutor_tj = models.CharField(max_length=100)

    teachers = models.ManyToManyField(Teacher, related_name="pages")

    def __str__(self):
        return "Teachers Page"
