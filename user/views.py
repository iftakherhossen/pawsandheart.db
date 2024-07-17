from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import UserModel
from .serializers import UserSerializer, RegistrationSerializer, LoginSerializer, UpdatePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user', None)
        user = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save() 
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/user/activate_email/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Your registration has been completed! A verification email has been sent!")
        return Response(serializer.errors)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=self.request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credentials!"})
        return Response(serializer.errors)
    
class UserLogOutApiView(APIView):
     def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response('Logged out successfully!')
            
class UpdatePasswordApiView(APIView):
    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            new_password = serializer.validated_data['new_password']
            
            userInfo = UserModel.objects.get(id=user_id).user
            userInfo.set_password(new_password)
            userInfo.save()

            email_subject = "Password updated confirmation"
            email_body = render_to_string('update_password.html')
            email = EmailMultiAlternatives(email_subject, '', to=[userInfo.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response({'success': 'Password updated successfully'})
        return Response({'error': serializer.errors})