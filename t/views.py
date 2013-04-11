from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from MutationAnalyzer.settings import UPLOAD_ROOT
from experiments.models import Experiment

from MutationAnalyzer.helpers import handle_file_upload

def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if not form.is_valid():
            message = 'Form was invalid'
        else:
            message = 'Form was valid'
            handle_file_upload(request.FILES['vcf_file'],UPLOAD_ROOT)
        return render(request, 'tests/submit.html', {'message':message })
    else:
        form = SubmitForm()
    return render(request, 'tests/submit.html', { 'form': form })

class SubmitForm(forms.Form):
    experiment = forms.CharField(max_length=50)
    user_name  = forms.CharField(max_length=50)
    vcf_file   = forms.FileField()
    ped_file   = forms.FileField()

def index(request):
    return HttpResponse("This is the index page!")

