
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='question'),
    path('info/', views.user_info, name='user_info'), # Сторінка введення email
    path('results/', views.results, name='results'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]