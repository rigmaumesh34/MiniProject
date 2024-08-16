from django.db import models

# Create your models here.    
class Student(models.Model):
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
        # Add more departments as needed
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES)
    year_of_study = models.CharField(max_length=9)  # Format: "2023-2024"

    def __str__(self):
        return f"{self.name} ({self.department}, Year {self.year_of_study})"
    

class Item(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold_out', 'Sold Out'),
    ]

    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='items/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    student = models.ForeignKey('Student', on_delete=models.CASCADE)  # ForeignKey to Student model
    def __str__(self):
        return f"{self.item_name} - {self.status}"

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
    student = models.ForeignKey('Student', on_delete=models.CASCADE)  # ForeignKey to Student model
    def __str__(self):
        return f"{self.name} - {self.status}"
    


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
    student = models.ForeignKey('Student', on_delete=models.CASCADE)  # ForeignKey to Student model
    
    def __str__(self):
        return f"{self.name} - {self.status}"
