from django.urls import path
from projects import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('guest-registration/', views.AddGuestView.as_view(), name='register'),
    path('team/', views.team, name='team'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    # path('documents/<int:pk>', views.ShowSimpleDocument.as_view(), name='simple_document'),
    path('reports/', views.ReportListView.as_view(), name='reports'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:project_slug>', views.ShowProject.as_view(), name='show_project'),
    path('contacts/', views.contacts, name='contacts'),
    path('donate/', views.donate, name='donate'),
    path('sitemap/', views.sitemap, name='sitemap'),
]