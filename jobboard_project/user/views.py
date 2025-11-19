from rest_framework import viewsets, permissions
from .serializers import *
from .models import *


# Create your views here.
class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [] 