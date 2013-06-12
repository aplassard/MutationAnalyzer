from django.db import models

class Family(models.Model):
    family_name = models.CharField(max_length=200)

