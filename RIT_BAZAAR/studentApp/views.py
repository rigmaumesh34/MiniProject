from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.
def index(request):
    
    return render(request,'index.html')

def studentlogin(request):
    return render(request,'studentlogin.html')

def studentregister(request):
    return render(request, 'studentregister.html')

def additem(request):
    return render(request,'additem.html')

def reportitemfound(request):
    return render(request,'reportitemfound.html')

def reportitemlost(request):
    return render(request,'reportitemlost.html')

def logout(request):
    pass