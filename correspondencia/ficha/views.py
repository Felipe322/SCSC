from django.shortcuts import render

from .models import Ficha

def home(request):
    fichas = Ficha.objects.all()
    context = {'fichas':fichas}
    return render(request, 'base.html', context)



    # posts = Post.objects.all().order_by("-id")[0:6]
    # skills = Skill.objects.all().order_by('id')
    # context = {'posts':posts, 'skills':skills}
    # return render(request, 'base/index.html', context)