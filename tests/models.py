from django.db import models

LEVEL_CHOICES = [
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('B1', 'B1'),
    ('B2', 'B2'),
    ('C1', 'C1'),
    ('C2', 'C2'),
]

class Question(models.Model):
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    question = models.TextField()
    options = models.JSONField()  # рӯйхати ҷавобҳо
    correctAnswer = models.IntegerField()
    explanation = models.TextField()

    def __str__(self):
        return f"{self.level}: {self.question[:60]}"
