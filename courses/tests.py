from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Course
from .models import Step

class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write regular expressions in Python"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)

class StepModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python testing",
            description="Learn to write tests in python."
        )

    def test_step_creation(self):
        step = Step.objects.create(
            title="A Lovely step title",
            description="Nice step description",
            course=self.course
        )
        self.assertIn(step, self.course.step_set.all())

class CourseViewsTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python testing",
            description="Learn to write tests in Python."
        )
        self.course2 = Course.objects.create(
            title="New Course",
            description="A new course"
        )
        self.step = Step.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in your Docstrings",
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:course',
                                        kwargs={'pk': self.course.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])
        self.assertTemplateUsed(resp, 'courses/course_detail.html')
        self.assertContains(resp, self.course.title)

    def test_step_detail_view(self):
        resp = self.client.get(reverse('courses:step',
                kwargs={'course_pk': self.course.pk,
                        'step_pk': self.step.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])
        self.assertTemplateUsed(resp, 'courses/step_detail.html')
        self.assertContains(resp, self.course.title)
        self.assertContains(resp, self.step.title)
