from django.contrib import admin
from .models import Pet, Species, Review

# Register your models here.
class SpeciesAdmin(admin.ModelAdmin):    
    prepopulated_fields = { 'slug' : ('name',), }
    
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Pet)
admin.site.register(Review)