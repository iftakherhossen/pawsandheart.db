from django.contrib import admin
from  .models import Contact

# Register your models here.
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']

admin.site.register(Contact, ContactModelAdmin)