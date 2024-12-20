from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name
