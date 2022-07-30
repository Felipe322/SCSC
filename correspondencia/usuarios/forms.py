from django import forms
from .models import Ajustes, Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = ('first_name','last_name','username','email','password')

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}),
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de usuario'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'}),
        }

    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AjustesForm(forms.ModelForm):
    class Meta:
        model = Ajustes

        fields = '__all__'

        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'subtitulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}),
            # 'logo': forms.ImageField()
        }
