from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView


def usuarios(request):
    return HttpResponse("Hello, world. From User page.")

class LoginUsuario(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm