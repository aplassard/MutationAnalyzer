from django.db import models

class Mutation(models.Model):
    chrom = models.CharField(max_length=20)
    pos   = models.IntegerField()
    ref   = models.CharField(max_length=1000)
    alt   = models.CharField(max_length=1000)
