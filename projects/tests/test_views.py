import shutil
import time
from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.core.files.temp import NamedTemporaryFile
from django.db.models.fields import files
from django.db.models.signals import post_save
from django.test import RequestFactory, Client
from django.test import TestCase, override_settings
from django.urls import reverse

from projects.models import Project, Guest, Document, set_doc_image
from projects.utils import get_uuid_id
from projects.views import main_page, team, projects, donate, login_page, ShowProject, \
    DocumentListView, download_file

TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username='my_username',
            email='abirvalg@lasdf.am',
            password='my_password',
        )
        cls.user.save()

        cls.project_1 = Project.objects.create(
            # id=2,
            name='tomorrows event',
            content=('x' * 50),
            price=300,
            date=datetime.now() + timedelta(days=1),
            total_places=0,
            qr_reveal_date=date.today(),
            howto='how to get',
            slug='tomorrows-event',
            photo=b''
        )
        cls.project_1.save()

        cls.guest_1 = Guest.objects.create(
            # id=1,
            firstname='Stephen',
            lastname='Hawking',
            birthdate='1942-01-08',
            phone='+12345678911',
            email='Stephen@Hawking.com',
            telegram='@SHawking',
            project=cls.project_1,
            ticket_uid=get_uuid_id(),
        )
        cls.guest_1.save()

        cls.document_1 = Document.objects.language('en').create(\
            file=files.File(NamedTemporaryFile(), name='my_document_1.pdf'),
            image=files.File(NamedTemporaryFile(), name='my_document_1.png'),
            name='my_doc',
        )
        cls.document_1.set_current_language('ru')
        cls.document_1.name = 'my_doc_ru'
        post_save.disconnect(set_doc_image, sender=Document)
        cls.document_1.save()
        post_save.connect(set_doc_image, sender=Document)

        cls.client = Client()

    def test_main_page(self):
        request = self.factory.get('')
        response = main_page(request)
        self.assertEqual(response.status_code, 200)

    def test_team(self):
        request = self.factory.get('team')
        response = team(request)
        self.assertEqual(response.status_code, 200)

    def test_projects(self):
        request = self.factory.get('projects')
        response = projects(request)
        self.assertEqual(response.status_code, 200)

    # def test_contacts(self):
    #     request = self.factory.get('contacts')
    #     response = contacts(request)
    #     self.assertEqual(response.status_code, 200)

    def test_donate(self):
        request = self.factory.get('donate')
        response = donate(request)
        self.assertEqual(response.status_code, 200)

    # def test_sitemap(self):
    #     request = self.factory.get('sitemap')
    #     response = sitemap(request)
    #     self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        request = self.factory.get('accounts/login')
        response = login_page(request)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        data = {'username': 'my_username', 'password': 'my_password'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)

    def test_show_project(self):
        path = self.project_1.get_absolute_url()
        request = self.factory.get(path)
        response = ShowProject.as_view()(request, project_slug='tomorrows-event')
        self.assertEqual(response.status_code, 200)

    def test_documents_view(self):
        request = self.factory.get('documents')
        response = DocumentListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_document_file_download(self):
        path = self.document_1.download()
        request = self.factory.get(path)
        response = download_file(request, file_type='document', pk=1)
        self.assertEqual(response.status_code, 200)

    def test_qr_image_download(self):
        path = self.guest_1.download_qr_image()
        request = self.factory.get(path)
        response = download_file(request, file_type='qr_image', pk=self.guest_1.id)
        self.assertEqual(response.status_code, 200)

    # def test_howto(self):
    #     request = self.factory.get('how_to')
    #     response = how_to_view(request, project_slug=self.project_1.slug, ticket_uid=self.guest_1.ticket_uid)
    #     self.assertEqual(response.status_code, 200)

    def test_participate(self):
        data = {
            'firstname': 'Linus',
            'lastname': 'Torvalds',
            'birthdate': '1969-12-28',
            'phone': '+12345678911',
            'email': 'LTorvalds@linker.eu',
            'telegram': '@LTorvalds',
        }
        response = self.client.post(reverse('participate', kwargs={'project_slug': self.project_1.slug}), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Guest.objects.all()), 2)

    def test_participate_invalid_form(self):
        data = {
            'firstname': 'Linus',
            'lastname': 'Torvalds',
            'birthdate': '1969-12-28',
            'phone': '',
            'email': 'LTorvalds@linker.eu',
            'telegram': '@LTorvalds',
        }
        response = self.client.post(reverse('participate', kwargs={'project_slug': self.project_1.slug}), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Guest.objects.all()), 1)

    def test_set_arrived(self):
        self.client.login(username='my_username', password='my_password')
        self.guest_3 = Guest.objects.create(
            # id=1,
            firstname='Stephen',
            lastname='Hawking',
            birthdate='1942-01-08',
            phone='+12345678911',
            email='Stephen@Hawking.com',
            telegram='@SHawking',
            project=self.project_1,
            ticket_uid=get_uuid_id(),
            paid=True,
        )
        response = self.client.get(reverse('set_arrived', kwargs={'ticket_uid': self.guest_3.ticket_uid}))
        self.assertEqual(response.status_code, 302)
        # self.assertTrue(self.guest_3.arrived)

    # def test_service_page(self):
    #     self.client.login(username='my_username', password='my_password')
    #     response = self.client.get(reverse(
    #         'service_page',
    #         kwargs={'project_slug': self.project_1.slug, 'ticket_uid': self.guest_1.ticket_uid}))
    #     self.assertEqual(response.status_code, 200)

    def test_service_page_no_object(self):
        self.client.login(username='my_username', password='my_password')
        request = self.factory.get('service_page')
        response = ShowProject.as_view()(
            request,
            project_slug=self.project_1.slug,
            ticket_uid='wrong-ticket',
        )
        self.assertEqual(response.status_code, 200)

    # def test_guest_list(self):
    #     self.client.login(username='my_username', password='my_password')
    #     response = self.client.get(reverse('guest_list', kwargs={'project_slug': self.project_1.slug}))
    #     self.assertEqual(response.status_code, 200)

    def test_payment_success(self):
        pass

    def test_result_payment(self):
        pass


def tearDownModule():
    print("\nDeleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
