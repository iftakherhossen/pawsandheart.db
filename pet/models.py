from django.db import models
from user.models import UserModel

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]

# Create your models here.
class Species(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    
    def __str__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=50)
    species = models.ForeignKey(Species, related_name='species', on_delete=models.CASCADE)
    age = models.CharField(max_length=50)
    price = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    health = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="pet/images/")
    created_on = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    review = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=10, choices=STAR_CHOICES)
    
    def __str__(self):
        return f"Reviewed by {self.reviewer.user.first_name} {self.reviewer.user.last_name}"