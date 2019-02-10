from itertools import chain

from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    View,
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.views.generic.base import TemplateView

from rest_framework import generics

from . import models
from . import forms
from . import mixins
from . import serializers

# def course_list(request):
#     courses = models.Course.objects.filter(published=True)
#     return render(request, 'courses/course_list.html', {'courses': courses})

class HomeView(TemplateView):

    template_name = "courses/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_courses'] = models.Course.objects.all()[:5]
        return context


class ListCreateCourse(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

class ListCreateReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return self.queryset.filter(course_id=self.kwargs.get('course_pk'))
    
    def perform_create(self, serializer):
        course = get_object_or_404(
            models.Course, pk=self.kwargs.get('course_pk')
        )
        serializer.save(course=course)

class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            course_id=self.kwargs.get('course_pk'),
            pk=self.kwargs.get('pk')
        )

class CourseListView(ListView):
    queryset = models.Course.objects.filter(published=True)
    context_object_name = 'courses'

class MyCoursesListView(ListView):
    context_object_name = 'courses'
    template_name = 'courses/my_courses.html'

    def get_queryset(self):
        return models.Course.objects.filter(teacher=self.request.user)

# def course_detail(request, course_pk):
#     course = get_object_or_404(models.Course, pk=course_pk, published=True)
#     steps = sorted(chain(course.text_set.all(), course.quiz_set.all()),
#             key= lambda step: step.order)
#     return render(request, 'courses/course_detail.html', {
#             'course': course,
#             'steps': steps
#         })

class CourseDetailView(DetailView):
    model = models.Course
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(models.Course, pk=self.kwargs.get("pk"))
        context["steps"] = sorted(chain(course.text_set.all(), course.quiz_set.all()),
                key= lambda step: step.order)
        return context

@method_decorator(login_required, name='dispatch')
class CourseCreateView(mixins.PageTitleMixin, CreateView):
    page_title = "Create a new course"
    model = models.Course
    fields = ("title", "description", "teacher", "subject", "status",)

    def get_initial(self):
        initial = super().get_initial()
        initial['teacher'] = self.request.user
        return initial

# def course_create(request):
#     form = forms.CourseForm()
#
#     if request.method == 'POST':
#         form = forms.CourseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('courses:list')
#     return render(request, 'courses/course_form.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CourseEditView(mixins.PageTitleMixin, UpdateView):
    model = models.Course
    fields = ("title", "description", "teacher", "subject", "status",)

    def get_page_title(self):
        obj = self.get_object()
        return "Edit {}".format(obj.title)

# @login_required
# def course_edit(request, pk):
#     course = get_object_or_404(models.Course, pk=pk)
#     steps = sorted(chain(course.text_set.all(), course.quiz_set.all()),
#             key= lambda step: step.order)
#     form = forms.CourseForm(instance=course)
#
#     if request.method == 'POST':
#         form = forms.CourseForm(instance=course, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('courses:detail', pk=pk)
#     return render(request, 'courses/course_form.html', {
#         'form': form
#     })

class CourseDeleteView(DeleteView):
    model = models.Course
    success_url = reverse_lazy("courses:list")

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(teacher=self.request.user)
        return self.model.objects.all()

class TextDetailView(DetailView):
    model = models.Text
    context_object_name = 'step'

# def text_detail(request, course_pk, step_pk):
#     step = get_object_or_404(models.Text, pk=step_pk, course_id=course_pk, course__published=True)
#     return render(request, 'courses/text_detail.html', {'step': step})

