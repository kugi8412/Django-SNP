from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.contrib import admin

"""
Species – Sample: one to many
Species – SNP: one to many
Sample – SNP: many to many
"""

class Species(models.Model):
    reference_genome = models.CharField(max_length=200, unique=True, null=False)
    name = models.CharField(max_length=200, null=False)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name


class Sample(models.Model):
    name = models.CharField(max_length=200, null=False)
    sampling_date = models.DateField()
    sequencing_date = models.DateField()
    specimen = models.CharField(max_length=200)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="samples")

    class Meta:
        unique_together = ["sampling_date", "specimen", "species"]
        constraints = [
            models.CheckConstraint(check = models.Q(sequencing_date__gte = models.F("sampling_date")),
                name="sequencing_later_than_sampling")
        ]

    def __str__(self):
        return f"Sample {self.name} for {self.species.reference_genome}"


NUCLEOTIDES = [(i, i) for i in "ACTG"]

class SNP(models.Model):
    chromosome = models.IntegerField()
    coordinate = models.IntegerField()
    reference_allele = models.CharField(max_length=1, choices=NUCLEOTIDES)
    alternative_allele = models.CharField(max_length=1, choices=NUCLEOTIDES)
    MAF = models.FloatField()
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["chromosome", "coordinate", "sample"]
        constraints = [
            models.CheckConstraint(check = ~models.Q(alternative_allele = models.F('reference_allele')),
                name='snips_cannot_be_equal'),
            # MAF beetwen 0.0 and 0.5   
            models.CheckConstraint(check = models.Q(MAF__gte=0.0) & models.Q(MAF__lte=0.5),
                name='MAF_range')
        ]

    def __str__(self):
        return f"SNP at position {self.coordinate} on Chromosome {self.chromosome} of {self.sample.name}"


class Annotation(models.Model):
    group = models.CharField(max_length=200)
    text = models.CharField(max_length=10000)
    SNP = models.ForeignKey(SNP, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Annotation of the {self.group} SNP {self.SNP.sample.name}"
