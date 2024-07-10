from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import UserModel

class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    
    class Meta:
        model = UserModel
        fields = '__all__'
        
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['image', 'username', 'first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password']
        
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password Doesn't Match!"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': "This Username Already Exists!"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "This Email Already Exists!"})        
        
        account = User(username=username, first_name=first_name, last_name=last_name, email=email)
        account.set_password(password)
        account.is_active=False
        account.save()
        return account
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)