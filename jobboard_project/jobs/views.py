from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .serializers import *

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []

class JobViewSet(viewsets.ModelViewSet):
    queryset =Job.objects.filter(is_active=True).select_related('company')
    serializer_class = JobSerializer
    permission_classes = []

    def get_queryset(self):
        qs = super().get_queryset()
        
           
