# usuarios/serializers.py
from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Pode adicionar informações extras no token, se quiser
        token['email'] = user.email
        token['nome'] = user.nome
        return token


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        nome_completo = validated_data.pop("nome", "")
        partes = nome_completo.split()

        primeiro_nome = partes[0] if partes else ""
        sobrenome = " ".join(partes[1:]) if len(partes) > 1 else ""

        validated_data["nome"] = primeiro_nome
        validated_data["sobrenome"] = sobrenome

        senha = validated_data.pop('senha')
        user = User(**validated_data)
        user.set_password(senha)
        user.save()
        return user


class AtualizarSenhaSerializer(serializers.Serializer):
    nova_senha = serializers.CharField(write_only=True, min_length=6)