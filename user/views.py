from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from user.models import User as Usuario
from user.serializers import UsuarioSerializer , AtualizarSenhaSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class UsuarioCreateView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]


class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]  # ou [AllowAny] se quiser público



class UsuarioUpdateView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class UsuarioDeleteView(generics.DestroyAPIView):
    queryset = Usuario.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class AtualizarSenhaView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        user = get_object_or_404(Usuario, id=id)

        if request.user != user:
            return Response({"erro": "Você só pode mudar sua própria senha."}, status=403)

        serializer = AtualizarSenhaSerializer(data=request.data)
        if serializer.is_valid():
            nova_senha = serializer.validated_data['nova_senha']
            user.set_password(nova_senha)
            user.save()
            return Response({"mensagem": "Senha atualizada com sucesso."})
        return Response(serializer.errors, status=400)


