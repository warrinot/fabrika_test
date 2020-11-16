from rest_framework.test import APITestCase
from rest_framework import status
from polls.models import Poll, Question, Choice, UserChoice
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .serializers import PollSerializer, QuestionSerializer, ChoiceSerializer


def get_test_poll(name, description):
    return Poll.objects.create(name=name, description=description)


def get_test_question(poll, text, question_type):
    return Question.objects.create(poll=poll, text=text, question_type=question_type)


def get_test_choice(question, text):
    return Choice.objects.create(question=question, text=text)


class AuthorizationTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='admin', is_staff=True)
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

    def test_admin_get_polls_only_if_authorized(self):
        url = reverse('poll-list')
        # response for unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

        # response for admin
        self.client.force_authenticate(self.user1)
        auth_response = self.client.get(url)
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)

    def test_not_admin_cant_get_polls(self):
        url = reverse('poll-list')
        regular_user = User.objects.create_user(username='regular user')
        self.client.force_authenticate(regular_user)
        self.assertTrue(regular_user.is_authenticated)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PollsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='admin', is_staff=True)
        self.client.force_authenticate(self.user1)
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

    def test_get_polls(self):
        url = reverse('poll-list')
        response = self.client.get(url)
        polls = Poll.objects.all()
        serializer_data = PollSerializer(polls, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post_polls(self):
        url = reverse('poll-list')
        data = {
            "name": "123",
            "description": "321"
        }
        self.assertEqual(2, Poll.objects.all().count())
        response = self.client.post(url, data=data)
        self.assertEqual(3, Poll.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_poll(self):
        url = reverse('poll-detail', args=(self.poll_1.id,))
        data = {
            "name": "321",
            "description": "123"
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_poll(self):
        url = reverse('poll-detail', args=(self.poll_1.id,))
        self.assertEqual(2, Poll.objects.all().count())
        response = self.client.delete(url)
        self.assertEqual(1, Poll.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class QuestionsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='admin', is_staff=True)
        self.client.force_authenticate(self.user1)
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

    def test_get_questions(self):
        url = reverse('question-list')
        response = self.client.get(url)
        questions = Question.objects.all()
        serializer_data = QuestionSerializer(questions, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post_questions(self):
        url = reverse('question-list')
        data = {
            "poll": 1,
            "text": "Текст",
            "question_type": 2
        }
        self.assertEqual(4, Question.objects.all().count())
        response = self.client.post(url, data=data)
        self.assertEqual(5, Question.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_question(self):
        url = reverse('question-detail', args=(self.question_1_1.id,))
        data = data = {
            "poll": 2,
            "text": "Новый Текст",
            "question_type": 3
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_question(self):
        url = reverse('question-detail', args=(self.question_1_1.id,))
        self.assertEqual(4, Question.objects.all().count())
        response = self.client.delete(url)
        self.assertEqual(3, Question.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ChoicesTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='admin', is_staff=True)
        self.client.force_authenticate(self.user1)
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

    def test_get_choices(self):
        url = reverse('choice-list')
        response = self.client.get(url)
        choices = Choice.objects.all()
        serializer_data = ChoiceSerializer(choices, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post_choices(self):
        url = reverse('choice-list')
        data = {
            "question": 1,
            "text": "Опция 1"
        }
        self.assertEqual(6, Choice.objects.all().count())
        response = self.client.post(url, data=data)
        self.assertEqual(7, Choice.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_choice(self):
        url = reverse('choice-detail', args=(self.choice_1_1.id,))
        data = {
            "question": 2,
            "text": "Опция 2"
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_choice(self):
        url = reverse('choice-detail', args=(self.choice_1_1.id,))
        self.assertEqual(6, Choice.objects.all().count())
        response = self.client.delete(url)
        self.assertEqual(5, Choice.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
