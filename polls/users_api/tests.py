from rest_framework.test import APITestCase
from rest_framework import status
from polls.models import Poll, Question, Choice, UserChoice
from django.urls import reverse
from django.utils import timezone
from polls.admin_api import serializers as admin_serializers
from .serializers import FinishedPollsSerializer


def get_test_poll(name, description):
    return Poll.objects.create(name=name, description=description)


def get_test_question(poll, text, question_type):
    return Question.objects.create(poll=poll, text=text, question_type=question_type)


def get_test_choice(question, text):
    return Choice.objects.create(question=question, text=text)


class UserPollTestCase(APITestCase):

    def setUp(self):
        self.poll_1 = get_test_poll('Test poll 1', 'Test poll description 1')
        self.question_1_1 = get_test_question(self.poll_1, 'Test question text 1', 2)
        self.choice_1_1 = get_test_choice(self.question_1_1, text='Test Choice 1')
        self.choice_1_2 = get_test_choice(self.question_1_1, text='Test Choice 2')

        self.question_1_2 = get_test_question(self.poll_1, 'Test question text 2', 2)
        self.choice_2_1 = get_test_choice(self.question_1_2, text='Test Choice 1')
        self.choice_2_2 = get_test_choice(self.question_1_2, text='Test Choice 2')

        self.poll_2 = get_test_poll('Test poll 2', 'Test poll description 2')
        self.question_2_1 = get_test_question(self.poll_2, 'Test question text 1', 2)
        self.choice_2_1 = get_test_choice(self.question_2_1, text='Test Choice 1')
        self.choice_2_2 = get_test_choice(self.question_2_1, text='Test Choice 1')

        self.question_2_2 = get_test_question(self.poll_2, 'Test question text 2', 1)

    def test_user_can_access_only_active_polls(self):
        url = reverse('active_polls-list')
        response = self.client.get(url)
        active_polls = Poll.objects.exclude(ended__lte=timezone.now())
        serializer_data = admin_serializers.PollSerializer(active_polls, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_user_get_finished_polls(self):
        user_id = 321
        user_choice = UserChoice.objects.create(
            question=self.question_1_1, user_id=user_id)
        user_choice.choice.add(self.choice_1_1)
        url = reverse('polls_finished_by_user-list')
        payload = {"user_id": user_id}
        response = self.client.get(url, data=payload)
        finished_polls = Poll.objects.filter(questions__user_choices__user_id=user_id)
        serializer_data = FinishedPollsSerializer(set(finished_polls), many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_user_can_send_answer(self):
        user_id = 213
        url = reverse('user_choices-list')
        payload = {
            "question": self.question_2_2.id,
            "user_id": user_id,
            "text_choice": "Текст ответа"
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
