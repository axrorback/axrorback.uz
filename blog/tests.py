from unittest.mock import patch

import requests
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import QuestionForm
from .models import Question
from .views import send_telegram_message


class QuestionFormTests(TestCase):
    def test_phone_number_accepts_standard_uzbek_format(self):
        form = QuestionForm(
            data={
                'name': 'Ali',
                'phone_number': '+998901234567',
                'question': 'Savol',
            }
        )
        self.assertTrue(form.is_valid())

    def test_phone_number_rejects_more_than_nine_digits_after_prefix(self):
        form = QuestionForm(
            data={
                'name': 'Ali',
                'phone_number': '+9989012345678',
                'question': 'Savol',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)


class AskQuestionViewTests(TestCase):
    @patch('blog.views.send_telegram_message')
    def test_valid_post_redirects_to_thanks(self, mocked_send):
        response = self.client.post(
            reverse('ask_question'),
            data={
                'name': 'Vali',
                'phone_number': '+998991112233',
                'question': 'Yordam kerak',
            },
        )

        self.assertRedirects(response, reverse('thanks'))
        self.assertEqual(Question.objects.count(), 1)
        mocked_send.assert_called_once()

    @patch('blog.views.requests.post', side_effect=requests.RequestException('network'))
    def test_valid_post_still_redirects_if_telegram_request_fails(self, mock_requests_post):
        with self.assertLogs('blog.views', level='WARNING') as logs:
            response = self.client.post(
                reverse('ask_question'),
                data={
                    'name': 'Vali',
                    'phone_number': '+998991112233',
                    'question': 'Yordam kerak',
                },
            )

        self.assertRedirects(response, reverse('thanks'))
        self.assertEqual(Question.objects.count(), 1)
        mock_requests_post.assert_called_once()
        self.assertTrue(
            any("Telegram xabari yuborilmadi" in message for message in logs.output)
        )


class SendTelegramMessageTests(TestCase):
    @override_settings(TELEGRAM_BOT_TOKEN='', TELEGRAM_CHANNEL_ID='')
    @patch('blog.views.requests.post')
    def test_skips_request_when_telegram_credentials_missing(self, mock_requests_post):
        with self.assertLogs('blog.views', level='INFO') as logs:
            send_telegram_message('test')

        mock_requests_post.assert_not_called()
        self.assertTrue(
            any("Telegram konfiguratsiyasi yo'q" in message for message in logs.output)
        )
