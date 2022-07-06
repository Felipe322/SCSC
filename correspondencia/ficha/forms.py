from django import forms

from django.forms import ModelForm

from .models import Ficha


class FichaForm(ModelForm):

    class Meta:
        model = Ficha
        fields = '__all__'

        # widgets = {
            # id_ficha
            # 'fecha': forms.TextInput(attrs={'class':'form-control'}),
            # 'asunto': forms.TextInput(attrs={'class':'form-control'}),
            # num_documento
            # fecha_documento
            # dependencia
            # nombre_firma
            # asunto
            # area_turnada
            # instruccion
            # resolucion
            # fecha_recibido
        # }

    #     proyecto = forms.ModelMultipleChoiceField(queryset=Proyecto.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
    #     tipo_defecto = forms.ModelMultipleChoiceField(queryset=TipoDefecto.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    #     fase = forms.ModelMultipleChoiceField(queryset=Fase.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    #     origen_defecto = forms.ModelMultipleChoiceField(queryset=OrigenDefecto.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    #     dependecia_defecto = forms.ModelMultipleChoiceField(queryset=Defecto.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    #     impacto = forms.ModelMultipleChoiceField(queryset=Impacto.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    #     # solucion = forms.ModelMultipleChoiceField(queryset=Solucion.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    #     fields = ('__all__')

    #     widgets = {
    #         'proyecto' : forms.Select(attrs={'class':'form-control'}),
    #         'fecha':forms.TextInput(attrs={'class':'form-control'}),
    #         'puesto_desarrollador':forms.TextInput(attrs={'class':'form-control'}),
    #         'usuario':forms.TextInput(attrs={'class':'form-control'}),
    #         'tiempo_correcion':forms.TextInput(attrs={'class':'form-control'}),
    #         'tipo_defecto':forms.Select(attrs={'class':'form-control'}),
    #         'fase':forms.Select(attrs={'class':'form-control'}),
    #         'dependecia_defecto':forms.Select(attrs={'class':'form-control'}),
    #         'origen_defecto':forms.Select(attrs={'class':'form-control'}),
    #         'commit':forms.TextInput(attrs={'class':'form-control'}),
    #         'impacto':forms.Select(attrs={'class':'form-control'}),
    #         # 'solucion':forms.Select(attrs={'class':'form-control'}),
    #         'solucion_descripcion':forms.Textarea(attrs={'class':'form-control','rows': 8}),
    #         'descripcion':forms.Textarea(attrs={'class':'form-control','rows': 8}),
    #     }