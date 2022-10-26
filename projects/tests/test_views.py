from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory, Client


class ViewsTests(TestCase):
    def setUpTestData(cls) -> None:
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username='Jack8369587426',
            email='abirvalg@lasdf.am',
            password='jasdfjkn,m1',
        )

        cls.client = Client()