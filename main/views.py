from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import AdvUser, SubRubric, Lesson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer
from django.contrib import messages


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'registration/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'registration/user_is_activated.html'
    else:
        template = 'registration/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                           PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль пользователя изменен'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'registration/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BBLoginView(LoginView):
    template_name = 'registration/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'registration/delete_user.html'
    success_url = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    lessons = Lesson.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        lessons = lessons.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(lessons, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'lessons': page.object_list,
               'form': form}
    return render(request, 'main/by_rubric.html', context)


@login_required
def detail(request, rubric_pk, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    ais = lesson.additionalfile_set.all()
    context = {'lesson': lesson, 'ais': ais}
    return render(request, 'main/detail.html', context)


@login_required
def profile_lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    ais = lesson.additionalfile_set.all()
    context = {'lesson': lesson, 'ais': ais}
    return render(request, 'main/profile_lesson_detail.html', context)


@login_required
def main(request):
    lessons = Lesson.objects.filter(is_active=True)[:10]
    context = {'lessons': lessons}
    return render(request, 'main.html', context)


@login_required
def profile(request):
    lessons = Lesson.objects.filter(author=request.user.pk)
    context = {'lessons': lessons}
    return render(request, 'registration/profile.html', context)
