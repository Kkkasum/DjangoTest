from django.contrib import admin

from .models import Poll, Question, Choice, Answer


class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'users_count')


class ChoiceInline(admin.TabularInline):
    model = Choice
    verbose_name_plural = 'Варианты для вопроса'
    fk_name = 'question'
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'poll', 'users_answered_count')
    list_filter = ('poll',)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'next_question',)
    list_filter = ('question',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('username', 'question', 'choice')
    list_filter = ('username', 'question',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
