from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'channels', views.ChannelsView)
router.register(r'contents', views.ContentsView)

urlpatterns = [
    path('', include(router.urls)),
]
