from rest_framework import serializers
from .models import Transaction
from pet.serializers import PetSerializer
from django.contrib.auth.models import User

class TransactionSerializer(serializers.ModelSerializer):
    pet = PetSerializer(required=False, allow_null=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['pet', 'amount', 'transaction_type', 'account']