from django import forms
from core.models import LabGroup, Student, Pair, GroupConstraints


class PairForm(forms.Form):
    secondMemberGroup = forms.ModelChoiceField(
        queryset=Student.objects.all(), label="Select the second")

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('userid', None)
        super(PairForm, self).__init__(*args, **kwargs)
        if user_id:
            # Fetch all students
            students = Student.objects.all()
            # Convert into list
            students = list(students)
            # Logged in student
            user1 = Student.objects.get(id=user_id)

            # Validated pairs
            pairs = Pair.objects.filter(validated=True)
            # If any of the possible students
            # is member of a validated pair --> not valid
            for p in pairs:
                if p.student1 in students:
                    students.remove(p.student1)
                if p.student2 in students:
                    students.remove(p.student2)
            # If the logged user is in the list
            if user1 in students:
                students.remove(user1)

            ids = []

            for st in students:
                ids.append(st.id)

            qset = Student.objects.filter(id__in=ids)
            self.fields['secondMemberGroup'].queryset = qset


class GroupForm(forms.Form):
    myLabGroup = forms.ModelChoiceField(
        queryset=None, label="Select the group you want to join to")

    def __init__(self, *args, **kwargs):
        st1_id = kwargs.pop('userid', None)
        super(GroupForm, self).__init__(*args, **kwargs)
        if st1_id:
            # Fetch the logged student
            st1 = Student.objects.get(id=st1_id)
            # Get all group constraints regarding
            # the theory group of the student logged in
            groups = GroupConstraints.objects.filter(
                theoryGroup=st1.theoryGroup)
            myLabGroup = []
            # For each valid lab group, we check if there is enough space
            for group in groups:
                if group.labGroup.counter < group.labGroup.maxNumberStudents:
                    myLabGroup.append(group.labGroup)
            qset = LabGroup.objects.filter(groupName__in=myLabGroup)
            self.fields['myLabGroup'].queryset = qset


class BreakPairForm(forms.Form):
    myPair = forms.ModelChoiceField(queryset=None,
                                    label="Select the pair to be broken")

    def __init__(self, *args, **kwargs):
        st_id = kwargs.pop('userid', None)
        super(BreakPairForm, self).__init__(*args, **kwargs)
        if st_id:
            st1 = Student.objects.get(id=st_id)
            pairs1 = Pair.objects.filter(student1=st1)
            pairs2 = Pair.objects.filter(student2=st1)
            myPair_ids = []
            for pair in pairs1:
                myPair_ids.append(pair.id)
            for pair in pairs2:
                myPair_ids.append(pair.id)
            qset = Pair.objects.filter(id__in=myPair_ids)
            self.fields['myPair'].queryset = qset
