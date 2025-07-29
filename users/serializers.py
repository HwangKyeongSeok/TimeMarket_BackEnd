from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# 회원가입용
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # username -> nickname 으로 변경
        fields = ['id', 'nickname', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            # username -> nickname 으로 변경
            nickname=validated_data["nickname"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user

# 사용자 정보 조회 및 수정용
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email']

# 로그인용 (JWT 커스터마이징 가능)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # username_field를 nickname으로 설정
    username_field = 'nickname'

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'nickname': self.user.nickname,
            'email': self.user.email,
        })
        return data
