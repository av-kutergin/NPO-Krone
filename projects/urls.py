from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

from projects import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.main_page, name='main_page'),
    path('team/', views.team, name='team'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('reports/', views.ReportListView.as_view(), name='reports'),
    path('projects/', views.projects, name='projects'),
    path('contacts/', views.contacts, name='contacts'),
    path('donate/', views.donate, name='donate'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('display_document/<int:pk>', views.display_document, name='display_document'),
    path('download/<slug:file_type>/<int:pk>', views.download_file, name='download_file'),
    path('projects/<slug:project_slug>', views.ShowProject.as_view(), name='show_project'),
    path('guest-registration/<slug:project_slug>', views.add_guest, name='register'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('how-to/<slug:project_slug>/<slug:ticket_uid>', views.how_to_view, name='how_to'),
    path('service/<slug:project_slug>/<slug:ticket_uid>', views.service_page, name='service_page'),
    path('guests/<slug:project_slug>', views.guest_list, name='guest_list'),
    path('set_arrived/<slug:ticket_uid>', views.set_arrived, name='set_arrived'),
    path('cash-desk/result-payment', views.result_payment, name='result_payment'),  # Payment ResultURL
    path('helpme', views.p_list, name='helpme'),
    path('make_carousel/<slug:project_slug>', views.make_carousel, name='make_carousel'),
    path('make_default_carousel', views.make_default_carousel, name='make_default_carousel'),
]
