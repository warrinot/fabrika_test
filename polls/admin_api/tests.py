from rest_framework.test import APITestCase
from rest_framework import status
from polls.models import Poll, Question, Choice, UserChoice
from django.urls import reverse
from django.utils import timezone


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
