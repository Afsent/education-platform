from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import AdvUser, SubRubric, Lesson, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm, \
    LessonForm, AIFormSet, UserCommentForm
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


class LWMPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
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


class LWMLoginView(LoginView):
    template_name = 'registration/login.html'


class LWMLogoutView(LoginRequiredMixin, LogoutView):
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
    comments = Comment.objects.filter(lesson=pk, is_active=True)
    initial = {'lesson': lesson.pk}
    context = {'lesson': lesson, 'ais': ais, 'comments': comments}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
        form = form_class(initial=initial)
        if request.method == 'POST':
            c_form = form_class(request.POST)
            if c_form.is_valid():
                c_form.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Комментарий добавлен')
            else:
                form = c_form
                messages.add_message(request, messages.WARNING,
                                     'Комментарий не добавлен')
        context['form'] = form
    else:
        context['form'] = None

    return render(request, 'main/detail.html', context)


@login_required
def profile_lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    ais = lesson.additionalfile_set.all()
    comments = Comment.objects.filter(lesson=pk, is_active=True)
    context = {'lesson': lesson, 'ais': ais, 'comments': comments}
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


@login_required
def profile_lesson_add(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=lesson)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Урок добавлен')
                return redirect('profile')
    else:
        form = LessonForm(initial={'author': request.user.pk})
        formset = AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'registration/profile_lesson_add.html', context)


@login_required
def profile_lesson_change(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            lesson = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=lesson)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Урок исправлен')
                return redirect('profile')
    else:
        form = LessonForm(instance=lesson)
        formset = AIFormSet(instance=lesson)
    context = {'form': form, 'formset': formset}
    return render(request, 'registration/profile_lesson_change.html', context)


@login_required
def profile_lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        lesson.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Урок удален')
        return redirect('profile')
    else:
        context = {'lesson': lesson}
        return render(request, 'registration/profile_lesson_delete.html',
                      context)
