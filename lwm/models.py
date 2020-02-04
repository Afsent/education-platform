from django.db import models


class Lessons(models.Model):
    id_lesson = models.IntegerField(primary_key=True)
    id_teacher = models.ForeignKey('Teachers', models.DO_NOTHING,
                                   db_column='id_teacher')
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


class Teachers(models.Model):
    id_teacher = models.IntegerField(primary_key=True)
    id_subject = models.IntegerField()
    name = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'teachers'
