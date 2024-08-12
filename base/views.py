from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from models import User
from rest_framework.decorators import api_view

@api_view(['POST'])
def signup(request):
    data = JSONParser().parse(request)
    print(data)
    user = User.objects.create_user(
        username = data['username'],
        password = data['password'],
    )
    return JsonResponse({'id': user.id, 'username': user.username})