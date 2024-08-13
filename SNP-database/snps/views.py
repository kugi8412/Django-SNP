from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Species, SNP, Sample, Annotation
from .forms import RegisterForm, SNPFilterForm, AnnotationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'snps/login.html', {'form': form})

@login_required(login_url='/')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'snps/register.html', {'form': form})

# Basic statistics from the SNP database
def home(request):
    animals = Species.objects.all()
    species = animals.count()
    animal_samples = {animal.name: animal.samples.count() for animal in animals}
    samples = Sample.objects.all().count()
    snps = SNP.objects.all().count()
    annotations = Annotation.objects.all().count()

    context = {
        'species_count': species,
        'sample_count': samples,
        'snp_count': snps,
        'annotation_count': annotations,
        'animal_samples_count': animal_samples
    }

    return render(request, 'snps/home.html', context)

# snps search
def snps(request): 
    species_name = request.GET.get('chosen_species')

    if request.method == 'POST':
        form = SNPFilterForm(request.POST)
        annotations = AnnotationForm(request.POST)
        species_name = request.POST.get('chosen_species')
        region = request.POST.get('region')
        maf_min = request.POST.get('maf_min')
        maf_max = request.POST.get('maf_max')
    else:
        form = SNPFilterForm()
        annotations = AnnotationForm()
        region = None
        maf_min = None
        maf_max = None

    species = Species.objects.all()
    snps = SNP.objects.all()
    samples = Sample.objects.all()

    # Filter based on selected species
    if species_name:
        chosen_species = Species.objects.get(name=species_name)
        samples = list(samples.filter(species=chosen_species))
        snps = snps.filter(sample__in=samples)

    # Filter based on region
    if region:
        chromosome, start, end = parse_region(region)
        snps = snps.filter(chromosome=chromosome, coordinate__gte=start, coordinate__lte=end)

    # Filter based on MAF
    if maf_min and maf_max:
        snps = snps.filter(MAF__gte=maf_min, MAF__lte=maf_max)

    context = {
        'snps': snps,
        'species_name': species_name,
        'species': species, 
        'form' : form,
        'annot_form': annotations
    }

    return render(request, 'snps/snps.html', context)

def parse_region(region):
    parts = region.split(':')
    chromosome = parts[0][3:]
    start, end = parts[1].split('-')
    return int(chromosome), int(start), int(end)

@login_required(login_url='snps')
def annotations(request):
    # Add new annotation
    if request.method == 'POST':
        form = AnnotationForm(request.POST)
        if form.is_valid():
            chosen_snp = request.POST.get('chosen_snp')
            snp = SNP.objects.get(pk=chosen_snp)
            group = request.POST.get('group')
            text = request.POST.get('text')
            new_annot = Annotation(group=group, text=text, SNP=snp, author=request.user)
            new_annot.save()
    else:
        form = SNPFilterForm() 

    return redirect(snps)

@login_required(login_url='/')
def save_snp(request):
    # Show SNP with annotations
    annotations = Annotation.objects.all()

    if request.method == 'POST':
        chosen_snp = request.POST.get('chosen_snp')
        snp = SNP.objects.get(pk=chosen_snp)
        annotations = annotations.filter(SNP=snp)

    # Return data in Json format
    data = []
    for annotation in annotations:
         data.append({                    
                'group': annotation.group,
                'text': annotation.text
                })
    return JsonResponse(data, safe=False)
