from django.shortcuts import render
from django.contrib.auth import authenticate, logout

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserRegisterSerializer
from .models import User
 
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
  serializer_class = UserRegisterSerializer

  def create(self, request, *arg, **kwargs):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
      return Response({"msg": "Los campos no pueden estar vacios"}, status=status.HTTP_400_BAD_REQUEST)

    if email and User.objects.filter(email=email).exists():
      return Response({"msg": "Correo electronico ya registrado"}, status=status.HTTP_400_BAD_REQUEST)

    data = {
      'email': email,
      'password': password,
    }

    serializer = self.get_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user_serializer = UserSerializer(user)

    return Response(user_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login_view(request):
  email = request.data.get("email")
  password = request.data.get("password")

  if not email or not password:
    return Response({"msg": "Debe introducir correo y contraseña"}, status=status.HTTP_400_BAD_REQUEST)

  if email and not User.objects.filter(email=email).exists():
    return Response({"msg": "Correo electronico no registrado"}, status=status.HTTP_404_NOT_FOUND)

  user = authenticate(request, email=email, password=password)

  if not user:
    return Response({"msg": "Error en credenciales, verificar y corregir"}, status=status.HTTP_400_BAD_REQUEST)
  
  user_serializer = UserSerializer(user)
  return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'msg': 'Cierre de sesión exitoso'})
