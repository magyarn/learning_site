from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

# Create your tests here.
from .models import Course, Text, Quiz

class CourseModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="My Great Course",
            description="It's the best"
        )

    def test_course_creation(self):
        now = timezone.now()
        self.assertLess(self.course.created_at, now)

class CourseViewTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="My Great Course",
            description="It's the best",
        )
        self.course2 = Course.objects.create(
            title="My Second Great Course",
            description="It's also pretty good",
        )
        self.text = Text.objects.create(
            title="Baby Step",
            description="It's so small and cute",
            course=self.course,
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail',
                                       kwargs={'course_pk':self.course.pk}
                                       ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])
        self.assertTemplateUsed(resp, 'courses/course_detail.html')
        self.assertContains(resp, self.course.title)

class StepModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="My Great Course",
            description="Blah blah blah"
        )
        self.step = Step.objects.create(
            title="The First Step",
            description="It's a big one",
            content="This is the content",
            order=0,
            course=self.course
        )

    def test_step_course_association(self):
        self.assertIn(self.step, self.course.step_set.all())

class StepViewTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="My Great Course",
            description="Blah blah blah"
        )
        self.step = Step.objects.create(
            title="The First Step",
            description="It's a big one",
            content="This is the content",
            order=0,
            course=self.course
        )

    def test_text_detail_view(self):
        resp = self.client.get(reverse('courses:text_detail', kwargs={
                                        'course_pk': self.course.pk,
                                        'step_pk': self.step.pk
                                        }
                                ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])
        self.assertTemplateUsed(resp, 'courses/text_detail.html')
        self.assertContains(resp, self.step.title)
