from django.db import models
from experiment.models import Experiment
from mutation.models import Mutation
from family.models import Family

class Patient(models.Model):
    experiment = models.ForeignKey(Experiment)
    patient_name = models.CharField(max_length=200)
    affliction_status = models.BooleanField(default=False)
    mother = models.ForeignKey('Patient',null=True,blank=True,related_name='patient_mother')
    father = models.ForeignKey('Patient',null=True,blank=True,related_name='patient_father')
    gender = models.CharField(max_length=10)
    family = models.ForeignKey(Family,related_name = 'family')

    def __unicode__(self):
        return '{ name: %s, experiment: %s }' % (self.patient_name,str(self.experiment.id))

class Patient_Mutation(models.Model):
    patient   = models.ForeignKey(Patient)
    mutation = models.ForeignKey(Mutation)
    is_homozygous = models.BooleanField()

    def __unicode__(self):
        return 'Patient: '+str(self.patient)+' Mutation: '+str(self.mutation)
