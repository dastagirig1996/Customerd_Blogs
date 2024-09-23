from django.urls import path
from . views import *
urlpatterns = [
    path('customer/', CustomerDetailView.as_view(), name='list_create'),
    path('customer/<int:id>/', CustomerDetailView.as_view(), name='get_update_delete'),
    path('login/', LoginView.as_view(), name = "login" ),
    path('refresh/',refresh_access_token_view,name= "refresh")
]
