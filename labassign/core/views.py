from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from core.models import Student, Pair, OtherConstraints
from core.forms import GroupForm, PairForm, BreakPairForm

"""
author: Belen Vivas Garcia
"""


def home(request):
    # If a user has logged in
    if request.user.is_authenticated:
        # Creating the context dict
        context_dict = {}
        # We get the info for the logged student
        st = Student.objects.get(id=request.user.id)
        context_dict['name'] = st.first_name + " " + st.last_name
        context_dict['val_status'] = st.convalidationGranted
        context_dict['labGroup'] = st.labGroup
        context_dict['pairs'] = Pair.objects.filter(student1=st)
        return render(request, 'core/home.html', context_dict)
    # Render in case no student has logged in
    else:
        return render(request, 'core/home.html')


"""
author: Belen Vivas Garcia
"""


def login_service(request):
    # If a user has already logged in, return an error.
    if request.user.is_authenticated:
        return render(request, 'core/login.html',
                      {'errormsg': "You are already logged in."})
    else:
        # Check if the data has been posted
        if request.method == 'POST':
            # Fetch form values
            uname = request.POST.get('username')
            passwd = request.POST.get('password')
            # We authenticate the user (in case it exists)
            user = authenticate(username=uname, password=passwd)
            # If the user is valid
            if user:
                # Log in the user
                login(request, user)
                return redirect(reverse('core:home'))
            else:
                context_dict = {}
                context_dict['errormsg'] = "Invalid credentials."
                return render(request, 'core/login.html', context_dict)
        else:
            return render(request, 'core/login.html')


"""
author: Andrea Olcina Jimenez
"""


@login_required
def logout_service(request):
    # Use the django logout function to delete all the session data
    logout(request)
    return redirect(reverse('core:home'))


"""
author: Andrea Olcina Jimenez
"""


@login_required
def pair(request):
    # We create a new form for the second member of the pair
    pairform = PairForm(userid=request.user.id)
    # Fecth logged student
    user1 = Student.objects.get(id=request.user.id)
    # IF USER HAS ALREADY SELECTED A PAIR, WE HAVE TO RENDER AN ERROR
    canApply = True
    if Pair.objects.filter(student1=user1).exists():
        canApply = False
        return render(request, 'core/pair.html', {'canApply': canApply})
    # If an student has been posted
    if request.method == 'POST':
        # Recover data
        pairform = PairForm(userid=request.user.id, data=request.POST)
        if pairform.is_valid():
            # Get the value posted
            user2 = pairform.cleaned_data['secondMemberGroup']
            # If the correspondant pair exists
            if Pair.objects.filter(student1=user2, student2=user1).exists():
                # We fetch the correspondant pair and
                # set validated to True in both
                pair = Pair.objects.get(student1=user2, student2=user1)
                pair.validated = True
                pair.save()
                return redirect(reverse('core:home'))
            else:
                # We create (or fetch) the pair just requested
                newpair = Pair.objects.get_or_create(
                    student1=user1, student2=user2)[0]
                newpair.save()
                # The pair is already created and
                # set to false then we just return home
                return redirect(reverse('core:home'))
    return render(request, 'core/pair.html',
                  {'form': pairform, 'canApply': canApply})


"""
author: Andrea Olcina Jimenez
"""


def convalidate(request):
    if request.user.is_authenticated:
        # If the user is not authenticated we can simply render the page
        # We check if the form has been posted
        # We get the logged students since its going
        # to be used in the inital rendering and the form
        st = Student.objects.get(id=request.user.id)

        # Fetch grades
        thGrade = st.gradeTheoryLastYear
        labGrade = st.gradeLabLastYear
        const = OtherConstraints.objects.all()[0]
        satisfy = False
        canRequest = True  # This var is used to determine whether
        # the user can request convalidation or not

        # Check if the constraints are satisfied
        if (thGrade > const.minGradeTheoryConv) \
                and (labGrade > const.minGradeLabConv):
            satisfy = True

        context_dict = {}
        context_dict['thGrade'] = thGrade
        context_dict['labGrade'] = labGrade
        context_dict['status'] = st.convalidationGranted

        # are the first member of a pair
        if Pair.objects.filter(student1=st).exists():
            canRequest = False
            context_dict['message'] = "You are the first member of a pair."

        # No validation request will be accepted from users which:
        # are part of a validated pair
        if Pair.objects.filter(student2=st, validated=True).exists():
            canRequest = False
            context_dict['message'] = "You belong to a validated pair."
        # have already select a laboratory group.
        if st.labGroup is not None:
            canRequest = False
            context_dict['message'] = "You have " \
                                      "already selected a laboratory group."
        # have al ready requested convalidation
        if st.convalidationGranted is True:
            canRequest = False
            context_dict['message'] = "You have " \
                                      "already been granted convalidation."
        context_dict['canRequest'] = canRequest
        context_dict['satisfy'] = satisfy
        # Check if the grades satisfy the minimum constraints
        if satisfy is True and canRequest is True:
            # The convalidation is granted
            st.convalidationGranted = True
            st.save()
        return render(request, 'core/convalidation.html', context_dict)
    else:
        return redirect(reverse('core:login'))


"""
author: Belen Vivas Garcia
"""


def group(request):
    if request.user.is_authenticated:
        otherConst = OtherConstraints.objects.all()[0]
        st = Student.objects.get(id=request.user.id)
        if st.labGroup is not None:
            return render(request, 'core/group.html',
                          {'errormsg': "You have already selected a group."})
        if date.today() >= otherConst.selectGroupStartDate:
            form = GroupForm(userid=request.user.id)
            if request.method == 'POST':
                form = GroupForm(userid=request.user.id, data=request.POST)
                if form.is_valid():
                    lGroup = form.cleaned_data['myLabGroup']
                    lGroup.counter += 1
                    lGroup.save()
                    st.labGroup = lGroup
                    st.save()
                    pairs = Pair.objects.filter(validated=True)
                    for p in pairs:
                        if p.student1 == st:
                            st2 = p.student2
                            lGroup.counter += 1
                            lGroup.save()
                            st2.labGroup = lGroup
                            st2.save()
                            return redirect(reverse('core:home'))
                        if p.student2 == st:
                            st2 = p.student1
                            lGroup.counter += 1
                            lGroup.save()
                            st2.labGroup = lGroup
                            st2.save()
                            return redirect(reverse('core:home'))
                else:
                    return redirect(reverse('core:home'))
            return render(request, 'core/group.html', {'form': form})
        else:
            return render(request, 'core/group.html',
                          {'errormsg': "Group selection is not active."})
    else:
        return redirect(reverse('core:login'))


"""
author: Andrea Olcina Jiménez
"""


def breakpair(request):
    if request.user.is_authenticated:
        # Fetch the student logged in
        st = Student.objects.get(id=request.user.id)
        # Create the break pair form
        form = BreakPairForm(userid=request.user.id)
        # If data has been posted --> recover chosen pair
        if request.method == 'POST':
            form = BreakPairForm(userid=request.user.id, data=request.POST)
            if form.is_valid():
                pair = form.cleaned_data['myPair']
                st1 = pair.student1
                st2 = pair.student2
                # If members of the pair have
                # already selected a group --> not valid
                if (st1.labGroup is not None or st2.labGroup is not None):
                    return render(request,
                                  'core/breakpair.html',
                                  {'errormsg': 'Could not process '
                                               'your request.'})
                # If the pair hasnt been yet validated
                if (pair.validated is False):
                    pair.delete()
                    return redirect(reverse('core:home'))
                # otherwise
                else:
                    # Request not null
                    if (pair.studentBreakRequest is not None):
                        pair.delete()
                    # otherwise
                    else:
                        pair.studentBreakRequest = st
                        pair.save()
                return redirect(reverse('core:home'))
            else:
                return render(request,
                              'core/breakpair.html',
                              {'errormsg': 'Could not process '
                                           'your request.'})
        else:
            return render(request, 'core/breakpair.html', {'form': form})
    else:
        return redirect(reverse('core:login'))


"""
author: Belen Vivas Garcia
"""


def convalidate_help(request):
    return render(request, 'core/convalidationhelp.html')


"""
author: Belen Vivas Garcia
"""


def group_help(request):
    return render(request, 'core/grouphelp.html')


"""
author: Belen Vivas Garcia
"""


def login_help(request):
    return render(request, 'core/loginhelp.html')


"""
author: Belen Vivas Garcia
"""


def pair_help(request):
    return render(request, 'core/pairhelp.html')
