from django.db import models
from django.contrib.auth.models import User

class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['due_date']