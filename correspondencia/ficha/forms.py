from django import forms
from .models import Ficha, Dependencia, Area


class FichaForm(forms.ModelForm):

    class Meta:
        model = Ficha

        dependencia = forms.ModelMultipleChoiceField(queryset=Dependencia.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
        area_turnada = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)

        fields = '__all__'

        exclude =[
                    'resolucion',
                    'estatus',
                    'fecha_recibido',
                ]

        widgets = {
            'id_ficha': forms.TextInput(attrs={'class':'form-control'}),
            'fecha': forms.TextInput(attrs={'class':'form-control', 'type':'date'}),
            'num_documento' : forms.TextInput(attrs={'class':'form-control'}),
            'fecha_documento' : forms.TextInput(attrs={'class':'form-control', 'type':'date'}),
            'dependencia' : forms.Select(attrs={'class':'form-control'}),
            'nombre_firma' : forms.Textarea(attrs={'class':'form-control','rows': 2}),
            'asunto' : forms.Textarea(attrs={'class':'form-control','rows': 3}),
            'area_turnada' : forms.Select(attrs={'class':'form-control'}),
            'instruccion' : forms.Textarea(attrs={'class':'form-control','rows': 3}),
            'prioridad' : forms.Select(attrs={'class':'form-control'}),
            'pdf_dependencia': forms.ClearableFileInput(attrs={'class':'form-control', 'readonly':'readonly'})
        }
    
class FichaUserForm(forms.ModelForm):

    class Meta:
        model = Ficha

        dependencia = forms.ModelMultipleChoiceField(queryset=Dependencia.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
        area_turnada = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)

        fields = '__all__'

        exclude =[
            'estatus',
        ]

        widgets = {
            'id_ficha' : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'fecha': forms.TextInput(attrs={'class':'form-control', 'type':'date', 'readonly':'readonly'}),
            'num_documento' : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'fecha_documento' : forms.TextInput(attrs={'class':'form-control', 'type':'date', 'readonly':'readonly'}),
            'dependencia' : forms.Select(attrs={'class':'form-control', 'readonly':'readonly', 'disabled':'disabled'}),
            'nombre_firma' : forms.Textarea(attrs={'class':'form-control','rows': 2, 'readonly':'readonly'}),
            'asunto' : forms.Textarea(attrs={'class':'form-control','rows': 3, 'readonly':'readonly'}),
            'area_turnada' : forms.Select(attrs={'class':'form-control', 'readonly':'readonly', 'disabled':'disabled'}),
            'instruccion' : forms.Textarea(attrs={'class':'form-control','rows': 3, 'readonly':'readonly'}),
            'prioridad' : forms.Select(attrs={'class':'form-control', 'readonly':'readonly', 'disabled':'disabled'}),
            'resolucion' : forms.Textarea(attrs={'class':'form-control','rows': 2}),
            'fecha_recibido' : forms.TextInput(attrs={'class':'form-control', 'type':'date'}),
            'pdf_dependencia': forms.ClearableFileInput(attrs={'class':'form-control', 'readonly':'readonly', 'disabled':'disabled'})

        }

class AreaForm(forms.ModelForm):
    
    class Meta:
        model = Area

        fields = '__all__'

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'siglas' : forms.TextInput(attrs={'class':'form-control'}),
        }


class DependenciaForm(forms.ModelForm):
    
    class Meta:
        model = Dependencia

        fields = '__all__'

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'siglas' : forms.TextInput(attrs={'class':'form-control'}),
        }