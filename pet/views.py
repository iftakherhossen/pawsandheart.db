from django.shortcuts import render
from rest_framework import viewsets, filters, pagination
from .models import Species, Pet, Review
from .serializers import SpeciesSerializer, PetSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

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
    pagination_class = PetPagination
    filter_backends = [filters.SearchFilter]    
    search_fields = ['name', 'species__name']
    
class RandomPetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.filter(adopted=False).order_by('?')[:8]
    serializer_class = PetSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        pet_id = self.request.query_params.get('pet', None)
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        return queryset     

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def perform_create(self, serializer):
        serializer.save()