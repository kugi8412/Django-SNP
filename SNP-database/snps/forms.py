from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Annotation, SNP

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SNPFilterForm(forms.Form):
    region = forms.CharField(
        label = 'Region',
        widget = forms.TextInput(attrs={'placeholder': 'chr1:001-1000', 'pattern': '^chr\d+:\d+-\d+$', 
                                      'class': 'form-control', 'style': 'max-width: 400px;',
                                      'id': 'id_region'})
    )

    maf_min = forms.DecimalField(
        label = 'Min. value',
        widget = forms.NumberInput(attrs={'min': '0', 'max': '1', 'step': '0.01', 'id': 'id_maf_min',
                                        'class': 'form-control', 'style': 'max-width: 100px;'})
    )

    maf_max = forms.DecimalField(
        label = 'Max. value',
        widget = forms.NumberInput(attrs={'min': '0', 'max': '0.5', 'step': '0.01', 'id': 'id_maf_max',
                                        'class': 'form-control', 'style': 'max-width: 100px;'})
    )


class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = ['group', 'text']
        widgets = {
            'group' : forms.TextInput(attrs={'class' : 'form-control'}),
            'text' : forms.Textarea(attrs={'class' : 'form-control'}),
        }
        labels = {
            'group': 'Group',
            'text': 'Text',
        }
 