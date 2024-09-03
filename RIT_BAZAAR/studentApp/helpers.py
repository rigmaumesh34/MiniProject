from django.core.mail import send_mail

from  django.conf import settings

from .models import Student


# def send_forget_password_mail(user, token):
    
    
#     subject='your forget password link'
#     message=f'Hi, click o the link to reset the password http://127.0.0.1:8000/confirmpassword/'
#     email_from=settings.EMAIL_HOST_USER
#     recepient_list=[user.email]
#     send_mail(subject,message,email_from,recepient_list)
#     return True

def send_forget_password_mail(user, token):
    subject = "Your password reset link"
    message = f"Hi {user.username},\n\nPlease click the link below to reset your password:\n\nhttp://127.0.0.1:8000/confirmpassword/{token}/"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)
    