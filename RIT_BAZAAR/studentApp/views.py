from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from .paytm_config import PAYTM_MERCHANT_KEY, PAYTM_MERCHANT_ID, PAYTM_WEBSITE, PAYTM_TRANSACTION_URL
from django.conf import settings
from django.core.mail import send_mail
from studentApp.models import *
from django.contrib import messages
import re  # For email validation
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .helpers import send_forget_password_mail
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Profile
import uuid
from django.contrib.auth.forms import AuthenticationForm
from .models import Item

def index(request):
    return render(request, 'index.html')

def paymentdummy(request):
    return render(request, 'paymentdummy.html')

from django.db import IntegrityError
from django.contrib import messages

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
            student = Student.objects.get(user=user)

            # Store student ID in session
            request.session['student_id'] = student.id
            return redirect('studenthome')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('studentlogin')

    return render(request, 'studentlogin.html')



def studenthome(request):
    
    student_id = request.session.get('student_id')
    if not student_id:
        messages.error(request, 'You need to log in first.')
        return redirect('studentlogin')
    student = Student.objects.get(id=student_id)
    
    return render(request, 'studenthome.html', {'student': student})

def additem(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        student = Student.objects.get(user=request.user)
        item_image = request.FILES.get('itemimage')

        
        if not item_name or not description or not price or not quantity or not category or not item_image:
            messages.error(request, 'All fields are required.')
            return render(request, 'additem.html')

        
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
            return render(request, 'additem.html', {'message': 'submitted item details to admin !'})

    
        except Exception as e:
            messages.error(request, f'Error saving item: {e}')

    return render(request, 'additem.html')





def buyitem(request):
    
    items = Item.objects.filter(delete_status='LIVE',status='approved')
    return render(request, 'buyitem.html', {'items': items})

def viewitemlost(request):
    lost_items = LostItem.objects.filter(stat='approved')
    return render(request, 'viewitemlost.html', {'lost_items': lost_items})

def viewitemfound(request):
   
    found_items = FoundItem.objects.filter(stat='approved')
    return render(request, 'viewitemfound.html', {'found_items':found_items})


def manageitem(request):
    
    students = request.user.student_profile  

    
    items = Item.objects.filter(student=students, delete_status='LIVE')

    context = {
        'items': items
    }
    return render(request, 'manageitem.html', context)



def deleteitem(request, item_id):
    item = get_object_or_404(Item, id=item_id, student=request.user.student_profile)
    
   
    # item.delete_status = Item.DELETE
    if request.method == 'POST':
        item.delete() 
        messages.success(request, 'Item deleted successfully.')  # Add a success message


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
          
            
            student = Student.objects.get(user=request.user)
          
            found_item = FoundItem(
                name=item_name,
                description=description,
               
                student=student,
                status='not_found'
            )
            found_item.save()

           
            messages.success(request, 'found item reported successfully!')

            return redirect('reportitemfound') 

    
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

           
            messages.success(request, 'Lost item reported successfully!')

            return redirect('reportitemlost')  

        return render(request, 'reportitemlost.html')
    





def manageprofile(request):
    student = Student.objects.get(email=request.user.email)  # Assuming email is unique

    if request.method == 'POST':
      
        student.name = request.POST['username']
        student.email = request.POST['email']
        student.phone = request.POST['phone']
        student.yearofstudy = request.POST['yearofstudy']
        student.department = request.POST['department']
        student.password=request.POST['password'] 

       
        student.save()

       
        messages.success(request, 'Profile updated successfully!')
        return redirect('manageprofile')

    return render(request, 'manageprofile.html', {'student': student})


def studentlogout(request):
    logout(request)
    return redirect('index')



def navbar(request):
    return render(request, 'navbar.html')




def claimitem(request, found_item_id):
    
    found_item = get_object_or_404(FoundItem, id=found_item_id)

    if request.method == 'POST':
        

        
        image = request.FILES.get('image')
        description = request.POST.get('description')
        phone_number = request.POST.get('phone_number')
        lost_location = request.POST.get('lost_location')
        lost_date = request.POST.get('lost_date')
        lost_time = request.POST.get('lost_time')

       
        if  not phone_number or not lost_location or not lost_date or not lost_time:
            messages.error(request, 'All fields are required.')
            return render(request, 'claimitem.html', {'found_item': found_item}) 

        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, 'Please enter a valid 10-digit phone number.')
            return render(request, 'claimitem.html', {'found_item': found_item})
        
        
        claim = Claim(
            image=image,
            description=description,
            phone_number=phone_number,
            lost_location=lost_location,
            lost_date=lost_date,
            lost_time=lost_time,
            found_item=found_item 
        )
        
        
        
        claim.save()
        return render(request, 'claimitem.html', {'found_item': found_item, 'message':'Your claim has been successfully submitted.'})
       
        return redirect('viewitemfound') 

    return render(request, 'claimitem.html', {'found_item': found_item})

   
    
