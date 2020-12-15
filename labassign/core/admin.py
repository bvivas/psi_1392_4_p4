from django.contrib import admin
from core.models import Teacher, Student, LabGroup, \
    TheoryGroup, Pair, GroupConstraints, OtherConstraints

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(LabGroup)
admin.site.register(TheoryGroup)
admin.site.register(Pair)
admin.site.register(GroupConstraints)
admin.site.register(OtherConstraints)
