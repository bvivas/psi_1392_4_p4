import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'labassign.settings')
import django

django.setup()

from core.models import Student, OtherConstraints, Pair
from datetime import date, timedelta


def test_query():
    # checks if a user (Student) with id=1000 exists
    user_1000 = Student.objects.get(id=1000)
    # checks if a user with id=1001 exists
    user_1001 = Student.objects.get(id=1001)
    # creates a pair (Pair) using as student1 and student2 users user 1000 and
    # user 1001
    # Persist the result in the database
    new_pair = Pair.objects.get_or_create(student1=user_1000,
                                          student2=user_1001)[0]
    new_pair.save()
    # searches for all the pairs (Pair) where user 1000
    # appears as student1.
    result_pairs = Pair.objects.all().filter(student1=user_1000)
    # modifies the value of validate in the pairs
    # resulting from the previous search
    # so that it is set to True
    for pair in result_pairs:
        pair.validated = True
        pair.save()
    # creates an object of type OtherConstraints
    othCons = OtherConstraints.objects.get_or_create(
        selectGroupStartDate=date.today() + timedelta(days=1))[0]
    print(othCons)
    # performs a search that returns all the objects of type OtherConstraints
    allOther = OtherConstraints.objects.all()
    if allOther[0].selectGroupStartDate > date.today():
        print("selectGroupStartDate is in the future.")
    else:
        print("selectGroupStartDate is in the past.")


# Start execution here!
if __name__ == '__main__':
    print('Starting Core test_query script')
    test_query()
