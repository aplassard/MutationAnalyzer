from django.http import HttpResponse
from django.shortcuts import render
from django import forms

def index(request):
    if request.method == 'POST':
        pass
    else:
        form = SubmitForm()

    return render(request, 'test/index.html', { 'form': form })

class SubmitForm(forms.Form):
    experiment = forms.CharField(max_length=100)
    user_name  = forms.CharField(max_length=100)
