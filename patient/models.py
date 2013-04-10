from django.db import models
from experiment.models import Experiment

class Patient(models.Model):
    experiments = models.ForeignKey(Experiment)
    name = models.CharField(max_length=200)
    affliction_status = models.BooleanField(default=False)
    mother = models.ForeignKey('Patient',null=True,blank=True)
    father = models.ForeignKey('Patient',null=True,blank=True)

    def __unicode__(self):
        return name
