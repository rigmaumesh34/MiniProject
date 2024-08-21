from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate,logout
from studentApp.models import Student
from django.contrib import messages
# Create your views here.
def index(request):
    
    return render(request,'index.html')



def studentregister(request):
    if request.POST:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            year=request.POST.get('yearofstudy')
            department=request.POST.get('department')
            
            #create user objects
            user=User.objects.create_user(username=username,password=password,email=email)
            student=Student.objects.create(user=user,phone=phone,yearofstudy=year,department=department)
            
            return redirect('studentlogin')
    else:
        return render(request,'studentregister.html')
    
def studentlogin(request):
    if request.method == 'POST':  # Check if the form was submitted
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request, user)
            return redirect('studenthome')  # Redirect to the view name, not an HTML file
        else:
            
            return render(request, 'studentlogin.html')  # Re-render the login page with error message

    # If it's a GET request, just render the login page
    return render(request, 'studentlogin.html')
        
        
        
def studenthome(request):
    return render(request, 'studenthome.html',{'username': request.user.username})

def additem(request):
    return render(request,'additem.html')

def reportitemfound(request):
    return render(request,'reportitemfound.html')

def reportitemlost(request):
    return render(request,'reportitemlost.html')

def studentlogout(request):
    logout(request)
    return redirect('index')

def navbar(request):
    return render(request,'navbar.html')