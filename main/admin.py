from django.contrib import admin
from .models import Lessons, Teachers, SubjectGroups, Subjects, AdvUser


@admin.register(AdvUser)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'email')


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_teacher')


@admin.register(Teachers)
class TeachersAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_subject')


@admin.register(SubjectGroups)
class SubjectGroupsAdmin(admin.ModelAdmin):
    list_display = ('id_group_sub', 'name')


@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id_subject', 'id_group_sub', 'name')
