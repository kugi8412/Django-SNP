from django.contrib import admin
from .models import Species, SNP, Sample, Annotation

class SpeciesAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    search_fields = ["reference_genome"]


class SampleAdmin(admin.ModelAdmin):
	list_filter = ["sampling_date", "sequencing_date"]
	search_fields = ["name"]


admin.site.register(Species, SpeciesAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(SNP)
admin.site.register(Annotation)
