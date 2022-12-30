from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

from projects import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.main_page, name='main_page'),
    path('team/', views.team, name='team'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('donate/', views.donate, name='donate'),
    path('download/<slug:file_type>/<int:pk>', views.download_file, name='download_file'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:project_slug>', views.ShowProject.as_view(), name='show_project'),
    path('participate/<slug:project_slug>', views.participate, name='participate'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_error/', views.payment_error, name='payment_error'),
    path('how-to/<slug:project_slug>/<slug:ticket_uid>/', views.how_to_view, name='how_to'),
    path('service/<slug:project_slug>/<slug:ticket_uid>/', views.service_page, name='service_page'),
    path('guests/<slug:project_slug>/', views.guest_list, name='guest_list'),
    path('set_arrived/<slug:ticket_uid>/', views.set_arrived, name='set_arrived'),
    path('cash-desk/result-payment/', views.result_payment, name='result_payment'),  # Payment ResultURL
    path('projects_list/', views.projects_list, name='projects_list'),
    path('make_carousel_from_project/<slug:project_slug>/', views.make_carousel_from_project, name='make_carousel_from_project'),
    path('make_carousel_default/', views.make_carousel_default, name='make_carousel_default'),
]
