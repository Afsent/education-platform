from django.shortcuts import render
from .models import Lessons


def index(request):
    lessons = Lessons.objects.all()
    return render(request,
                  'index.html', context={'lessons': lessons})
