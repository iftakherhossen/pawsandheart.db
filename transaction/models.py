from django.db import models
from user.models import UserModel
from pet.models import Pet

# Create your models here.
TRANSACTION_TYPE = [
    ('Deposit', 'Deposit'),
    ('Purchase', 'Purchase')
]

class Transaction(models.Model):
    account = models.ForeignKey(UserModel, related_name='user_details', on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, related_name='pet_details', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']