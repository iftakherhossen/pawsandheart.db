from django.contrib import admin
from .models import UserModel

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone', 'image']
    
    def first_name(self, obj):
        return obj.user.first_name
    def last_name(self, obj):
        return obj.user.last_name
    def email(self, obj):
        return obj.user.email
    
admin.site.register(UserModel)