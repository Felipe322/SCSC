from dataclasses import field
from django import forms

from django.forms import ModelForm

from .models import Ficha, Dependencia, Area


class FichaForm(forms.ModelForm):

    class Meta:
        model = Ficha

        # fecha = forms.TimeField()
        # fecha_documento = forms.TimeField()
        dependencia = forms.ModelMultipleChoiceField(queryset=Dependencia.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
        area_turnada = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)

        fields = ['id_ficha','fecha', 'num_documento', 'fecha_documento', 'dependencia','nombre_firma', 'asunto', 'area_turnada', 'instruccion','prioridad']

        widgets = {
            'id_ficha' : forms.TextInput(attrs={'class':'form-control'}),
            'fecha' : forms.DateInput(attrs={'type':'date'}),
            'num_documento' : forms.TextInput(attrs={'class':'form-control'}),
            'fecha_documento' : forms.DateInput(attrs={'type':'date'}),
            'dependencia' : forms.Select(attrs={'class':'form-control'}),
            'nombre_firma' : forms.Textarea(attrs={'class':'form-control','rows': 2}),
            'asunto' : forms.Textarea(attrs={'class':'form-control','rows': 3}),
            'area_turnada' : forms.Select(attrs={'class':'form-control'}),
            'instruccion' : forms.Textarea(attrs={'class':'form-control','rows': 3}),
            'prioridad' : forms.Select(attrs={'class':'form-control'}),
        }

class AreaForm(forms.ModelForm):
    
    class Meta:
        model = Area

        fields = '__all__'

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'siglas' : forms.TextInput(attrs={'class':'form-control'}),
            'encargado' : forms.TextInput(attrs={'class':'form-control'}),
            'puesto' : forms.TextInput(attrs={'class':'form-control'})
        }


class DependenciaForm(forms.ModelForm):
    
    class Meta:
        model = Dependencia

        fields = '__all__'

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'siglas' : forms.TextInput(attrs={'class':'form-control'}),
        }