from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('snps/', views.snps, name='snps'),
    path('snps/annotations', views.annotations, name='annotations'),
    path('snps/json', views.save_snp, name='save_snp'),
]
