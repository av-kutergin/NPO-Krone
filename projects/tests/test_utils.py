from django.test import TestCase

from projects.templatetags.language_selector import new_lang_code, new_lang_name
from projects.utils import get_uuid_id, get_day_word


class ModelTests(TestCase):

    def test_uid_generation(self):
        for i in range(50):
            uid_1 = get_uuid_id()
            uid_2 = get_uuid_id()
            self.assertNotEqual(uid_1, uid_2)

    def test_day_word_selector(self):
        self.assertEqual(get_day_word(0), 'дней')
        self.assertEqual(get_day_word(20), 'дней')
        self.assertEqual(get_day_word(21), 'день')
        self.assertEqual(get_day_word(3), 'дня')

    def test_lang_changer(self):
        self.assertEqual(new_lang_code('en'), 'ru')
        self.assertEqual(new_lang_code('ru'), 'en')

    def test_lang_name_selector(self):
        self.assertEqual(new_lang_name('en'), 'Russian')
        self.assertEqual(new_lang_name('anything'), 'English')





