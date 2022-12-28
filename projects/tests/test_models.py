import shutil

from datetime import date, datetime, timedelta

from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User
from django.db.models.fields import files
from django.db.models.signals import post_save
from django.test import TestCase, override_settings

from projects.models import Project, Guest, TeamMate, DonateButton, Carousel, Document, set_doc_image
from projects.utils import get_uuid_id, calculate_signature

TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='123',
            email='abirvalg@lasdf.am',
            password='jasdfjkn,m1'
        )
        cls.user.save()
        cls.project_1 = Project.objects.create(
            # id=1,
            name='forthcoming event',
            price=200,
            date=datetime.now() + timedelta(days=5),
            total_places=1,
            qr_reveal_date=date.today() + timedelta(days=4),
            howto='how to get',
            slug='forthcoming-event',
        )
        cls.project_1.save()
        cls.project_2 = Project.objects.create(
            # id=2,
            name='already passed event',
            content=('x' * 250),
            price=300,
            date=datetime.now() - timedelta(days=5),
            total_places=10,
            qr_reveal_date=date.today() - timedelta(days=6),
            howto='how to get',
            slug='already-passed-event',
        )
        cls.project_2.save()
        cls.project_3 = Project.objects.create(
            # id=2,
            name='tomorrows event',
            content=('x' * 50),
            price=300,
            date=datetime.now() + timedelta(days=1),
            total_places=0,
            qr_reveal_date=date.today(),
            howto='how to get',
            slug='tomorrows-event',
        )
        cls.project_3.save()
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
        cls.guest_2 = Guest.objects.create(
            # id=2,
            firstname='Guido',
            lastname='vanRossum',
            birthdate='1956-01-31',
            phone='+12345678911',
            email='Guido@vanRossum.com',
            telegram='@GvanRossum',
            project=cls.project_2,
            ticket_uid=get_uuid_id(),
            paid=True,
        )
        cls.guest_2.save()
        cls.don_button_1 = DonateButton.objects.create(amount=20)
        cls.don_button_1.save()

    def test_dummy(self):
        self.assertEqual(2 + 2, 4)

    # Test Guest
    # def test_set_paid_guest_arrived(self):
    #     self.guest_2.set_arrived()
    #     self.assertTrue(self.guest_2.arrived)

    # def test_set_unpaid_guest_arrived_does_not_work(self):
    #     self.guest_1.set_arrived()
    #     self.assertFalse(self.guest_1.arrived)

    def test_guest_str(self):
        self.assertEqual(str(self.guest_1), 'Stephen Hawking')

    def test_set_paid(self):
        self.guest_1.set_paid()
        self.assertTrue(self.guest_1.paid)

    # Test Project
    def test_project_str(self):
        self.assertEqual(str(self.project_1), 'forthcoming event')

    def test_project_is_over(self):
        self.assertFalse(self.project_1.is_over())
        self.assertTrue(self.project_2.is_over())

    def test_project_howto_revealing(self):
        self.assertFalse(self.project_1.is_it_time_to_reveal_howto())
        self.assertTrue(self.project_2.is_it_time_to_reveal_howto())
        self.assertTrue(self.project_3.is_it_time_to_reveal_howto())

    def test_days_to_event(self):
        self.assertEqual(self.project_1.days_to_event(), 4)

    def test_brief_content_autofill(self):
        self.project_1.clean()
        self.project_2.clean()
        self.project_3.clean()
        self.assertEqual(len(self.project_1.content_brief), 0)
        self.assertEqual(len(self.project_2.content_brief), 200)
        self.assertEqual(len(self.project_3.content_brief), 50)

    def test_project_has_vacant_places(self):
        self.guest_1.set_paid()
        self.assertFalse(self.project_1.has_vacant())
        self.assertTrue(self.project_2.has_vacant())
        self.assertFalse(self.project_3.has_vacant())

    # Test TeamMate
    def test_teammate_str(self):
        self.member_1 = TeamMate.objects.create(name='Gor')
        self.member_1.save()
        self.assertEqual(str(self.member_1), 'Gor')

    # Test Documents
    # def test_document_clean_str(self):
        # with NamedTemporaryFile() as temp:
        #     file = files.File(temp, name='my_file.pdf')
        #     self.simple_doc_1 = Document.objects.language('en').create(file=file, image=file)
        #     self.simple_doc_1.set_current_language('ru')
        #
        #     post_save.disconnect(set_doc_image, sender=Document)
        #     self.simple_doc_1.save()
        #     self.assertEqual(str(self.simple_doc_1), 'my_file.pdf')
        #     post_save.connect(set_doc_image, sender=Document)

    # Test Donation
    def test_get_donation(self):
        self.assertEqual(self.don_button_1.get_hash(), calculate_signature('', 20, ''))

    def test_donation_str(self):
        self.assertEqual(str(self.don_button_1), '20')

    # Test Carousel
    def test_carousel_str(self):
        self.carousel_1 = Carousel.objects.create(display_name='I am a carousel')
        self.assertEqual(str(self.carousel_1), 'I am a carousel')


def tearDownModule():
    print("\nDeleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass