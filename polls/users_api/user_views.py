from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from polls.admin_api.serializers import PollSerializer
from polls.models import Poll, UserChoice
from .permissions import IsAdminorReadOnly
from .serializers import UserChoiceSerializer, FinishedPollsSerializer
from polls.models import Question


class ActivePollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminorReadOnly]
    queryset = Poll.objects.exclude(ended__lte=timezone.now())
    serializer_class = PollSerializer


class UserChoiceViewsSet(viewsets.ViewSet):

    def create(self, request):
        serializer = UserChoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_id = serializer.validated_data.get('user_id')
        question = serializer.validated_data.get('question')

        # check if user already answered this question
        try:
            user_choice = UserChoice.objects.get(question=question, user_id=user_id)
        except UserChoice.DoesNotExist:
            user_choice = False

        if user_choice:
            return Response('User already answered', status=status.HTTP_400_BAD_REQUEST)

        # check if it is text choice answer
        if question.question_type == Question.TEXT_OPTION:
            if not serializer.validated_data.get('text_choice'):
                return Response('Question answer should be text',
                                status=status.HTTP_400_BAD_REQUEST)

        # check if it is single option answer
        elif question.question_type == Question.SINGLE_OPTION:
            if len(serializer.validated_data.get('choice')) != 1:
                return Response('Question answer should be single option',
                                status=status.HTTP_400_BAD_REQUEST)
        # check if it is multiple options answer
        elif question.question_type == Question.MULTIPLE_OPTIONS:
            if not serializer.validated_data.get('choice'):
                return Response('Question answer should contain option',
                                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserFinishedPolls(viewsets.ViewSet):

    permission_classes = [IsAdminorReadOnly]

    def list(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response('user_id was not provided', status.HTTP_400_BAD_REQUEST)
        polls = Poll.objects.filter(questions__user_choices__user_id=user_id)
        serializer = FinishedPollsSerializer(set(polls), many=True)
        return Response(serializer.data, status.HTTP_200_OK)
