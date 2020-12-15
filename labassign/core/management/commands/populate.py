# Populate database
# This file has to be placed within the
# core/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate
import django

django.setup()

import csv
import collections
from django.core.management.base import BaseCommand
from core.models import OtherConstraints, Pair, Student, \
    GroupConstraints, TheoryGroup, LabGroup, Teacher
from datetime import date, timedelta


# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
#
# Teachers, groups and constraints
# will be hardcoded in this file.
# Students will be read from a cvs file
# last year grade will be obtained from another cvs file
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate database
           """

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help="""
        model to  update:
        all -> all models
        teacher
        labgroup
        theorygroup
        groupconstraints
        otherconstrains
        student (require csv file)
        studentgrade (require different csv file,
        update only existing students)
        pair
        """)
        parser.add_argument('studentinfo', type=str, help="""CSV file with student information
        header= NIE, DNI, Apellidos, Nombre, Teoría
        if NIE or DNI == 0 skip this entry and print a warning""")
        parser.add_argument('studentinfolastyear', type=str, help="""CSV file with student information
        header= NIE,DNI,Apellidos,Nombre,Teoría, grade lab, grade the
        if NIE or DNI == 0 skip this entry and print a warning""")

    # handle is another compulsory name, do not change it"
    def handle(self, *args, **kwargs):
        model = kwargs['model']
        cvsStudentFile = kwargs['studentinfo']
        cvsStudentFileGrades = kwargs['studentinfolastyear']
        # clean database
        if model == 'all':
            self.cleanDataBase()
        if model == 'teacher' or model == 'all':
            self.teacher()
        if model == 'labgroup' or model == 'all':
            self.labgroup()
        if model == 'theorygroup' or model == 'all':
            self.theorygroup()
        if model == 'groupconstraints' or model == 'all':
            self.groupconstraints()
        if model == 'otherconstrains' or model == 'all':
            self.otherconstrains()
        if model == 'student' or model == 'all':
            self.student(cvsStudentFile)
        if model == 'studentgrade' or model == 'all':
            self.studentgrade(cvsStudentFileGrades)
        if model == 'pair' or model == 'all':
            self.pair()

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        # remove pass and ADD CODE HERE
        Teacher.objects.all().delete()
        LabGroup.objects.all().delete()
        TheoryGroup.objects.all().delete()
        GroupConstraints.objects.all().delete()
        Pair.objects.all().delete()
        Student.objects.all().delete()
        OtherConstraints.objects.all().delete()

    def teacher(self):
        # "create teachers here"
        # remove pass and ADD CODE HERE
        # create dictionary with teacher data
        teacherD = {}
        teacherD[1] = {'id': 1,  # 1261, L 18:00, 1271 X 18-20
                       'first_name': 'No',
                       'last_name': 'Asignado1'}
        teacherD[2] = {'id': 2,  # 1262 X 18-20, 1263/1273 V 17-19
                       'first_name': 'No',
                       'last_name': 'Asignado4'}
        teacherD[3] = {'id': 3,  # 1272 V 17-19, 1291 L 18-20
                       'first_name': 'Julia',
                       'last_name': 'Diaz Garcia'}
        teacherD[4] = {'id': 4,  # 1292/1251V 17:00
                       'first_name': 'Alvaro',
                       'last_name': 'del Val Latorre'}
        teacherD[5] = {'id': 5,  # 1201 X 18:00
                       'first_name': 'Roberto',
                       'last_name': 'Marabini Ruiz'}

        for tch in teacherD:
            teacher = Teacher.objects.get_or_create(id=teacherD[tch]['id'],
                                                    first_name=teacherD[tch]
                                                    ['first_name'],
                                                    last_name=teacherD[tch]
                                                    ['last_name'])[0]
            teacher.save()

    def labgroup(self):
        # "add labgroups"
        # remove pass and ADD CODE HERE
        labgroupD = {}
        maxNumberStudents = 23
        # create dictionary with teacher data
        labgroupD[1261] = {'id': 1261,  # 1261, L 18:00, 1271 X 18-20
                           'groupName': '1261',
                           'teacher': 1,
                           'schedule': 'Lunes/Monday 18-20',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1262] = {'id': 1262,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 2,
                           'groupName': '1262',
                           'schedule': 'Miércoles/Wednesday 18-20',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1263] = {'id': 1263,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 2,
                           'groupName': '1263',
                           'schedule': 'Viernes/Friday 17-19',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1271] = {'id': 1271,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 1,
                           'groupName': '1271',
                           'schedule': 'Miércoles/Wednesday 18-20',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1272] = {'id': 1272,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 3,
                           'groupName': '1272',
                           'schedule': 'Viernes/Friday 17-19',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1291] = {'id': 1291,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 3,
                           'groupName': '1291',
                           'schedule': 'Lunes/Monday 18-20',
                           'language': 'inglés/English',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1292] = {'id': 1292,
                           'teacher': 4,
                           'groupName': '1292',
                           'schedule': 'Viernes/Friday 17-19',
                           'language': 'inglés/English',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1201] = {'id': 1201,
                           'teacher': 5,
                           'groupName': '1201',
                           'schedule': 'Miércoles/Wednesday 18-20',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}

        for group in labgroupD:
            t = Teacher.objects.get(id=labgroupD[group]['teacher'])
            labGroup = LabGroup.objects.get_or_create(
                id=labgroupD[group]['id'], teacher=t,
                groupName=labgroupD[group]['groupName'])[0]
            labGroup.language = labgroupD[group]['language']
            labGroup.schedule = labgroupD[group]['schedule']
            labGroup.maxNumberStudents = labgroupD[group]['maxNumberStudents']
            labGroup.save()

    def theorygroup(self):
        # "add theorygroups"
        # remove pass and ADD CODE HERE
        theorygroupD = {}
        theorygroupD[126] = {'id': 126,
                             'groupName': '126',
                             'language': 'español/Spanish', }
        theorygroupD[127] = {'id': 127,  # 127/120
                             'groupName': '127',
                             'language': 'español/Spanish', }
        theorygroupD[129] = {'id': 129,  # 129/125
                             'groupName': '129',
                             'language': 'inglés/English', }
        theorygroupD[120] = {'id': 120,  # 127/120
                             'groupName': '120',
                             'language': 'español/Spanish', }
        theorygroupD[125] = {'id': 125,  # 129/125
                             'groupName': '125',
                             'language': 'inglés/English', }
        for group in theorygroupD:
            # save_thGroup(group['id'], group['teacher'],
            # group['groupName'], group['language'])
            theorygroup = TheoryGroup.objects.get_or_create(
                id=theorygroupD[group]['id'],
                groupName=theorygroupD[group]['groupName'])[0]
            theorygroup.language = theorygroupD[group]['language']
            theorygroup.save()

    def groupconstraints(self):
        # "add group constrints"
        # remove pass and ADD CODE HERE
        groupconstraintsD = {}
        groupconstraintsD[1261] = {'theoryGroup': 126,
                                   'labGroup': 1261}  # mañana
        groupconstraintsD[1262] = {'theoryGroup': 126,
                                   'labGroup': 1262}  # mañana
        groupconstraintsD[1263] = {'theoryGroup': 126,
                                   'labGroup': 1263}  # mañana
        # tarde, split ii and doble
        groupconstraintsD[1271] = {'theoryGroup': 127,
                                   'labGroup': 1271}  # tarde - no doble
        groupconstraintsD[1272] = {'theoryGroup': 127,
                                   'labGroup': 1272}  # tarde - no doble
        groupconstraintsD[1201] = {'theoryGroup': 120,
                                   'labGroup': 1201}
        # doble - tarde - español - WEds
        # english
        groupconstraintsD[1291] = {'theoryGroup': 129,
                                   'labGroup': 1291}
        # inglés - ii - tarde Friday
        groupconstraintsD[1292] = {'theoryGroup': 125,
                                   'labGroup': 1292}  # inglés - doble
        # groupconstraintsD[1202] =
        # {'theoryGroup' : 120, 'labGroup': 1202}
        # doble - tarde - 2nd group

        for groupcons in groupconstraintsD:
            thGroup = TheoryGroup.objects.get(
                id=groupconstraintsD[groupcons]['theoryGroup'])
            lGroup = LabGroup.objects.get(
                id=groupconstraintsD[groupcons]['labGroup'])
            gconst = GroupConstraints.objects.get_or_create(
                theoryGroup=thGroup, labGroup=lGroup)[0]
            gconst.save()

    def pair(self):
        # "create a few valid pairs"
        # remove pass and ADD CODE HERE
        pairD = collections.OrderedDict()
        # Mañana
        pairD[1000] = {'student2': 1100, 'validated': False}
        pairD[1001] = {'student2': 1101, 'validated': False}
        pairD[1010] = {'student2': 1110, 'validated': True}
        pairD[1011] = {'student2': 1111, 'validated': True}
        pairD[1012] = {'student2': 1112, 'validated': True}

        for pair in pairD:
            st1 = Student.objects.get(id=pair)
            st2 = Student.objects.get(id=pairD[pair]['student2'])
            pair = Pair.objects.get_or_create(
                student1=st1, student2=st2,
                validated=pairD[pair]['validated'])[0]
            pair.save()

    def otherconstrains(self):
        """create a single object here with staarting dates
        and maximum and minimum convalidation grades"""
        """ Use the following values:
        selectGroupStartDate = now + 1 day,
        minGradeTheoryConv = 3,
        minGradeLabConv = 7
        """
        # remove pass and ADD CODE HERE
        othConst = OtherConstraints.objects.get_or_create(
            selectGroupStartDate=date.today() + timedelta(days=1),
            minGradeTheoryConv=3.0, minGradeLabConv=7.0)[0]
        othConst.save()

    def student(self, csvStudentFile):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría
        # remove pass and ADD CODE HERE
        actual_id = 1000
        with open(csvStudentFile, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_row = 0
            for row in csv_reader:
                if line_row != 0:
                    txt = row[0]
                    txt = txt.replace('"', '')
                    row_split = txt.split(",")
                    thGroup = TheoryGroup.objects.get(id=row_split[4])
                    st = Student.objects.create_user(
                        id=actual_id, username=row_split[0],
                        password=row_split[1], first_name=row_split[3],
                        last_name=row_split[2], theoryGroup=thGroup)
                    actual_id += 1
                    st.save()
                line_row += 1

    def studentgrade(self, cvsStudentFileGrades):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría
        # grade-practicas	gradeteoria
        # remove pass and ADD CODE HERE
        with open(cvsStudentFileGrades, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_row = 0
            for row in csv_reader:
                if line_row != 0:
                    txt = row[0]
                    txt = txt.replace('"', '')
                    row_split = txt.split(",")
                    st = Student.objects.get(username=row_split[0])
                    st.gradeTheoryLastYear = row_split[6]
                    st.gradeLabLastYear = row_split[5]
                    st.save()
                line_row += 1
