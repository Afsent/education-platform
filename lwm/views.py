from django.shortcuts import render
from .models import Lessons


def main(request):
    lessons = Lessons.objects.all()
    return render(request,
                  'main.html', context={'lessons': lessons})
