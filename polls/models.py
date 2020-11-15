from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=255)
    started = models.DateTimeField(auto_now=True, editable=False)
    ended = models.DateTimeField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    TEXT_OPTION = 1
    SINGLE_OPTION = 2
    MULTIPLE_OPTIONS = 3
    QUESTION_TYPES = [(TEXT_OPTION, 'text_option'),
                      (SINGLE_OPTION, 'single_option'),
                      (MULTIPLE_OPTIONS, 'multiple_options')]
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.PositiveIntegerField(choices=QUESTION_TYPES)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey('Question', related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)  # models.PositiveIntegerField

    def __str__(self):
        return self.text


class UserChoice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='user_choices')
    choice = models.ManyToManyField('Choice', blank=True, related_name='user_choices')
    user_id = models.PositiveIntegerField()
    text_choice = models.TextField(max_length=255, blank=True)
