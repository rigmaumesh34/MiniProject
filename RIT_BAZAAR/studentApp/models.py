from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.    
class Student(models.Model):
   
    LIVE=1
    DELETE=0
    DELETE_CHOICES = [(LIVE,'live'),(DELETE,'delete')]
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=20,unique=True)
    password=models.CharField(max_length=256,null=True)
    user=models.OneToOneField(User,related_name='student_profile',on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    yearofstudy = models.CharField(max_length=50)  # Format: "2023-2024"
    password=models.CharField(max_length=20)
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=1)
    
    def __str__(self):
        return f"{self.name} ({self.department}, Year {self.yearofstudy})"
    

    

class Item(models.Model):

    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'LIVE'),(DELETE,'DELETE'))
    name = models.CharField(max_length=255,null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='items/')
    delete_status = models.CharField(max_length=10, choices=DELETE_CHOICES, default='LIVE')
    student = models.ForeignKey(Student, on_delete=models.CASCADE) # ForeignKey to Student model
    category = models.CharField(max_length=20, default='', blank=False)

    
    def __str__(self):
        return f"{self.name} ({self.price}, {self.description})"
    
    
    
# class Order(models.Model):
#     LIVE=1
#     DELETE=0
#     DELETE_CHOICES=((LIVE,'LIVE'),(DELETE,'DELETE'))
#     ORDER_CONFIRM=1
#     ORDER_REJECTED=2
#     STATUS_CHOICE=((ORDER_CONFIRM,'ORDER_CONFIRM'),(ORDER_REJECTED,"ORDER_REJECTED"))
#     delete_status = models.CharField(max_length=10, choices=DELETE_CHOICES, default='LIVE')
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
    

# class LostItem(models.Model):
#     STATUS_CHOICES = [
#         ('found', 'Found'),
#         ('not_found', 'Not Found'),
#     ]

#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     lost_date = models.DateField()
#     lost_time = models.TimeField()
#     lost_location = models.CharField(max_length=255)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='not_found')
#     image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)  # ForeignKey to Student model
#     def __str__(self):
#         return f"{self.name} - {self.status}"
    


# class FoundItem(models.Model):
#     STATUS_CHOICES = [
#         ('owner_verified', 'Owner Verified'),
#         ('not_verified', 'Not Verified'),
#     ]

#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     found_date = models.DateField()
#     found_time = models.TimeField()
#     found_location = models.CharField(max_length=255)
#     status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_verified')
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)  # ForeignKey to Student model
    
#     def __str__(self):
#         return f"{self.name} - {self.status}"
