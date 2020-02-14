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
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name='Изображение')
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
    image = models.FileField(upload_to=get_timestamp_path,
                             verbose_name='Файл')

    class Meta:
        verbose_name_plural = 'Дополнительные материалы'
        verbose_name = 'Дополнительная материалы'


class SubjectGroups(models.Model):
    id_group_sub = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'subject_groups'
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


class Subjects(models.Model):
    id_subject = models.AutoField(primary_key=True)
    id_group_sub = models.ForeignKey(SubjectGroups, models.DO_NOTHING,
                                     db_column='id_group_sub')
    name = models.CharField(max_length=45)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'subjects'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Teachers(models.Model):
    id_teacher = models.AutoField(primary_key=True)
    id_subject = models.ForeignKey(Subjects, models.DO_NOTHING,
                                   db_column='id_subject')
    name = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'teachers'
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
