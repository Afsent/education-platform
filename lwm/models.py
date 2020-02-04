from django.db import models


class Lessons(models.Model):
    id_lesson = models.AutoField(primary_key=True)
    id_teacher = models.ForeignKey('Teachers', models.DO_NOTHING,
                                   db_column='id_teacher')
    id_subject = models.ForeignKey('Subjects', models.DO_NOTHING,
                                   db_column='id_subject')
    name = models.CharField(max_length=80)
    video = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'lessons'


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
