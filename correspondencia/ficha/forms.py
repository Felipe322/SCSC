from django import forms

from django.forms import ModelForm

from .models import Ficha, Dependencia, Area


class FichaForm(forms.ModelForm):

    class Meta:
        model = Ficha

        fecha = forms.TimeField()
        fecha_documento = forms.TimeField()
        dependencia = forms.ModelMultipleChoiceField(queryset=Dependencia.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
        area_turnada = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)

        fields = '__all__'

        widgets = {
            'id_ficha' : forms.TextInput(attrs={'class':'form-control'}),
            'fecha' : forms.DateField(label=('Fecha')),
            'num_documento' : forms.TextInput(attrs={'class':'form-control'}),
            'fecha_documento' : forms.TextInput(attrs={'class':'form-control'}),
            'dependencia' : forms.Select(attrs={'class':'form-control'}),
            'nombre_firma' : forms.Textarea(attrs={'class':'form-control','rows': 5}),
            'asunto' : forms.Textarea(attrs={'class':'form-control','rows': 6}),
            'area_turnada' : forms.Select(attrs={'class':'form-control'}),
            'instruccion' : forms.Textarea(attrs={'class':'form-control','rows': 6}),
            'resolucion' : forms.Textarea(attrs={'class':'form-control','rows': 6}),
            'fecha_recibido' : forms.TextInput(attrs={'class':'form-control'}),
        }
