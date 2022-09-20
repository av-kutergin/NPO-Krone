from django.urls import path
from projects import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('guest-registration/', views.AddGuestView.as_view(), name='register'),
    path('team/', views.team, name='team'),
    path('documents/', views.documents, name='documents'),
    path('reports/', views.reports, name='reports'),
    path('projects/', views.projects, name='projects'),
    path('contacts/', views.contacts, name='contacts'),
    path('donate/', views.donate, name='donate'),
    path('sitemap/', views.sitemap, name='sitemap'),
]