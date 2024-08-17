from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from studentApp.models import Student
# Create your views here.
def index(request):
    
    return render(request,'index.html')

def studentlogin(request):
    return render(request,'studentlogin.html')

def studentregister(request):
    if request.POST:
        name=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        year=request.POST.get('yearofstudy')
        department=request.POST.get('department')
        password=request.POST.get('password')
        Student.objects.create(name=name,email=email,phone=phone,year_of_study=year,department=department,password=password)
        return redirect('studenthome')
    return render(request, 'studentregister.html')

def studenthome(request):
    return render(request, 'studenthome.html')

def additem(request):
    return render(request,'additem.html')

def reportitemfound(request):
    return render(request,'reportitemfound.html')

def reportitemlost(request):
    return render(request,'reportitemlost.html')

def logout(request):
    pass