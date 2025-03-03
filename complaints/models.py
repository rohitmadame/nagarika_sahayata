from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    COMPLAINT_TYPES = (
        ('street_light', 'Street Light'),
        ('ghanta_gadi', 'Ghanta Gadi'),
        ('waste_water', 'Waste Water'),
        ('road', 'Road'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_TYPES,default="General")
    city = models.CharField(
        max_length=100,
        default='Unknown',  # Default value added
        blank=False,
        null=False
    )
    ward_number = models.IntegerField(
        default=0,  # Default value added
        blank=False,
        null=False
    )
    landmark = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )

    def __str__(self):
        return f"{self.get_complaint_type_display()} - {self.city}"

class ComplaintImage(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='complaints/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.complaint.id}"