def viewclaim(request):
    student_id = request.session.get('student_id')

    found_items = FoundItem.objects.filter(student_id=student_id)
    found_item_ids = found_items.values_list('id', flat=True)
    claims = Claim.objects.filter(found_item__in=found_item_ids)
    return render(request, 'viewclaim.html',{'claims':claims})


def complaints(request):
    if request.method == 'POST':
        description = request.POST['description']
        complaint_type = request.POST['complaint_type']
        image = request.FILES.get('image', None)
        student = request.user

       
        complaint = Complaints(
            student=student,
            description=description,
            complaint_type=complaint_type,
            image=image
        )
        complaint.save()

        messages.success(request, 'Your complaint has been submitted successfully.')
        return redirect('complaint')

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
    


def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'No user with this email exists.')
            return redirect('forgetpassword')

        try:
            
            profile_obj = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
           
            messages.error(request, 'Profile for this user does not exist.')
            return redirect('forgetpassword')

        
        token = str(uuid.uuid4())
        profile_obj.forget_password_token = token
        profile_obj.save()

        
        send_forget_password_mail(user, token)
        messages.success(request, 'An email has been sent with a link to reset your password.')
        return redirect('forgetpassword')

    return render(request, 'forgetpassword.html')


def confirmpassword(request, token):
    try:
       
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

def manageevent(request):
    events = Events.objects.all()
    return render(request, 'manageevent.html', {'events': events})

def deleteevent(request,event_id):
    event = get_object_or_404(Events, id=event_id)
    if request.method == 'POST':
        event.delete()
    
    return redirect('manageevent')







def manageitemfound(request):
    student = request.user.student_profile
    items = student.found_items.all()  
    context = {
        'items': items
    }
    return render(request, 'manageitemfound.html', context)

def manageitemlost(request):
    student = request.user.student_profile
    items = student.lost_items.all()  
    context = {
        'items': items
    }
    return render(request, 'manageitemlost.html', context)



def deleteitemfound(request, item_id):

    item = get_object_or_404(FoundItem, id=item_id, student=request.user.student_profile)
    item.delete()

    messages.success(request, 'Item deleted successfully.')
    return redirect('manageitemfound')


def deleteitemlost(request, item_id):

    item = get_object_or_404(LostItem, id=item_id, student=request.user.student_profile)
    item.delete()

    messages.success(request, 'Item deleted successfully.')
    return redirect('manageitemlost')

def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        if username == "admin" and password == "password":
            
            return redirect('adminhome')
        else:
            
            messages.error(request, "Invalid username or password")
    
    return render(request, 'adminlogin.html')
   


def adminhome(request):
    if not request.session.get('admin_id'):
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    items = Item.objects.filter(delete_status='LIVE',status='pending')
    return render(request, 'adminhome.html', {'items': items})

def manageitemlost_admin(request):
    if not request.session.get('admin_id'):
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    items = LostItem.objects.filter(stat='pending')
    return render(request, 'mangeitemlost_admin.html', {'items': items})

def manageitemfound_admin(request):
    if not request.session.get('admin_id'):
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    items = FoundItem.objects.filter(stat='pending')
    return render(request, 'manageitemfound_admin.html', {'items': items})



def send_item_notification(item, status):
    """
    Sends an email to the item's owner regarding the approval/rejection status.
    """
    subject = f"Your item '{item.name}' has been {status}!"
    message = f"Dear {item.student.name},\n\n" \
              f"Your item '{item.name}' has been {status} by the admin.\n" \
              f"Thank you for using our platform."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [item.student.email] 

    send_mail(
        subject,      
        message,     
        from_email,  
        recipient_list,
        fail_silently=False,
    )

def send_item_notification_lost(item, stat):
    """
    Sends an email to the item's owner regarding the approval/rejection status.
    """
    subject = f"Your item '{item.name}' has been {stat}!"
    message = f"Dear {item.student.name},\n\n" \
              f"Your item '{item.name}' has been {stat} by the admin.\n" \
              f"Thank you for using our platform."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [item.student.email] 

    send_mail(
        subject,      
        message,     
        from_email,  
        recipient_list,
        fail_silently=False,
    )

