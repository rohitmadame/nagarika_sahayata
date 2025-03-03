from django.urls import path
from . import views  # Correct import for views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),  # Added missing admin login URL
    path('add-complaint/', views.add_complaint, name='add_complaint'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('logout/', views.user_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)