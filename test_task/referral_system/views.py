import random

from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        if user.my_refer:
            return Response({"error": "You can only set my_refer once."}, status=status.HTTP_400_BAD_REQUEST)

        invite_code = request.data.get('my_refer')
        if not CustomUser.objects.filter(invite_code=invite_code).exists():
            return Response({'error': 'Указанный invite_code не существует'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthUserView(APIView):

    def get(self, request):        
        return render(request, 'auth.html')

    def post(self, request):
        if request.data.get('verification_code'):
            return self.verify_code(request)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = authenticate(request, phone_number=phone_number)
            verification_code = self.generate_verification_code()
            print(verification_code)
            request.session['verification_code'] = verification_code
            request.session['phone_number'] = phone_number

            if user is not None:
                request.session['is_new_user'] = False
            else:
                register_serializer = RegisterSerializer(data=request.data)
                if register_serializer.is_valid():
                    user = register_serializer.save()
                    request.session['is_new_user'] = True
                else:
                    return Response({'message': 'Вы неправильно ввели данные!'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Код отправлен', 'code_sent': True, 'verification_code': verification_code}, status=status.HTTP_200_OK)

        return Response({'message': 'Вы неправильно ввели данные!'}, status=status.HTTP_400_BAD_REQUEST) 

    def generate_verification_code(self):
        return str(random.randint(1000, 9999))
    
    def verify_code(self, request):
        entered_code = request.data.get('verification_code')
        stored_code = request.session.get('verification_code')
        phone_number = request.session.get('phone_number')
        user = authenticate(request, phone_number=phone_number)

        if entered_code == stored_code:
            is_new_user = request.session.get('is_new_user')
            login(request, user, backend='referral_system.backends.PhoneNumberBackend')
            if is_new_user:
                return Response({'message': 'Вы успешно зарегистрировались и авторизовались', 'authorized': True}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Вы успешно авторизовались', 'authorized': True}, status=status.HTTP_200_OK)
        return Response({'message': 'Неверный код', 'authorized': False}, status=status.HTTP_400_BAD_REQUEST)


def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'переадресация на главную страницу...'})