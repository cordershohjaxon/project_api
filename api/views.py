from django.contrib.auth import get_user_model
from rest_framework import permissions

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_main.models import Note
from .serializers import NoteSerializer, UserSerializer
from .permissions import IsOwner, IsSelfOrReadOnly

User = get_user_model()


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(owner=request.user)
        serializer = NoteSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSelfOrReadOnly]
        return [permission() for permission in permission_classes]
