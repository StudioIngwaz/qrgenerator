from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_qr, name='generate_qr'),
    path('qrcode/<int:qrcode_id>/', views.qrcode_display, name='qrcode_display'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
