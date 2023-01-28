from django.contrib import admin

from .models import Question, Theme, TestEntry


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'theme')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Theme)
admin.site.register(TestEntry)
