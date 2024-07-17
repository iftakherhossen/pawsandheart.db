from rest_framework import serializers
from .models import Species, Pet, Review
from user.serializers import UserSerializer
    

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = '__all__'
        
class PetSerializer(serializers.ModelSerializer):
    species = serializers.StringRelatedField(many=False)
    
    class Meta:
        model = Pet
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Review
        fields = '__all__'