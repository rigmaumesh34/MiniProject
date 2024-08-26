from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from studentApp.models import Item, Student
from django.contrib import messages
import re  # For email validation
from django.contrib import messages


def index(request):
    return render(request, 'index.html')



def studentregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        year = int(request.POST.get('yearofstudy'))
        department = request.POST.get('department')
            
       
        user = User.objects.create_user(username=username, password=password, email=email)
        student=Student(user=user,name=username, email=email, password=password, phone=phone, yearofstudy=year, department=department)
        student.save()
        return redirect('studentlogin')

    return render(request,'studentregister.html')

def studentlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('studenthome')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'studentlogin.html')

    return render(request, 'studentlogin.html')

def studenthome(request):
    return render(request, 'studenthome.html', {'username': request.user.username})

def additem(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        student = Student.objects.get(user=request.user)
        item_image = request.FILES.get('itemimage')

        # Validate required fields
        if not item_name or not description or not price or not quantity or not category or not item_image:
            messages.error(request, 'All fields are required.')
            return render(request, 'additem.html')

        # Create and save the item
        try:
            item = Item.objects.create(
                student=student,
                name=item_name,
                description=description,
                price=price,
                quantity=quantity,
                category=category,
                image=item_image,
                delete_status='LIVE'
            )
            item.save()
            messages.success(request, 'Item added successfully!')
        except Exception as e:
            messages.error(request, f'Error saving item: {e}')

    return render(request, 'additem.html')

def reportitemfound(request):
    return render(request, 'reportitemfound.html')

def reportitemlost(request):
    return render(request, 'reportitemlost.html')

def studentlogout(request):
    logout(request)
    return redirect('index')

def navbar(request):
    return render(request, 'navbar.html')
