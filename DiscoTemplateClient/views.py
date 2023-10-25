from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from django.shortcuts import render

from DiscoTemplateClient.utils import (
    update_state_sync
)

from DiscoTemplateClient.permissions import AllowGETUnauthenticated

# ---------------- INDEX, ETC. ----------------

def index(request):
    update_state_sync({ 'host_url': request.get_host() })
    return render(request, "DiscoTemplateClient/index.html")



# ---------------- REST API --------------------

from DiscoTemplateClient import models, serializers


# Configuration / State limited to update (PUT)
class ConfigurationViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = serializers.ConfigurationSerializer
     
    def get_queryset(self):
        return models.Configuration.objects.filter(id=models.Configuration.objects.first().id)


class StateViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.StateSerializer

    def get_queryset(self):
        return models.State.objects.filter(id=models.State.objects.first().id)


class ErrLogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = models.ErrLog.objects.all()
    serializer_class = serializers.ErrLogSerializer

class EventLogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = models.EventLog.objects.all()
    serializer_class = serializers.EventLogSerializer

class DiscordServerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = models.DiscordServer.objects.all()
    serializer_class = serializers.DiscordServerSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer