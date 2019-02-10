from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

import math

STATUS_CHOICES = (
    ('i', 'In Progress'),
    ('r', 'In Review'),
    ('p', 'Published'),
)

# Create your models here.
class Course(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(default='', max_length=100)
    published = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='i')


    def __str__(self):
        return self.title

    def time_to_complete(self):
        from courses.templatetags.course_extras import time_estimate
        return '{} min.'.format(time_estimate(len(self.description.split())))

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={'pk': self.pk})

class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = ['reviewer', 'course']
    
    def __str__(self):
        return '{0.rating} by {0.reviewer} for {0.course}'.format(self)

class Step(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ['order',]

    def __str__(self):
        return self.title

class Text(Step):
    content = models.TextField(blank=True, default='')

    # Using self.course_id requires one less lookup than course.pk
    # get_absolute_url provides a url string to a model instance
    # useful when you have a mixture of different models to display and link to
    def get_absolute_url(self):
        return reverse('courses:text_detail', kwargs={
            'course_pk': self.course_id,
            'pk': self.id
        })

class Quiz(Step):
    total_questions = models.IntegerField(default=4)

    class Meta:
        verbose_name_plural = "Quizzes"


    def get_absolute_url(self):
        return reverse('courses:quiz_detail', kwargs={
            'course_pk': self.course_id,
            'step_pk': self.id
        })

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    prompt = models.TextField()

    class Meta:
        ordering = ['order',]

    # Rather than providing a link to the question, link to the quiz it belongs to
    def get_absolute_url(self):
        return self.quiz.get_absolute_url()

    def __str__(self):
        return self.prompt

class MultipleChoiceQuestion(Question):
    # Foreign key back to the Question model isn't necessary because of multi-table inheritance
    # This model inherits from Question, which isn't abstract. A table exists for Questions
    # and for MultipleChoiceQuestions.
    shuffle_answers = models.BooleanField(default=False)

class TrueFalseQuestion(Question):
    pass

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['order',]

    def __str__(self):
        return self.text
