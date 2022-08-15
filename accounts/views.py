from django.shortcuts import render

# Create your views here.
from .models import Account

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_users=Account.objects.all()
    # Доступные книги (статус = 'a')
    
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_users':num_users},
    )