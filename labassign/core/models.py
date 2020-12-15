from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):
    MAX_LENGTH = 128
    first_name = models.CharField(max_length=MAX_LENGTH)
    last_name = models.CharField(max_length=MAX_LENGTH)

    def save(self, *args, **kwargs):
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['last_name', 'first_name']


class LabGroup(models.Model):
    LGROUP_MAX_LENGTH = 128
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groupName = models.CharField(max_length=LGROUP_MAX_LENGTH)
    language = models.CharField(max_length=LGROUP_MAX_LENGTH)
    schedule = models.CharField(max_length=LGROUP_MAX_LENGTH)
    maxNumberStudents = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(LabGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.groupName

    class Meta:
        ordering = ['groupName']


class TheoryGroup(models.Model):
    TGROUP_MAX_LENGTH = 128
    groupName = models.CharField(max_length=TGROUP_MAX_LENGTH)
    language = models.CharField(max_length=TGROUP_MAX_LENGTH)

    def save(self, *args, **kwargs):
        super(TheoryGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.groupName

    class Meta:
        ordering = ['groupName']


class Student(User):
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE, null=True)
    theoryGroup = models.ForeignKey(
        TheoryGroup, on_delete=models.CASCADE, null=True)
    # first_name = models.CharField()
    # last_name = models.CharField()
    # password = models.CharField()
    # username = models.CharField()
    gradeTheoryLastYear = models.FloatField(default=0.0, null=True)
    gradeLabLastYear = models.FloatField(default=0.0, null=True)
    convalidationGranted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.last_name + ", " + self.first_name

    class Meta:
        ordering = ['last_name', 'first_name']


class Pair(models.Model):
    student1 = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name="student1_id")
    student2 = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name="student2_id")
    validated = models.BooleanField(default=False)
    studentBreakRequest = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        super(Pair, self).save(*args, **kwargs)

    def __str__(self):
        return self.student1.first_name + ' ' + self.student2.first_name


class GroupConstraints(models.Model):
    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(GroupConstraints, self).save(*args, **kwargs)

    def __str__(self):
        return self.theoryGroup.groupName + " " + self.labGroup.groupName

    class Meta:
        ordering = ['labGroup', 'theoryGroup']


class OtherConstraints(models.Model):
    selectGroupStartDate = models.DateField()
    minGradeTheoryConv = models.FloatField(default=0.0)
    minGradeLabConv = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        super(OtherConstraints, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.minGradeLabConv) + " " + str(self.minGradeTheoryConv)
