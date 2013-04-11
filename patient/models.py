from django.db import models
from experiment.models import Experiment
from mutation.models import Mutation

class Patient(models.Model):
    experiments = models.ForeignKey(Experiment)
    name = models.CharField(max_length=200)
    affliction_status = models.BooleanField(default=False)
    mother = models.ForeignKey('Patient',null=True,blank=True,related_name='patient_mother')
    father = models.ForeignKey('Patient',null=True,blank=True,related_name='patient_father')

    def __unicode__(self):
        return name

class Patient_Mutations(models.Model):
    patient   = models.ForeignKey(Patient)
    mutation = models.ForeignKey(Mutation)
    is_homozygous = models.BooleanField()

    def __unicode__(self):
        return 'Patient: '+str(self.patient)+' Mutation: '+str(self.mutation)
