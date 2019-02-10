from django import forms
from django.core import validators

from . import models

def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')

class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(help_text='Please verify your email address')
    suggestion = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label="Leave empty",
        # Built-in validator to check for an empty field
        # validators=[validators.MaxLengthValidator(0)]
        # Custom validator for the same thing below:
        validators=[must_be_empty]
        )

    # Less reusable way of validating a single form field:
    # def clean_honeypot(self):
    #     honeypot = self.cleaned_data['honeypot']
    #     if len(honeypot):
    #         raise forms.ValidationError(
    #             'honeypot should be left empty'
    #         )
    #     return honeypot

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        verify = cleaned_data['verify_email']

        if email != verify:
            raise forms.ValidationError(
                "You need to enter the same email in both fields."
            )

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = [
            'title',
            'description',
            'published',
        ]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = [
            'comment',
            'rating',
        ]

class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = [
            'title',
            'description',
            'order',
            'total_questions'
        ]

class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = models.TrueFalseQuestion
        fields = ['prompt', 'order',]

class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = models.MultipleChoiceQuestion
        fields = [
            'prompt',
            'order',
            'shuffle_answers',
            ]
class TextForm(forms.ModelForm):
    class Meta:
        model = models.Text
        fields = [
            'title',
            'description',
            'order',
            'content'
        ]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = [
            'text',
            'correct',
            'order'
        ]

AnswerFormSet = forms.modelformset_factory(
    models.Answer,
    form=AnswerForm,
    extra=2,
)

AnswerInlineFormSet = forms.inlineformset_factory(
    models.Question, #The model the formset appears in
    models.Answer, #The model to be edited in the form
    extra=2,
    fields=('order', 'text', 'correct'), #necessary for the factory
    formset=AnswerFormSet, #optional
    min_num=1,
)
