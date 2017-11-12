from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from qa.models import (Answer, AnswerComment, AnswerVote, Question,
                       QuestionComment, UserQAProfile)

class AnswerInline(admin.TabularInline):
	model = Answer
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields':['description']}),
	]
	inlines = [AnswerInline]
	list_display = ('title','description')
	search_fields=['description']
		
		
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, MarkdownModelAdmin)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
admin.site.register(AnswerVote)
admin.site.register(UserQAProfile)
