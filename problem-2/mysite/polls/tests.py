from django.test import TestCase
import datetime

from django.urls import reverse
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        old_question = Question(pub_date=timezone.now() - datetime.timedelta(days=1, seconds=1))
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recently_question(self):
        recently_question = Question(pub_date=timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59))
        self.assertIs(recently_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")  # html코드에 <p>No polls are available.</p>가 포함되었는지
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question('past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No polls are available")  # html코드에 <p>No polls are available.</p>가 포함되었는지
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        question = create_question('future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")  # html코드에 <p>No polls are available.</p>가 포함되었는지
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question('future question', days=30)
        question = create_question('past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No polls are available")  # html코드에 <p>No polls are available.</p>가 포함되었는지
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_two_past_question(self):
        question1 = create_question('past question 1', days=-30)
        question2 = create_question('past question 2', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No polls are available")  # html코드에 <p>No polls are available.</p>가 포함되었는지
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1])  # 정렬여부까지 확인


class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        future_question = create_question("future_question", days=30)
        response = self.client.get(reverse('polls:detail', kwargs={'pk': future_question.pk}))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("past_question", days=-30)
        response = self.client.get(reverse('polls:detail', kwargs={'pk': past_question.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

