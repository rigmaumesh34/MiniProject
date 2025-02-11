from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.   
from django.core.exceptions import ValidationError 
class Student(models.Model):
   
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=20,unique=True)
    password=models.CharField(max_length=25,null=True)
    user=models.OneToOneField(User,related_name='student_profile',on_delete=models.CASCADE)
    phone = models.CharField(max_length=40)
    department = models.CharField(max_length=50)
    yearofstudy = models.CharField(max_length=50) 
    
    def __str__(self):
        return f"{self.name} ({self.department}, Year {self.yearofstudy},{self.phone})"
    

    
    

class Item(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    DELETE_CHOICES=(1,'Live'),(0,'Delete')
    name = models.CharField(max_length=255,null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='items/')
    delete_status=models.CharField(choices=DELETE_CHOICES,default='LIVE')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, default='', blank=False)
    paid=models.CharField(max_length=20, default='NOT PAID', blank=False)
    u=models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    
    def __str__(self):
        return f"{self.name} ({self.price}, {self.description},{self.student})"
    
    

class LostItem(models.Model):

    STAT_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    lost_date = models.DateField()
    lost_time = models.TimeField()
    lost_location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='lost_items')
    stat = models.CharField(
        max_length=10,
        choices=STAT_CHOICES,
        default='pending',
    ) 
    def __str__(self):
        return f"{self.name}  ({self.lost_date} , {self.lost_time} , {self.lost_location}, {self.student})"
    


class FoundItem(models.Model):
  
    STAT_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    # found_date = models.DateField()
    # found_time = models.TimeField()
    # found_location = models.CharField(max_length=255)
    
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='found_items')  
    stat = models.CharField(
        max_length=10,
        choices=STAT_CHOICES,
        default='pending'
    )
    def __str__(self):
        return f"{self.name} ({self.description} , {self.student},)"


    
    
class Claim(models.Model):
    image = models.ImageField(upload_to='claims/')
    description = models.TextField()
    lost_location = models.CharField(max_length=25)
    lost_date = models.DateField()
    lost_time = models.TimeField()
    phone_number = models.CharField(max_length=10)
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE)
 
    
    
class Complaints(models.Model):
    COMPLAINT_TYPE_CHOICES = [
        ('LF', 'Lost and Found'),
        ('BS', 'Buy and Sell'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='complaint/', blank=True, null=True)
    description = models.TextField()
    complaint_type = models.CharField(max_length=2, choices=COMPLAINT_TYPE_CHOICES)

  
    def __str__(self):
        return f'Complaint by {self.student.username} , {self.student.email}, for {self.complaint_type},{self.image},{self.description},'
    
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
class Events(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField()
    location=models.TextField()
    dateofevent=models.DateField()
    timeofevent=models.TimeField()
    image = models.ImageField(upload_to='eventimages/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}, {self.location},  {self.description} , {self.dateofevent}, {self.timeofevent}"
    
class Admin(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    user=models.OneToOneField(User,related_name='admin_profile',on_delete=models.CASCADE)
    
class Payment(models.Model):
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    
    
    payment_status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    buyer_user = models.ForeignKey(User, on_delete=models.CASCADE)
    refund_status=models.CharField(max_length=10,default='False')
    refund_description=models.TextField(default='n')
    refund_image=models.ImageField(upload_to='refund/', default='items/book.jpg')
    refund_date=models.CharField(max_length=10)
    
    
    def __str__(self):
        return f'Payment {self.item} - {self.transaction_id} {self.buyer_user}'
    

    