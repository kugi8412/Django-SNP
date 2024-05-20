from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search-snps", views.search_snps, name="search_snps"),
    path("create-animal/", views.create_animal, name="create_animal"),
]