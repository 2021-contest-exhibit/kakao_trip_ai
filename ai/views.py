from django.shortcuts import render
import requests
from django.http import HttpResponse


def index(request):
    res = requests.get('http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode?ServiceKey=hopxVnTUPGecxaK%2BhbSb0LK0%2BMonhKp8GTyVMtrD8DE2NSucFjfWCHja06wJuxKdE7eW59gNaSnjQcMiJ0Kd5g%3D%3D&numOfRows=10&pageNo=1&MobileOS=AND&MobileApp=appName&_type=json')
    return HttpResponse(str(res.status_code) + " | " + res.text)