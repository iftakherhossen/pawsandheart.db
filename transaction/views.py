from django.shortcuts import render
from rest_framework import viewsets, pagination, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer, CreateTransactionSerializer
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from user.models import UserModel
from pet.models import Pet

# Create your views here.
def SendTransactionEmail(user, amount, key):
    mail_subject = key + ' Confirmation'
    template = 'email_template.html'
        
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
        'balance': user.account.balance,
        'key': key
    })
    send_email = EmailMultiAlternatives(mail_subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()
    
class TransactionPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = page_size
    max_page_size = 100
    
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    filter_backends = [filters.SearchFilter]  
    search_fields = ['transaction_type']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        transaction_type = self.request.query_params.get('transaction_type')
        account = self.request.query_params.get('account')
        if transaction_type:
            queryset = queryset.filter(transaction_type__iexact=transaction_type)  
        if account:
            queryset = queryset.filter(account=account)
        return queryset

class CreateTransactionApiViewSet(APIView):
    def post(self, request):
        serializer = CreateTransactionSerializer(data=request.data)
        
        if serializer.is_valid():
            pet = serializer.validated_data.get('pet')
            amount = serializer.validated_data.get('amount')
            transaction_type = serializer.validated_data.get('transaction_type')
            userId = serializer.validated_data.get('account').id
            account = get_object_or_404(UserModel, id=userId) 
            
            if transaction_type == 'Deposit':
                account.balance += amount
                account.save(update_fields=['balance'])
                message = f"${amount} has been deposited successfully!"
                
            if transaction_type == 'Purchase':
                petId = serializer.validated_data.get('pet').id
                pet = get_object_or_404(Pet, id=petId) 
                pet.adopted = True
                pet.save(update_fields=['adopted'])
                account.balance -= amount
                account.save(update_fields=['balance'])
                message = "Purchased successfully!"
            
            Transaction.objects.create(
                pet=pet,
                amount=amount,
                transaction_type=transaction_type,
                balance_after_transaction = account.balance,
                account=account,                
            ) 
            
            SendTransactionEmail(account.user, amount, transaction_type) 
                  
            return Response(message)
        return Response(serializer.errors)