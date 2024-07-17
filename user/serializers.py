from rest_framework import serializers
from user.models import UserModel
from django.contrib.auth.models import User

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        
class UserSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    
    class Meta:
        model = UserModel
        fields = '__all__'
        
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        
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
        
        UserModel.objects.create(
            user=account,
            balance=0.00,
        )
        return account
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    
class UpdatePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'new_password': 'New passwords do not match'})
        return attrs

    def validate_user_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')
        return value

    def validate_current_password(self, value):
        user = User.objects.get(id=self.initial_data['user_id'])
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        return value