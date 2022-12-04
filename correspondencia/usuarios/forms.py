from django import forms

from ficha.models import Area
from .models import Ajustes, Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        area = forms.ModelMultipleChoiceField(queryset=Area.objects.all().filter(), required=True, widget=forms.CheckboxSelectMultiple)

        fields = ('first_name','last_name','username','email','area','puesto')

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre(s)'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido(s)'}),
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuario'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'area' : forms.Select(attrs={'class':'form-control', 'placeholder':'Area a la que pertenece el usuario'}),
            'puesto' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Puesto del usuario'})
        }

    # def __init__(self, *args, **kwargs):
    #     super(UsuarioForm, self).__init__(*args, **kwargs)
    #     self.fields['area'].queryset = Usuario.objects.filter(area__isnull=True)

class AjustesForm(forms.ModelForm):
    class Meta:
        model = Ajustes

        fields = '__all__'

        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'subtitulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}),
        }
