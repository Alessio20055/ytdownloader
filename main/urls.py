from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('get-audio/', views.getAudio, name="get-audio"),
    path('error/', views.errore, name="error")
]