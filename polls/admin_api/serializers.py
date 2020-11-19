from rest_framework import serializers
from polls.models import Poll, Question, Choice, UserChoice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'poll', 'text', 'question_type', 'choices']


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'started', 'ended', 'description', 'questions']


class UserChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChoice
        fields = ['choice', 'user']


class NestedChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']


class NestedQuestionSerializer(serializers.ModelSerializer):
    choices = NestedChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['text', 'question_type', 'choices']


class NestedSerializer(serializers.ModelSerializer):
    questions = NestedQuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'started', 'ended', 'description', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)

        for question_data in questions_data:
            choices_data = question_data.pop('choices')

            question = Question.objects.create(poll=poll, **question_data)
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)

        return poll
