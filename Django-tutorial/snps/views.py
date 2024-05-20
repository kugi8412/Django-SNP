from django.shortcuts import render, redirect
from .forms import AnimalForm

def home(request):
    return render(request, "snps/home.html")

def search_snps(request):
    return render(request, "snps/search.html")

def create_animal(request):
    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AnimalForm()
    return render(request, "snps/create_animal.html", {"form": form})
