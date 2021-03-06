from rest_framework import viewsets
from rest_framework import permissions
from polls.admin_api.serializers import (PollSerializer,
                                         QuestionSerializer,
                                         ChoiceSerializer,
                                         NestedSerializer)
from polls.models import Poll, Question, Choice


class PollViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    queryset = Question.objects.all().select_related('poll')
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    queryset = Choice.objects.all().select_related('question')
    serializer_class = ChoiceSerializer


class NestedPollViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    queryset = Poll.objects.all()
    serializer_class = NestedSerializer
    http_method_names = ['get', 'post', 'head']
