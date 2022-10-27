from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

from projects import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.main_page, name='main_page'),
    path('team/', views.team, name='team'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    # path('documents/<int:pk>', views.ShowSimpleDocument.as_view(), name='simple_document'),
    path('reports/', views.ReportListView.as_view(), name='reports'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:project_slug>', views.ShowProject.as_view(), name='show_project'),
    path('contacts/', views.contacts, name='contacts'),
    path('donate/', views.donate, name='donate'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('display_document/<int:pk>', views.display_document, name='display_document'),
    path('download/<slug:file_type>/<int:pk>', views.download_file, name='download_file'),
    path('guest-registration/<slug:project_slug>', views.add_guest, name='register'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('service/<slug:project_slug>/<slug:ticket_uid>', views.service_page, name='service_page'),
    path('guests/<slug:project_slug>', views.guest_list, name='guest_list'),
    path('how-to/<slug:project_slug>/<slug:ticket_uid>', views.how_to_view, name='how_to'),
    path('set_arrived/<slug:ticket_uid>', views.set_arrived, name='set_arrived'),
    path('cash-desk/result-payment', views.result_payment, name='result_payment'),  # Payment ResultURL
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
