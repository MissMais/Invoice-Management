from django.shortcuts import render
from rest_framework import viewsets
from phaseapi.models import Phase
from phaseapi.serializers import PhaseSerializer

# Create your views here.
class PhaseViewSet(viewsets.ModelViewSet):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer