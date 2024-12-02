import random

from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render


class ListUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ListUsersSerializer


class AuthUserView(APIView):
    def get(self, request):        
        return render(request, 'auth.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = authenticate(request, phone_number=phone_number)
            if user is not None:
                login(request, user, backend='referral_system.backends.PhoneNumberBackend')
                return Response({'message': 'Вы успешно авторизовались'}, status=status.HTTP_200_OK)
            else:
                register_serializer = RegisterSerializer(data=request.data)
                if register_serializer.is_valid():
                    user = register_serializer.save()
                    login(request, user, backend='referral_system.backends.PhoneNumberBackend')
                    return Response({'message': 'Вы успешно зарегистрировались и авторизовались'}, status=status.HTTP_201_CREATED)
        print(serializer.errors) # Добавляем вывод ошибок сериализатора для отладки
        return Response({'message': 'Вы неправильно ввели данные!'}, status=status.HTTP_400_BAD_REQUEST)
    

def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'переадресация на главную страницу...'})