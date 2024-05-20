from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Animal(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to="animal_images/")

    def __str__(self):
        return self.name

class Chromosome(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="chromosomes")
    number = models.IntegerField()
    start_position = models.IntegerField()
    end_position = models.IntegerField()

    def __str__(self):
        return f"Chromosome {self.number} for {self.animal.name}"

NUCLEOTIDES = [(i, i) for i in "ACTG"]
class SNP(models.Model):
    chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE, related_name='snps')
    position = models.IntegerField()
    ref = models.CharField(max_length=1, choices=NUCLEOTIDES)
    alt = models.CharField(max_length=1, choices=NUCLEOTIDES)
    maf = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    def __str__(self):
        return f"SNP at position {self.position} on Chromosome {self.chromosome.number}"

class Annotation(models.Model):
    snp = models.ForeignKey(SNP, on_delete=models.CASCADE, related_name='annotations')
    author = models.ForeignKey(User, max_length=200, on_delete=models.CASCADE, related_name='annotations')
    description = models.TextField()

    def __str__(self):
        return f"Annotation for SNP at position {self.snp.position} on Chromosome {self.snp.chromosome.number} by {self.author}"
