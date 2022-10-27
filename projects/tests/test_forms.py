from datetime import date

from django.test import SimpleTestCase

from projects.forms import AddGuestForm


class TestForms(SimpleTestCase):

    def test_add_guest_form_valid(self):
        form = AddGuestForm(data={
            'firstname': 'Linus',
            'lastname': 'Torvalds',
            'birthdate': '1969-12-28',
            'phone': '+12345678911',
            'email': 'LTorvalds@linker.eu',
            'telegram': '@LTorvalds',
        })
        self.assertTrue(form.is_valid())

    def test_add_guest_form_invalid(self):
        form = AddGuestForm(data={
            'firstname': 'Linus',
            'lastname': '',
            'birthdate': '',
            'phone': '+258',
            'email': 'LTorvalds@linker.eu',
            'telegram': '@LTorvalds',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_add_guest_form_no_data(self):
        form = AddGuestForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)
