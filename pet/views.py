from django.shortcuts import render
from rest_framework import viewsets, filters, pagination
from .models import Species, Pet, Review
from .serializers import SpeciesSerializer, PetSerializer, ReviewSerializer

# Create your views here.
class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    
class PetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = page_size
    max_page_size = 100
        
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = PetPagination
    search_fields = ['name', 'species__name']
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer