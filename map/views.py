from rest_framework import viewsets, permissions
from .models import TimeMarker
from .serializers import TimeMarkerSerializer

class TimeMarkerViewSet(viewsets.ModelViewSet):
    queryset = TimeMarker.objects.all()
    serializer_class = TimeMarkerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
