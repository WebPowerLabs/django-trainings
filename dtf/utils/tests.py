from django_nose.testcases import FastFixtureTestCase


class TestCaseBase(FastFixtureTestCase):
    def assertEqualQs(self, first, second, ordered=False):
        first = list(first)
        second = list(second)
        if not ordered:
            first = sorted(first, key=lambda obj: obj.pk)
            second = sorted(second, key=lambda obj: obj.pk)
        self.assertEqual(first, second)
