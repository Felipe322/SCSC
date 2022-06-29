from django.http import HttpResponse


def usuarios(request):
    return HttpResponse("Hello, world. From User page.")