class TextCreateView(CreateView):
    model = models.Text
    fields = ('title', 'description', 'content', 'order')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Course` instance exists
        before going any further.
        """
        self.course = get_object_or_404(models.Course, pk=kwargs['course_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(models.Course, pk=self.kwargs.get("course_pk"))
        return context

    def form_valid(self, form):
        """
        Overridden to add the course relation to the `Text` instance.
        """
        form.instance.course = self.course
        return super().form_valid(form)

# @login_required
# def text_create(request, course_pk):
#     course = get_object_or_404(models.Course, pk=course_pk)
#     form = forms.TextForm()
#
#     if request.method == 'POST':
#         form = forms.TextForm(request.POST)
#         if form.is_valid():
#             text = form.save(commit=False)
#             text.course = course
#             text.save()
#             messages.success(request, 'Text step created!')
#             return HttpResponseRedirect(text.get_absolute_url())
#     return render(request, 'courses/text_form.html', {
#         'form': form,
#         'course': course,
#     })

@method_decorator(login_required, name="dispatch")
class TextEditView(UpdateView):
    model = models.Text
    fields = ('title', 'description', 'content', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(models.Course, pk=self.kwargs.get("course_pk"))
        return context

# @login_required
# def text_edit(request, course_pk, step_pk):
#     text = get_object_or_404(models.Text, pk=step_pk, course_id=course_pk, course__published=True)
#     form = forms.TextForm(instance=text)
#
#     if request.method == 'POST':
#         form = forms.TextForm(instance=text, data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, '{} updated!'.format(form.cleaned_data['title']))
#             return HttpResponseRedirect(text.get_absolute_url())
#     return render(request, 'courses/text_form.html', {
#         'form': form,
#         'course': text.course
#         })

class TextDeleteView(DeleteView):
    model = models.Text
    context_object_name = 'step'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(models.Course, pk=self.kwargs.get("course_pk"))
        return context

    def get_success_url(self):
        course = self.object.course
        return reverse_lazy("courses:detail", kwargs={'pk': course.pk})

# @login_required
# def text_delete(request, course_pk, step_pk):
#     text = get_object_or_404(models.Text, pk=step_pk, course_id=course_pk)
#     text.delete()
#     messages.success(request, "Text step deleted")
#     return redirect('courses:detail', course_pk=course_pk)


def quiz_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Quiz, pk=step_pk, course_id=course_pk, course__published=True)
    return render(request, 'courses/quiz_detail.html', {'step': step})

@login_required
def quiz_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.QuizForm()

    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.add_message(request, messages.SUCCESS,
                                'Quiz added!')
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': course})

@login_required
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk, course_id=course_pk, course__published=True)
    form = forms.QuizForm(instance=quiz)

    if request.method == 'POST':
        form = forms.QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form, 'course':quiz.course})

def suggestion_view(request):
    form = forms.SuggestionForm()
    if request.method=="POST":
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            send_mail(
                'Suggestion from {}'.format(form.cleaned_data['name']),
                form.cleaned_data['suggestion'],
                '{name} <{email}>'.format(**form.cleaned_data),
                ['magyarn@umich.edu']
            )
            messages.add_message(request, messages.SUCCESS,
                                'Thanks for your suggestion!')
            return HttpResponseRedirect(reverse('courses:suggestion_form'))
    return render(request, 'courses/suggestion_form.html', {'form': form})

@login_required
def question_create(request, quiz_pk, question_type):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)
    if question_type == 'tf':
        form_class = forms.TrueFalseQuestionForm
    else:
        form_class = forms.MultipleChoiceQuestionForm

    form = form_class()
    answer_forms = forms.AnswerInlineFormSet(
        # Returns a blank query set, since this is a new question
        queryset=models.Answer.objects.none()
    )

    if request.method == 'POST':
        form = form_class(request.POST)
        answer_forms = forms.AnswerInlineFormSet(
            request.POST,
            queryset=models.Answer.objects.none()
        )
        if form.is_valid() and answer_forms.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Added question!")
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/question_form.html', {
        'quiz': quiz,
        'form': form,
        'formset': answer_forms
    })

@login_required
def question_edit(request, quiz_pk, question_pk):
    question = get_object_or_404(models.Question,
                                pk=question_pk, quiz_id=quiz_pk)
    if hasattr(question, 'truefalsequestion'):
        form_class = forms.TrueFalseQuestionForm
        question = question.truefalsequestion
    else:
        form_class = forms.MultipleChoiceQuestionForm
        question = question.multiplechoicequestion

    form = form_class(instance=question)
    answer_forms = forms.AnswerInlineFormSet(
        queryset=form.instance.answer_set.all()
    )

    if request.method == 'POST':
        form = form_class(instance=question, data=request.POST)
        answer_forms = forms.AnswerInlineFormSet(
            request.POST,
            queryset=form.instance.answer_set.all()
        )
        if form.is_valid() and answer_forms.is_valid():
            form.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Updated question!")
            return HttpResponseRedirect(question.quiz.get_absolute_url())
    return render(request, 'courses/question_form.html', {
        'form': form,
        'formset': answer_forms
    })

@login_required
def answer_create(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)
    formset = forms.AnswerFormSet(queryset=question.answer_set.all())

    if request.method == 'POST':
        formset = forms.AnswerFormSet(request.POST,
                                    queryset=question.answer_set.all())
        if formset.is_valid():
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Answers added!")
            return HttpResponseRedirect(question.get_absolute_url())
    return render(request, 'courses/answer_form.html', {
            'question': question,
            'formset': formset
        })

def courses_by_teacher(request, teacher):
    courses = models.Course.objects.filter(teacher__username=teacher, published=True)
    return render(request, 'courses/course_list.html', {'courses': courses})

def search_results(request):
    term = request.GET.get('q')
    courses = models.Course.objects.filter(title__icontains=term, published=True)
    return render(request, 'courses/course_list.html', {'courses': courses})
