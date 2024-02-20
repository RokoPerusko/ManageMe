from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    color = models.CharField(max_length=50)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.ManyToManyField(Task, related_name='completed_in_diary_entries', blank=True)  # Dodao sam 'blank=True' za opcionalnost

    def __str__(self):
        return f"{self.title} - {self.date}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
