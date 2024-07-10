from django.db import models
from user.models import User

# Create your models here.
TRANSACTION_TYPE = [
    ('Deposit', 'Deposit'),
    ('Purchase', 'Purchase')
]

class Transaction(models.Model):
    account = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']