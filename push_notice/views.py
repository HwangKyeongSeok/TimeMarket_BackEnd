from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DeviceTokenSerializer
from .models import DeviceToken
from .services import send_push_to_user
from users.models import User


class RegisterDeviceTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({"token": obj.token, "platform": obj.platform}, status=status.HTTP_201_CREATED)


class UnregisterDeviceTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "token is required"}, status=400)
        DeviceToken.objects.filter(token=token, user=request.user).update(is_active=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TestSendPushView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 본인에게 테스트 발송
        title = request.data.get("title", "Test Push")
        body = request.data.get("body", "This is a test push message")
        result = send_push_to_user(request.user, title, body, data={"type": "test"})
        return Response(result)

