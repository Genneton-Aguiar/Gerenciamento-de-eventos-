from rest_framework import routers
from django.urls import path, include
from .views import *


router = routers.DefaultRouter()
router.register(r'event', EventsViewSet )
router.register(r'users', UsersViewSet)
router.register(r'inscription', InscriptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]   