from django.shortcuts import render, redirect
from .models import Question, Role, Answer
import json
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Імпорти для шрифтів
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def home(request):
    if 'answers' in request.session:
        del request.session['answers']
    return render(request, 'navigator/home.html')

def test(request):
    questions = Question.objects.prefetch_related('answers').all()
    if request.method == 'GET':
        return render(request, 'navigator/question.html', {'questions': questions})
    elif request.method == 'POST':
        results_json = request.POST.get('results')
        if results_json:
            request.session['answers'] = json.loads(results_json)
        return redirect('user_info')

def user_info(request):
    if request.method == 'POST':
        request.session['user_name'] = request.POST.get('name')
        request.session['user_email'] = request.POST.get('email')
        return redirect('results') 
    return render(request, 'navigator/info.html')

def results(request):
    answers_dict = request.session.get('answers')
    if not answers_dict:
        return redirect('home')

    role_scores = {role.name: 0 for role in Role.objects.all()}
    for q_index_str, answer_id in answers_dict.items():
        try:
            ans = Answer.objects.get(id=answer_id)
            role_name = ans.role_points_to.name
            role_scores[role_name] = role_scores.get(role_name, 0) + 1
        except Answer.DoesNotExist:
            continue

    if not role_scores:
        return redirect('home')
        
    winner_name = max(role_scores, key=role_scores.get)
    winner_role = Role.objects.get(name=winner_name)

    context = {
        'user_name': request.session.get('user_name', 'Кандидат'),
        'winner': winner_role,
        'roadmap': winner_role.roadmap_steps.all(),
        'technologies': winner_role.technologies.all(),
        'vacancies': winner_role.vacancies.filter(is_active=True),
        'chart_labels': json.dumps(list(role_scores.keys())),
        'chart_data': json.dumps(list(role_scores.values())),
    }
    return render(request, 'navigator/results.html', context)

def download_pdf(request):
    answers_dict = request.session.get('answers')
    if not answers_dict:
        return redirect('home')

    # Реєстрація шрифту БЕЗ використання тимчасових папок (якщо виникає помилка 13, 
    # просто видали ці 2 рядки нижче, і PDF завантажиться без української мови)
    pdfmetrics.registerFont(TTFont('MyFont', 'DejaVuSans.ttf'))

    user_name = request.session.get('user_name', 'Кандидат')
    role_scores = {role.name: 0 for role in Role.objects.all()}
    for q_index_str, answer_id in answers_dict.items():
        try:
            ans = Answer.objects.get(id=answer_id)
            role_name = ans.role_points_to.name
            role_scores[role_name] += 1
        except Answer.DoesNotExist:
            continue
    winner_name = max(role_scores, key=role_scores.get)
    winner_role = Role.objects.get(name=winner_name)

    context = {
        'user_name': user_name,
        'winner': winner_role,
        'roadmap': winner_role.roadmap_steps.all(),
        'technologies': winner_role.technologies.all(),
    }

    template = get_template('navigator/pdf_report.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="IDEIL_Career_Plan_{user_name}.pdf"'

    pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=response, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse('Помилка PDF', status=500)
    return response