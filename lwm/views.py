from django.contrib.auth import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .models import Lessons
from django.contrib.auth.decorators import login_required


@login_required
def main(request):
    lessons = Lessons.objects.all()
    return render(request,
                  'main.html', context={'lessons': lessons})
