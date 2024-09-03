from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from studentApp.models import *
from django.contrib import messages
import re  # For email validation
from django.contrib import messages
from django.http import JsonResponse
from .helpers import send_forget_password_mail
import uuid
from django.views.decorators.csrf import csrf_exempt

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
        profile_obj=Profile.objects.create(user=user)
        profile_obj.save()
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
            return redirect('studentlogin')

    return render(request, 'studentlogin.html')



def studenthome(request):
    if request.user.is_authenticated:
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





def buyitem(request):
    
    items = Item.objects.filter(delete_status='LIVE')
    return render(request, 'buyitem.html', {'items': items})


def manageitem(request):
    # Assuming `request.user` is linked to your `Student` model
    students = request.user.student_profile  # Assuming there is a `OneToOne` relationship between User and Student

    # Retrieve all items for the logged-in student that are not deleted
    items = Item.objects.filter(student=students, delete_status='LIVE')

    context = {
        'items': items
    }
    return render(request, 'manageitem.html', context)



def deleteitem(request, item_id):
    item = get_object_or_404(Item, id=item_id, student=request.user.student_profile)
    
    # Mark the item as deleted
    item.delete_status = Item.DELETE
    item.save()

    messages.success(request, 'Item deleted successfully.')
    return redirect('manageitem')


def edititem(request, item_id):
    item = get_object_or_404(Item, id=item_id, student=request.user.student_profile)
    
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')
        item.quantity = request.POST.get('quantity')
        item.category = request.POST.get('category')
        item.save()
        return redirect('manageitem')
    
    return render(request, 'edititem.html', {'item': item})


def reportitemfound(request):
    if request.method == 'POST':
       
            item_name = request.POST.get('itemName')
            description = request.POST.get('description')
            location_found = request.POST.get('location')
            date_found = request.POST.get('dateFound')
            time_found = request.POST.get('timeFound')
            
            student = Student.objects.get(user=request.user)
            # Create a new LostItem object and save it to the database
            found_item = FoundItem(
                name=item_name,
                description=description,
                found_location=location_found,
                found_date=date_found,
                found_time=time_found,
               
                student=student,
                status='not_found'
            )
            found_item.save()

            # Display success message
            messages.success(request, 'found item reported successfully!')

            return redirect('reportitemfound')  # Redirect to the same form or another page

    
    return render(request, 'reportitemfound.html')



def reportitemlost(request):
    
        if request.method == 'POST':
            item_name = request.POST.get('itemName')
            description = request.POST.get('description')
            location_lost = request.POST.get('location')
            date_lost = request.POST.get('dateLost')
            time_lost = request.POST.get('timeLost')
            item_image = request.FILES.get('itemImage')
            student = Student.objects.get(user=request.user)
            # Create a new LostItem object and save it to the database
            lost_item = LostItem(
                name=item_name,
                description=description,
                lost_location=location_lost,
                lost_date=date_lost,
                lost_time=time_lost,
                image=item_image,
                student=student,
                status='not_found'
            )
            lost_item.save()

            # Display success message
            messages.success(request, 'Lost item reported successfully!')

            return redirect('reportitemlost')  # Redirect to the same form or another page

        return render(request, 'reportitemlost.html')
    





def manageprofile(request):
    student = Student.objects.get(email=request.user.email)  # Assuming email is unique

    if request.method == 'POST':
        # Get the updated data from the form
        student.name = request.POST['username']
        student.email = request.POST['email']
        student.phone = request.POST['phone']
        student.yearofstudy = request.POST['yearofstudy']
        student.department = request.POST['department']
        student.password=request.POST['password']  # Update password

        # Save the updated student object to the database
        student.save()

        # Display a success message
        messages.success(request, 'Profile updated successfully!')
        return redirect('manageprofile')

    return render(request, 'manageprofile.html', {'student': student})


def studentlogout(request):
    logout(request)
    return redirect('index')



def navbar(request):
    return render(request, 'navbar.html')


def viewitemfound(request):
   
    found_items = FoundItem.objects.all()
    context = {
        'found_items': found_items
    }
    return render(request, 'viewitemfound.html', context)



def claimitem(request):

    return render(request, 'claimitem.html')

def viewitemlost(request):
    lost_items = LostItem.objects.select_related('student').all()
    return render(request, 'viewitemlost.html', {'lost_items': lost_items})

def complaints(request):
    if request.method == 'POST':
        description = request.POST['description']
        student = request.user

        complaint = complaints(student=student, description=description)
        complaint.save()

        messages.success(request, 'Your complaint has been submitted successfully.')
        return redirect('studenthome')

    return render(request, 'complaint.html')

# def forgetpassword(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         if not User.objects.filter(username=username).first():
#             messages.success(request,'No user with this name')
#             return redirect('forgetpassword')
#         user_obj=User.objects.get(username=username)
#         token=str(uuid.uuid4())
#         send_forget_password_mail(user_obj,token)
#         messages.success(request,'An email is sent')
#         return redirect('forgetpassword')
#     return render(request,'forgetpassword.html')


# def confirmpassword(request, token):
#     profile_obj=Profile.objects.get(orget_password_token=token)
#     return render(request,'confirmpassword.html')
    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
import uuid

def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if a user with the provided email exists
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'No user with this email exists.')
            return redirect('forgetpassword')

        try:
            # Attempt to get the Profile object associated with the user
            profile_obj = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            # Handle the case where the Profile does not exist
            messages.error(request, 'Profile for this user does not exist.')
            return redirect('forgetpassword')

        # Generate a token and save it to the profile
        token = str(uuid.uuid4())
        profile_obj.forget_password_token = token
        profile_obj.save()

        # Send an email with the password reset link
        send_forget_password_mail(user, token)
        messages.success(request, 'An email has been sent with a link to reset your password.')
        return redirect('forgetpassword')

    return render(request, 'forgetpassword.html')


def confirmpassword(request, token):
    try:
        # Find the profile with the corresponding token
        profile_obj = Profile.objects.get(forget_password_token=token)
        user = profile_obj.user

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect(f'/confirmpassword/{token}/')

            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password has been reset successfully.')
            return redirect('studentlogin')

        return render(request, 'confirmpassword.html', {'token': token})

    except Profile.DoesNotExist:
        messages.error(request, 'Invalid or expired token.')
        return redirect('forgetpassword')
    
    
    
    
    
    
    
    
    


def eventss(request):
    events = Events.objects.all()
    return render(request, 'events.html', {'events': events})


def manageitemfound(request):
    student = request.user.student_profile
    items = student.found_items.all()  
    context = {
        'items': items
    }
    return render(request, 'manageitemfound.html', context)



def deleteitemfound(request, item_id):

    item = get_object_or_404(FoundItem, id=item_id, student=request.user.student_profile)
    item.delete()

    messages.success(request, 'Item deleted successfully.')
    return redirect('manageitemfound')


