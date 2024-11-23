from django.db import models
from authapp.models import User, Organizer
from events.models import Registration

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Payment by {self.user.name} for {self.registration.event.title}"

class Payout(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payout_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    payout_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Payout request by {self.organizer.company_name}"
