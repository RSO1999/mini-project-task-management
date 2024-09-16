from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse


class TodoItem(models.Model):
    LEVEL_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)  # FOREIGN KEY

    title = models.CharField(max_length=50, null=False,
                             blank=False, default="My Task")
    description = models.TextField(max_length=500, null=True, blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.date.today)
    priority = models.CharField(
        max_length=10, choices=LEVEL_CHOICES, default='M')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date']
