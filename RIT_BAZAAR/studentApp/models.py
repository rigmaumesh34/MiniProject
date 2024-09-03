from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.    
class Student(models.Model):
   
   
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=20,unique=True)
    password=models.CharField(max_length=25,null=True)
    user=models.OneToOneField(User,related_name='student_profile',on_delete=models.CASCADE)
    phone = models.CharField(max_length=40)
    department = models.CharField(max_length=50)
    yearofstudy = models.CharField(max_length=50)  # Format: "2023-2024"
    
    
    def __str__(self):
        return f"{self.name} ({self.department}, Year {self.yearofstudy})"
    

    
    

class Item(models.Model):

   
    name = models.CharField(max_length=255,null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='items/')
    student = models.ForeignKey(Student, on_delete=models.CASCADE) # ForeignKey to Student model
    category = models.CharField(max_length=20, default='', blank=False)

    
    def __str__(self):
        return f"{self.name} ({self.price}, {self.description})"
    
    

class LostItem(models.Model):
    STATUS_CHOICES = [
        ('found', 'Found'),
        ('not_found', 'Not Found'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    lost_date = models.DateField()
    lost_time = models.TimeField()
    lost_location = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='not_found')
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # ForeignKey to Student model
    def __str__(self):
        return f"{self.name}  ({self.status}  {self.description}  {self.student})"
    


class FoundItem(models.Model):
    STATUS_CHOICES = [
        ('owner_verified', 'Owner Verified'),
        ('not_verified', 'Not Verified'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    found_date = models.DateField()
    found_time = models.TimeField()
    found_location = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_verified')
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='found_items')  # ForeignKey to Student model
    
    def __str__(self):
        return f"{self.name} ({self.description} , {self.found_location})"


    
    
class Claim(models.Model):
    image = models.ImageField(upload_to='claims/')
    description = models.TextField()
    phone_number = models.CharField(max_length=15) 
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE)
    
    
    
class complaints(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    

    def __str__(self):
        return f'Complaint by {self.student.username} , {self.student.email}'
    
    
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
    
    