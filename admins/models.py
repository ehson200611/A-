from django.db import models

# --- Users/Admin ---
class AdminUser(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superadmin', 'SuperAdmin')
    ]
    name = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    joinDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

# --- Notifications ---
class NotificationAdmin(models.Model):
    TYPE_CHOICES = [
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    STATUS_CHOICES = [
        ('read', 'Read'),
        ('unread', 'Unread')
    ]
    title = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.title} ({self.status})"

# --- SuperAdmin admins ---
class AdminForSuperAdmin(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, default='admin')
    joinDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

# --- Test Admin ---
class TestAdmin(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('not_started', 'Not Started')
    ]
    userName = models.CharField(max_length=255)
    level = models.CharField(max_length=10)
    dateCompleted = models.DateTimeField(null=True, blank=True)
    timeSpent = models.CharField(max_length=50, null=True, blank=True)
    totalQuestions = models.IntegerField()
    correctAnswers = models.IntegerField(null=True, blank=True)
    incorrectAnswers = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.userName} ({self.level})"
