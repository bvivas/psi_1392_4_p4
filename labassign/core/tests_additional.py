from core.tests_services import ServiceBaseTest
from core.tests_services import LOGIN_SERVICE, CONVALIDATION_SERVICE, \
    CONVALIDATION_HELP_SERVICE, GROUP_HELP_SERVICE, PAIR_HELP_SERVICE, \
    FIRST_STUDENT_ID, GROUP_SERVICE, GROUP_FORM_LABEL, LOGIN_HELP_SERVICE
from django.urls import reverse
from django.utils import timezone
from core.models import (Student, OtherConstraints,
                         Pair, TheoryGroup, GroupConstraints,
                         LabGroup)
import datetime

USERNAME_NV = "testUser_5"
PASSWORD_NV = "pass5"
FIRST_NAME_NV = "user5"
LAST_NAME_NV = "name5"


class LogInServiceAdditionalTests(ServiceBaseTest):
    def test06_login_already(self):
        # Log in user
        self.loginTestUser(self.client1, self.user1)
        # Try to log in with another user
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.paramsUser2,
                                     follow=True)
        # Message found
        self.assertFalse(self.decode(response.content).
                         find("You are already logged in.") == -1)

    def test07_login_invalid(self):
        # Create invalid credentials
        self.paramsUserInvalid = {"username": USERNAME_NV,
                                  "password": PASSWORD_NV,
                                  "first_name": FIRST_NAME_NV,
                                  "last_name": LAST_NAME_NV,
                                  "id": FIRST_STUDENT_ID + 6}
        # Log in with invalid credentials
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.paramsUserInvalid,
                                     follow=True)
        # Message found
        self.assertFalse(self.decode(response.content).
                         find("Invalid credentials.") == -1)


class ConvalidationServiceAdditionalTests(ServiceBaseTest):
    def test15_user_withgroup(self):
        # Log in user
        self.loginTestUser(self.client1, self.user1)
        # The user has already selected a lab group
        # so it doesn't satisfy the requirements
        o = GroupConstraints.objects.all().first()
        self.user1.theoryGroup = o.theoryGroup
        self.user1.labGroup = o.labGroup
        self.user1.save()
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        # convalidation test
        self.assertFalse(self.decode(response.content).
                         find("You have already selected"
                              " a laboratory group.") == -1)

    def test16_user_convalidated(self):
        # Log in user
        self.loginTestUser(self.client1, self.user1)
        # The user is already convalidated
        self.user1.convalidationGranted = True
        self.user1.save()
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)

        # convalidation test
        self.assertFalse(self.decode(response.content).
                         find("You have already been "
                              "granted convalidation.") == -1)


class GroupServiceAdditionalTests(ServiceBaseTest):
    def test45_group_already(self):
        # Log in user
        self.loginTestUser(self.client1, self.user1)
        # The user has already selected a lab group
        # so it doesn't satisfy the requirements
        o = GroupConstraints.objects.all().first()
        self.user1.theoryGroup = o.theoryGroup
        self.user1.labGroup = o.labGroup
        self.user1.save()
        response = self.client1.get(reverse(GROUP_SERVICE),
                                    follow=True)
        # Group already selected --> fail
        self.assertFalse(self.decode(response.content).
                         find("You have already selected a group.") == -1)

    def test46_group_pair(self):
        # Log in user
        self.loginTestUser(self.client1, self.user1)
        # assign theory group to user
        theoryGroup = TheoryGroup.objects.all().first()
        self.user1.theoryGroup = theoryGroup
        self.user1.save()

        # set othercostraint.selectGroupStart to now
        o = OtherConstraints.objects.all().first()
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        o.selectGroupStartDate = now
        o.save()

        # We create a validated pair
        pair = Pair(student1=self.user1, student2=self.user2, validated=True)
        pair.save()

        # assign maximum number of students and count to labGroup
        labGroup = GroupConstraints.objects.filter(
            theoryGroup=theoryGroup).first().labGroup
        labGroup.counter = 1
        labGroup.maxNumberStudents = 4
        labGroup.save()
        # try to reserve
        labGroupId = labGroup.id
        data = {GROUP_FORM_LABEL: labGroupId}
        self.client1.post(reverse(GROUP_SERVICE),
                          data=data,
                          follow=True)
        # refresh user
        user_1 = Student.objects.get(pk=self.user1.id)
        labGroup = LabGroup.objects.get(pk=labGroup.id)
        self.assertEqual(user_1.labGroup.id, labGroup.id)
        self.assertEqual(labGroup.counter, 3)

        # We check if the group of the pair has been updated
        user_2 = Student.objects.get(pk=self.user2.id)
        self.assertIsNotNone(user_2.labGroup)


class NotLoggedAdditionalTests(ServiceBaseTest):
    def test_convalidation_help(self):
        # Convalidation help test page
        self.client1.get(reverse(CONVALIDATION_HELP_SERVICE),
                         follow=True)

    def test_group_help(self):
        # Group help test page
        self.client1.get(reverse(GROUP_HELP_SERVICE),
                         follow=True)

    def test_login_help(self):
        # Log in help test page
        self.client1.get(reverse(LOGIN_HELP_SERVICE),
                         follow=True)

    def test_pair_help(self):
        # Pair help test page
        self.client1.get(reverse(PAIR_HELP_SERVICE),
                         follow=True)
