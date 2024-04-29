from django.db import models
from django.urls import reverse
from datetime import date

class Comment(models.Model):
    text = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True)
    published_from = models.DateField(default=date.today)

    def __str__(self):
        return self.text
