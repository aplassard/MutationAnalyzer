from django import forms
from django.shortcuts import render
from django.http import HttpResponse

class NewExperimentForm(forms.Form):
    experiment = forms.CharField(max_length=50)
    vcf_file   = forms.FileField()
    ped_file   = forms.FileField()

def index(request):
    return HttpResponse("This is the index")

def new(request):
    if request.method=='POST':
        return HttpResponse("This is the new POST page")
    else:
        form = NewExperimentForm()
        return render(request,'experiment/new.html',{'form':form})

def create(request):
    pass
