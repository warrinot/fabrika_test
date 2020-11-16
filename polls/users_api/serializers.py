from rest_framework import serializers
from polls.models import UserChoice, Poll, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'user_choices']


class UserChoiceSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer()
    # text_choice = serializers.CharField(max_length=255)

    class Meta:
        model = UserChoice
        fields = ['question', 'choice', 'user_id', 'text_choice']


class FinishedPollsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'started', 'ended', 'questions']
