from django.db import models


class Profile(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.CharField(max_length=100)

    def __str__(self):
        return self.name