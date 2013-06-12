from django.db import models

class Gene(models.Model):
    gene_name = models.CharField(max_length=200)

class Transcript(models.Model):
    transcript_name = models.CharField(max_length=200)
    gene            = models.ForeignKey(Gene)

