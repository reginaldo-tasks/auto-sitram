from django.urls import path
from . import views

app_name = 'automation'

urlpatterns = [
    path('sitram/search/', views.SITRAMSearchView.as_view(), name='sitram-search'),
]
