from django.urls import path
from projects import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('guest-registration/', views.AddGuestView.as_view(), name='register'),
]