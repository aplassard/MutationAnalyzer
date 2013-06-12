from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from MutationAnalyzer.settings import UPLOAD_ROOT
from MutationAnalyzer.helpers import handle_file_upload, parse_vcf
from experiment.models import Experiment
from django.utils import timezone
from patient.models import Patient
from family.models import Family

def parse_ped(ped_file,experiment_id):
    f = open(ped_file,'r')
    f.readline()
    patients = []
    for line in f:
        line = line.strip().split(',')
        p = Patient(patient_name = line[0], affliction_status=line[6]=='1', family=Family.objects.get_or_create(family_name=line[1])[0], gender= ('male' if line[5]=='0' else 'female'),experiment=Experiment.objects.get(pk=experiment_id))
        patients.append(p)
    Patient.objects.bulk_create(patients)
    print 'Saved %s Patients in the First Pass' % len(patients)
    f.close()
    f = open(ped_file,'r')
    f.readline()
    patients = []
    for line in f:
        changed = False
        line = line.strip().split(',')
        p = Patient.objects.get(patient_name=line[0],experiment_id__exact=experiment_id)
        if line[3] != '?':
            changed=True
            p.father = Patient.objects.get(patient_name=line[3],experiment_id__exact=experiment_id)
        if line[4] != '?':
            changed=True
            p.mother = Patient.objects.get(patient_name=line[4],experiment_id__exact=experiment_id)
        if changed:
            patients.append(p)
            p.save()
    print 'Updated %s Patients in the Second Pass' % len(patients)

class NewExperimentForm(forms.Form):
    experiment = forms.CharField(max_length=50)
    vcf_file   = forms.FileField()
    ped_file   = forms.FileField()

def index(request):
    return HttpResponse("This is the index")

def new(request):
    if request.method=='POST':
        form = NewExperimentForm(request.POST, request.FILES)
        if form.is_valid():
            e = Experiment(name=request.POST['experiment'],start_date = timezone.now())
            e.save()
            print '** Saved Experiment %s, id: %s **' % (str(e),e.id,)
            handle_file_upload(request.FILES['vcf_file'],UPLOAD_ROOT+str(e.id)+'.vcf')
            print '** Uploaded File %s **' % request.FILES['vcf_file'].name
            handle_file_upload(request.FILES['ped_file'],UPLOAD_ROOT+str(e.id)+'.ped')
            print '** Uploaded File %s **' % request.FILES['ped_file'].name
            return redirect('/experiment/'+str(e.id)+'/create/')
        else:
            return HttpResponse("The form is invalid")
    else:
        form = NewExperimentForm()
        return render(request,'experiment/new.html',{'form':form})

def create(request,experiment_id):
    parse_ped(UPLOAD_ROOT+str(experiment_id)+'.ped',experiment_id)
    parse_vcf(UPLOAD_ROOT+str(experiment_id)+'.vcf',experiment_id)
    return HttpResponse("Pedigree loaded Successfully\n<br />VCF Parsed Successfully")
