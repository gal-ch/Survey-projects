from django.contrib import admin

from .models import Question, Answer


class AnswerTabularInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerTabularInline]
    class Meta:
        __module__ = Question


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)