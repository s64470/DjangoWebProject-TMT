"""
Definition of Database models.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        ('F', 'Fast Lane'),
    ]
    due_date = models.DateField(null=True, blank=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='L',
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']