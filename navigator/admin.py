from django.contrib import admin
from .models import Role, Question, Answer, Technology, Vacancy, RoadmapStep

# Цей клас дозволяє додавати відповіді прямо на сторінці створення запитання
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3 # Скільки порожніх полів для відповідей показувати відразу

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'order')

# Реєструємо всі наші таблиці
admin.site.register(Role)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Technology)
admin.site.register(Vacancy)
admin.site.register(RoadmapStep)