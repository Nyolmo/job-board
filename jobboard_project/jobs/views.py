from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from .models import *
from .permissions import IsCompanyAdminOrReadOnly
from .pagination import StandardPagination

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active = True)
    serializer_class = JobSerializer
    pagination_class = StandardPagination
    permission_classes = [IsCompanyAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = "apps.jobs.filters.JobFilter"
    search_fields = ["title", "short_description", "company__name"]
    ordering_fields = ["posted_at", "salary_min", "salary_max"]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    pagination_class = StandardPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ["full_name", "email"]

    def perform_create(self, serializer):
        return serializer.save()
    


