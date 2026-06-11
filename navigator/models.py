from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва ролі")
    description = models.TextField(verbose_name="Опис професії")

    def __str__(self):
        return self.name

class Technology(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=100, verbose_name="Назва технології")

    def __str__(self):
        return f"{self.name} ({self.role.name})"

class RoadmapStep(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='roadmap_steps')
    step_number = models.IntegerField(verbose_name="Номер кроку")
    title = models.CharField(max_length=150, verbose_name="Назва кроку")
    description = models.TextField(verbose_name="Детальний опис кроку")

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Крок {self.step_number}: {self.title} ({self.role.name})"

class Question(models.Model):
    text = models.CharField(max_length=255, verbose_name="Текст запитання")
    order = models.IntegerField(default=0, verbose_name="Порядок запитання")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, verbose_name="Текст відповіді")
    role_points_to = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Додає бал до ролі")

    def __str__(self):
        return f"{self.question.text} -> {self.text}"


class Vacancy(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='vacancies')
    title = models.CharField(max_length=200, verbose_name="Назва вакансії")
    link = models.URLField(verbose_name="Посилання на вакансію")
    is_active = models.BooleanField(default=True, verbose_name="Активна?")

    def __str__(self):
        return self.title