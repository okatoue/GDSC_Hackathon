from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

def basic(request):
    return render(request, 'basic.html')