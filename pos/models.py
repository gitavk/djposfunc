from django.db import models


class A(models.Model):
    title = models.CharField(max_length=50)
