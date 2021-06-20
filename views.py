from django.http import HttpResponse
from django import forms
import json
from django.http import JsonResponse
import sqlite3
from datetime import datetime
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from get_data_iherb import get_vitamin, get_questions_func, get_article_func, decision


@require_http_methods(["GET", "POST"])
@csrf_exempt
def add_person(request):
    if 'fullname' in request.POST:
        characteristic_identifiers = {"fullname": request.POST['fullname']}
        if 'biologicalSex' in request.POST:
            characteristic_identifiers['biologicalSex'] = request.POST['biologicalSex']
        if 'bloodType' in request.POST:
            characteristic_identifiers['bloodType'] = request.POST['bloodType']
        if 'dateOfBirthComponents' in request.POST:
            characteristic_identifiers['dateOfBirthComponents'] = request.POST['dateOfBirthComponents']
        activity = {""}
        data = {'characteristic_identifiers': characteristic_identifiers}
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response
    else:
        return HttpResponse("Не введено имя")


def get_products(request):
    # Товары из магазина
    res = get_vitamin(request.GET)
    response = JsonResponse(res, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response


def get_article(request):
    # Получить статьи с блога
    res = get_article_func(request.GET)
    #response = JsonResponse(res, safe=False)
    response = HttpResponse(str(res), content_type="application/json; charset=utf-8")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

    
def get_questions(request):
    # Получить список вопросов
    res = get_questions_func()
    response = HttpResponse(str(res).replace("'", '"'), content_type="application/json; charset=utf-8")
    #response = JsonResponse(res, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    response['Content-Type'] = 'application/json; charset=utf-8'
    return response
    
    
@require_http_methods(["GET", "POST"])
@csrf_exempt
def desicion_view(request):
    # Обработка данных пользователя, диагноз, рекомендации
    with open('post.txt', 'at') as f:
        f.write(str(request.POST))
        f.write('\n')
    res = decision(request.POST)
    response = HttpResponse(str(res).replace("'", '"'), content_type="application/json; charset=utf-8")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    response['Content-Type'] = 'application/json; charset=utf-8'
    return response
