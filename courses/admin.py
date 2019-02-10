from django.contrib import admin
from datetime import date

from . import models

def make_published(modeladmin, request, queryset):
    queryset.update(status='p', published=True)

make_published.short_description = 'Mark selected courses as Published'

def make_in_review(modeladmin, request, queryset):
    queryset.update(status='r', published=False)

make_in_review.short_description = 'Mark selected courses as In Review'

def make_in_progress(modeladmin, request, queryset):
    queryset.update(status='i', published=False)

make_in_progress.short_description = 'Mark selected courses as In Progress'

class AnswerInline(admin.TabularInline):
    model = models.Answer

class YearListFilter(admin.SimpleListFilter):
    title = 'year created'
    #parameter name shows up in the URL
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        if qs.filter(created_at__gte=date(2016, 1, 1),
                      created_at__lte=date(2016, 12, 31)).exists():
            yield ('2016', '2016')
        if qs.filter(created_at__gte=date(2017, 1, 1),
                      created_at__lte=date(2017, 12, 31)).exists():
            yield ('2017', '2017')
        if qs.filter(created_at__gte=date(2018, 1, 1),
                      created_at__lte=date(2018, 12, 31)).exists():
            yield ('2018', '2018')
        if qs.filter(created_at__gte=date(2019, 1, 1),
                      created_at__lte=date(2019, 12, 31)).exists():
            yield ('2019', '2019')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_at__gte=date(int(self.value()), 1, 1),
                                created_at__lte=date(int(self.value()), 12, 31))
        return queryset


class CourseAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']

    list_filter = ['created_at', 'published', 'teacher', YearListFilter]

    list_display = ['title', 'teacher', 'created_at', 'published', 'time_to_complete', 'status']

    list_editable = ['status']

    actions = [make_in_progress, make_in_review, make_published]

    class Media:
        js = ('js/vendor/markdown.js', 'js/preview.js')
        css = {
            'all': ('css/preview.css',),
        }

class QuizAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'description', 'order', 'total_questions']

class AnswerAdmin(admin.ModelAdmin):
    fields = ['question', 'text', 'order']

    list_display = ['text', 'question', 'order']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]

    fields = ['quiz', 'prompt', 'order']

    search_fields = ['prompt']

    list_display = ['prompt', 'quiz', 'order']

    list_editable = ['quiz', 'order']

    # Good for when a model field has a small number of choices only
    # radio_fields = {'quiz': admin.HORIZONTAL}

class TextAdmin(admin.ModelAdmin):
    # fields = ['course', 'title', 'description', 'order', 'content']

    list_display = ['title', 'course', 'order']

    # Customizing the Text detail view
    # Can't have 'fields' (above) and 'fieldsets'
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'order', 'description',)
        }),
        ('Add content', {
            'fields': ('content',),
            'classes': ('collapse',)
        })
    )



admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(models.TrueFalseQuestion, QuestionAdmin)
admin.site.register(models.Review)
admin.site.register(models.Subject)
