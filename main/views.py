from django.shortcuts import render
from .models import Lessons
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


class BBLoginView(LoginView):
    template_name = 'registration/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'


@login_required
def main(request):
    lessons = Lessons.objects.all()
    return render(request,
                  'main.html', context={'lessons': lessons})


@login_required
def profile(request):
    return render(request, 'registration/profile.html')
