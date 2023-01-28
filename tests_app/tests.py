from django.test import TestCase
from django.urls import reverse, resolve

from .models import Question, Theme, TestEntry
from .views import QuestionListView


class QuestionTests(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.theme1 = Theme.objects.create(
            name='Python',
        )
        cls.theme2 = Theme.objects.create(
            name='Django',
            parent=cls.theme1,
        )

        cls.q1 = Question.objects.create(
            question='Python question',
            answer='answer one',
            theme=cls.theme1,
        )
        cls.q2 = Question.objects.create(
            question='Django question',
            answer='answ 2',
            theme=cls.theme2,
        )

        cls.test1 = TestEntry.objects.create()
        cls.test1.questions.add(cls.q1)
        cls.test1.questions.add(cls.q2)

    def test_homepage_url_resovles_homepageview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, QuestionListView.as_view().__name__)

    def test_question_listing(self):
        self.assertEqual(self.q1.question, 'Python question')
        self.assertEqual(self.q1.answer, 'answer one')
        self.assertEqual(self.q1.theme.name, 'Python')
        self.assertEqual(self.q2.question, 'Django question')
        self.assertEqual(self.q2.answer, 'answ 2')
        self.assertEqual(self.q2.theme.name, 'Django')
        self.assertEqual(self.q2.theme.parent.name, 'Python')

    def test_theme_list_view(self):
        response = self.client.get(reverse('themes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')
        self.assertContains(response, 'Django')
        self.assertTemplateUsed(response, 'tests_app/themes.html')

    def test_theme_detail_view(self):
        response = self.client.get(self.theme1.get_absolute_url())
        no_response = self.client.get(reverse('theme_detail', args=['doesnotexist']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Python')
        self.assertContains(response, 'Python question')
        self.assertContains(response, 'answer one')
        self.assertTemplateUsed(response, 'tests_app/questions.html')
    
    def test_question_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertContains(response, 'Django question')
        self.assertContains(response, 'answ 2')
        self.assertTemplateUsed(response, 'tests_app/questions.html')
    
    def test_testentry_listing(self):
        self.assertEqual(self.test1.questions.get(pk=self.q1.pk).question, 'Python question')
        self.assertEqual(self.test1.questions.get(pk=self.q1.pk).answer, 'answer one')
        self.assertEqual(self.test1.questions.get(pk=self.q1.pk).theme.name, 'Python')
        self.assertEqual(self.test1.questions.get(pk=self.q2.pk).question, 'Django question')
        self.assertEqual(self.test1.questions.get(pk=self.q2.pk).answer, 'answ 2')
        self.assertEqual(self.test1.questions.get(pk=self.q2.pk).theme.name, 'Django')
        self.assertEqual(self.test1.questions.get(pk=self.q2.pk).theme.parent.name, 'Python')

    def test_testentry_list_view(self):
        response = self.client.get(reverse('test_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertContains(response, 'Django question')
        self.assertNotContains(response, 'answ 2')
        self.assertTemplateUsed(response, 'tests_app/tests.html')

    def test_testentry_detail_view_pageone(self):
        response = self.client.get(f"{reverse('test_detail', args=[self.test1.pk])}?q=1")
        no_response = self.client.get(reverse('test_detail', args=[12345]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Python')
        self.assertContains(response, 'Python question')
        self.assertContains(response, 'answer one')
        self.assertContains(response, 'Next') # next link
        self.assertTemplateUsed(response, 'tests_app/test_detail.html')

    def test_testentry_detail_view_pagetwo(self):
        response = self.client.get(f"{reverse('test_detail', args=[self.test1.pk])}?q=2")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertContains(response, 'Django question')
        self.assertContains(response, 'answ 2')
        self.assertNotContains(response, 'Next') # next link
        self.assertTemplateUsed(response, 'tests_app/test_detail.html')