def send_item_notification_found(item, stat):
    """
    Sends an email to the item's owner regarding the approval/rejection status.
    """
    subject = f"Your item '{item.name}' has been {stat}!"
    message = f"Dear {item.student.name},\n\n" \
              f"Your item '{item.name}' has been {stat} by the admin.\n" \
              f"Thank you for using our platform."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [item.student.email] 

    send_mail(
        subject,      
        message,     
        from_email,  
        recipient_list,
        fail_silently=False,
    )



def approve_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.status = 'approved'
    item.save()

  
    send_item_notification(item, 'approved')

    return redirect('adminhome')

def approve_item_lost(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)
    item.stat = 'approved'
    item.save()

  
    send_item_notification_lost(item, 'approved')

    return redirect('mangeitemlost_admin')



def approve_item_found(request, item_id):
    item = get_object_or_404(FoundItem, id=item_id)
    item.stat = 'approved'
    item.save()

  
    send_item_notification_found(item, 'approved')

    return redirect('manageitemfound_admin')


# def approve_item_found(request, item_id):
#     item = get_object_or_404(FoundItem, id=item_id)
#     item.stat = 'approved'
#     item.save()

  
#     send_item_notification(item, 'approved')

#     return redirect('manageitemfound_admin')





def reject_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.status = 'rejected'
    item.save()

   
    send_item_notification(item, 'rejected')

    return redirect('adminhome') 
 
def reject_item_lost(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)
    item.stat = 'rejected'
    item.save()

   
    send_item_notification_lost(item, 'rejected')

    return redirect('mangeitemlost_admin')


def reject_item_found(request, item_id):
    item = get_object_or_404(FoundItem, id=item_id)
    item.stat = 'rejected'
    item.save()

   
    send_item_notification_found(item, 'rejected')

    return redirect('manageitemfound_admin')
    
# def approve_item(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     item.status = 'approved'  # Assuming you have a status field
#     item.save()
#     return redirect('adminhome')

# def reject_item(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     item.status = 'rejected'
#     item.save()
#     return redirect('adminhome')

# User Login View
def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                admins = Admin.objects.get(user=user)

                request.session['admin_id'] = admins.id
                return redirect('adminhome')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'adminlogin.html', {'form': form})


def admin_logout(request):
    logout(request)

    return redirect('adminlogin')


def view_complaints(request):
   
    complaints = Complaints.objects.all()

   
    return render(request, 'viewcomplaints.html', {'complaints': complaints})




def admin_addevent(request):
    mess = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        dateofevent = request.POST.get('dateofevent')
        timeofevent = request.POST.get('timeofevent')
        image = request.FILES.get('image')

        
        event = Events(
            name=name,
            description=description,
            location=location,
            dateofevent=dateofevent,
            timeofevent=timeofevent,
            image=image
        )
        event.save()

        
        mess='Event has been added successfully!'

    return render(request, 'adminaddevent.html',{'mess':mess})

# def initiate_payment(request, item_id):
#     # Assuming you have the item and price logic here
#     item = Item.objects.get(id=item_id)
#     price = item.price  # For example, ₹500
#     student_email = request.user.email  # Assuming user is logged in

#     # Payment data
#     paytm_params = {
#         'MID': PAYTM_MERCHANT_ID,
#         'ORDER_ID': str(item_id) + '_' + str(request.user.id),
#         'CUST_ID': student_email,
#         'TXN_AMOUNT': str(price),
#         'CHANNEL_ID': 'WEB',
#         'WEBSITE': PAYTM_WEBSITE,
#         'INDUSTRY_TYPE_ID': 'Retail',
#         'CALLBACK_URL': settings.PAYTM_CALLBACK_URL
#     }

#     # Generating checksum
#     checksum = paytmchecksum.generateSignature(paytm_params, PAYTM_MERCHANT_KEY)
#     paytm_params['CHECKSUMHASH'] = checksum

#     # Sending request to Paytm payment gateway
#     return render(request, 'redirect_to_paytm.html', {'paytm_params': paytm_params, 'PAYTM_TRANSACTION_URL': PAYTM_TRANSACTION_URL})

# def handle_payment(request):
#     received_data = dict(request.POST.items())
#     paytm_checksum = received_data.pop('CHECKSUMHASH', None)
#     is_valid_checksum = paytmchecksum.verifySignature(received_data, PAYTM_MERCHANT_KEY, paytm_checksum)

#     if is_valid_checksum:
#         # Payment verified
#         if received_data['RESPCODE'] == '01':
#             # Payment successful
#             return HttpResponse("Payment successful")
#         else:
#             # Payment failed
#             return HttpResponse(f"Payment failed because {received_data['RESPMSG']}")
#     else:
#         # Invalid checksum
#         return HttpResponse("Checksum verification failed")