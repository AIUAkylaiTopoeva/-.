from django.urls import path, include
from .views import TaskViewset

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('tasks',TaskViewset)

urlpatterns = [
    path('',include(router.urls))
]