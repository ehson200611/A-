from django.db import models

class HomePage(models.Model):
    data = models.JSONField()  # ҳама маълумот дар як field нигоҳ медорад

    def __str__(self):
        return "Home Page Data"
