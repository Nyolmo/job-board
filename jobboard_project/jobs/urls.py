from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = router.urls

router.register("companies", CompanyViewSet, basename='company')
router.register('jobs', JobViewSet, basename='job')
router.register('applications', ApplicationViewSet, basename='application')
