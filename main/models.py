from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .utilities import send_activation_notification, get_timestamp_path

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True,
                                        verbose_name='Слать оповещения о новых комментариях?')
    is_teacher = models.BooleanField(default=False,
                                     verbose_name='Является учителем?')

    def delete(self, *args, **kwargs):
        for lesson in self.lesson_set.all():
            lesson.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True,
                            verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True,
                                     verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric',
                                     on_delete=models.PROTECT, null=True,
                                     blank=True,
                                     verbose_name='Надрубрика')
    description = models.TextField(default=None, null=True,
                                   verbose_name='Описание курса')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name='Изображение')


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order',
                    'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class Lesson(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT,
                               verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Урок')
    content = models.TextField(verbose_name='Oпиcaниe')
    contacts = models.TextField(verbose_name='Koнтaкты')
    video = models.CharField(max_length=140, verbose_name='Видео',
                             default=None)
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                               verbose_name='Преподаватель')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.title}'

    def delete(self, *args, **kwargs):
        for ai in self.additionalfile_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Уроки'
        verbose_name = 'Урок'
        ordering = ['-created_at']


class AdditionalFile(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               verbose_name='Урок')
    file = models.FileField(upload_to=get_timestamp_path,
                            verbose_name='Файл',
                            default=None)

    class Meta:
        verbose_name_plural = 'Дополнительные материалы'
        verbose_name = 'Дополнительная материалы'


class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               verbose_name='Объявление')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.CharField(max_length=255, verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликован')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.content}'

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-created_at']


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    description = models.TextField(default=None, null=True,
                                   verbose_name='Описание вопросов')
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.description}'

    class Meta:
        verbose_name_plural = 'Тесты'
        verbose_name = 'Тест'
        ordering = ['-pub_date']


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.question_text}'

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'
        ordering = ['-pub_date']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.choice_text}'

    class Meta:
        verbose_name_plural = 'Варианты ответа'
        verbose_name = 'Вариант ответа'
        ordering = ['-question']
