from django.shortcuts import render
from rest_framework import viewsets
from .models import Species, Pet, Review
from .serializers import SpeciesSerializer, PetSerializer, ReviewSerializer

# Create your views here.
class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer