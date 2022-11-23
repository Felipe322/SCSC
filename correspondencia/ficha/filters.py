import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class FichaFilterHome(django_filters.FilterSet):
    class Meta:
        model = Ficha
        fields = ('area_turnada', 'prioridad', 'estatus')

class FichaFilterUser(django_filters.FilterSet):
    class Meta:
        model = Ficha
        fields = ('dependencia', 'prioridad', 'estatus')

class FichaFilter(django_filters.FilterSet):
    fecha_inicio = DateFilter(field_name="fecha", lookup_expr="gte")
    fecha_fin = DateFilter(field_name="fecha", lookup_expr="lte")
    asunto = CharFilter(field_name="asunto", lookup_expr="icontains")
    class Meta:
        model = Ficha
        fields = ('id_ficha', 'area_turnada', 'asunto', 'prioridad', 'estatus', 'dependencia')