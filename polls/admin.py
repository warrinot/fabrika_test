from django.contrib import admin
from .models import UserChoice, Poll, Question, Choice


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(UserChoice)


class ChoiceInline(admin.StackedInline):
    model = Choice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['poll', 'text', 'question_type']
    inlines = [ChoiceInline]
