from django.db import models

class Experiment(models.Model):
    name=model.CharField(max_length=50)
    start_date = models.DateTimeField()
