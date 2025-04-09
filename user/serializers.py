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

    def validate_foto_perfil(self, value):
        # Tipos de imagem permitidos
        valid_types = ['image/jpeg', 'image/png', 'image/jpg']
        if hasattr(value, 'content_type') and value.content_type not in valid_types:
            raise serializers.ValidationError("A imagem deve ser do tipo JPEG ou PNG.")

        # Tamanho máximo: 5MB
        max_size = 5 * 1024 * 1024  # 5 megabytes
        if value.size > max_size:
            raise serializers.ValidationError("A imagem não pode ser maior que 5MB.")

        return value

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