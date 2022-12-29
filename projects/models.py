import datetime
import os
import random
import shutil
from io import BytesIO

import qrcode
from ckeditor.fields import RichTextField
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields, TranslatableModel
from phonenumber_field.modelfields import PhoneNumberField

from Krone.settings import MEDIA_ROOT
from projects.utils import get_uuid_id, COLORS, calculate_signature, pdf2png, strfdelta


class Project(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name=_('Название')),
        content=RichTextField(blank=True, verbose_name=_('Контент')),
        content_brief=models.TextField(max_length=200, blank=True, verbose_name=_('Контент кратко')),
        summary=models.CharField(max_length=50, blank=True, verbose_name=_('В двух словах')),
        howto=models.TextField(max_length=200, verbose_name=_('Как добраться')),
    )
    price = models.DecimalField(max_digits=5, decimal_places=0, verbose_name=_('Стоимость входа'))
    date = models.DateTimeField(verbose_name=_('Дата проведения'))
    total_places = models.PositiveIntegerField(verbose_name=_('Количество мест'))
    qr_reveal_date = models.DateField(verbose_name=_('Дата, когда откроется qr-код'))
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=None)
    photo = models.ImageField(blank=True, verbose_name=_('Фото'), upload_to='projects_photos/%Y/')
    show_on_main = models.BooleanField(default=False, verbose_name=_('Отображать на главной странице'))
    # vacant_places = models.PositiveIntegerField(verbose_name='Количество свободных мест', editable=False, blank=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_project', kwargs={'project_slug': self.slug})

    # def is_future_event(self):
    #     return self.date > datetime.date.today()

    def is_over(self):
        result = (self.date - datetime.datetime.now()).days < -1
        return result

    def is_it_time_to_reveal_howto(self):
        return datetime.date.today() >= self.qr_reveal_date

    def time_before_reveal(self):
        return strfdelta(datetime.datetime.combine(self.qr_reveal_date, datetime.datetime.min.time()) - datetime.datetime.now(), "%D дней %H часов и %M минут")

    def has_vacant(self):
        return int(self.total_places) - len(self.guest_set.all().filter(paid=True))

    def clean(self):
        if not self.content_brief:
            if not self.content:
                pass
            elif len(self.content) < 200:
                self.content_brief = self.content
            else:
                self.content_brief = self.content[:200]

    # @staticmethod
    # def make_carousel_from_project(project=None):
    #     new_cariousel = Carousel.objects.create(display_name='', background_image=b'', content='')
    #     for lang in ['ru', 'en']:
    #         project.set_current_language(lang)
    #         new_cariousel.set_current_language(lang)
    #         new_cariousel.display_name = project.name
    #         new_cariousel.background_image = project.photo
    #         new_cariousel.content = project.summary
    #         new_cariousel.project = project
    #     new_cariousel.save()
    #
    # @staticmethod
    # def make_carousel_default(project=None):
    #     new_cariousel = Carousel.objects.create(display_name='', background_image=b'', content='')
    #     new_cariousel.set_current_language('ru')
    #     new_cariousel.display_name = 'DefaultRu'
    #     new_cariousel.background_image = b''
    #     new_cariousel.content = 'DefaultRu'
    #     new_cariousel.set_current_language('en')
    #     new_cariousel.display_name = 'DefaultEn'
    #     new_cariousel.background_image = b''
    #     new_cariousel.content = 'DefaultEn'
    #     new_cariousel.save()


    # IF NEEDED
    #
    # PASSPHRASE_CHOICES = [
    #     ('NO', 'не использовать'),
    #     ('ONE', 'общее слово для всех'),
    #     ('MANY', 'личное слово'),
    # ]
    # passphrase_needed = models.CharField(max_length=4, choices=PASSPHRASE_CHOICES, default='NO')
    # passphrases = models.JSONField(default=dict)


class Guest(models.Model):
    firstname = models.CharField(max_length=100, verbose_name='Имя')
    lastname = models.CharField(max_length=100, verbose_name='Фамилия')
    birthdate = models.DateField(verbose_name='Дата рождения')
    phone = PhoneNumberField(verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Электронная почта')
    telegram = models.CharField(blank=True, max_length=30, verbose_name='Телеграм')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект')
    ticket_uid = models.CharField(default=get_uuid_id, verbose_name='UID билета',
                                  max_length=40, unique=True)
    qr = models.ImageField(blank=True, editable=False, upload_to='guest_QRs/%Y/')
    arrived = models.BooleanField(default=False, verbose_name='Пришёл')
    paid = models.BooleanField(default=False, verbose_name='Оплачено', editable=False)

    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    # def set_arrived(self):
    #     if self.paid:
    #         self.arrived = True
    #         self.save(update_fields=['arrived'])
    #     return self

    def set_paid(self):
        self.paid = True
        self.save(update_fields=['paid'])
        return self

    def download_qr_image(self):
        return reverse('download_file', kwargs={'pk': self.id, 'file_type': 'qr_image'})


class TeamMate(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name='Имя'),
        description=models.TextField(blank=True, verbose_name='Описание'),
    )
    high_rank = models.BooleanField(default=False, verbose_name='Верхнее звено')
    avatar = models.ImageField(blank=True, verbose_name='Фото', upload_to='team_avatars/')
    show = models.BooleanField(default=True, verbose_name='Отображать на сайте')
    telegram = models.CharField(blank=True, max_length=100, verbose_name='Телеграм')

    # django_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Член команды'
        verbose_name_plural = 'Команда'


class Document(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=True, verbose_name='Название', unique=True),
    )
    file = models.FileField(verbose_name='Файл', upload_to='documents/pdf/')
    image = models.FileField(verbose_name='рендер', blank=True, editable=False, upload_to='documents/png/')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name

    def download(self):
        return reverse('download_file', kwargs={'pk': self.id, 'file_type': 'document'})

    # def clean(self):
    #     for lang in ['en', 'ru']:
    #         self.set_current_language(lang)
    #         if not self.name:
    #             self.name = self.file.url.split('/')[-1]
    #             self.save()
    #             return
    #     return

    # def get_absolute_url(self):
    #     return reverse('display_document', kwargs={'pk': self.id})


class Carousel(TranslatableModel):
    POSITION = (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    translations = TranslatedFields(
        display_name=models.CharField(max_length=100, verbose_name='Наименование', default=_('Некоторое')),
        content=RichTextField(verbose_name='Контент', null=True, default=_('')),
    )
    background_image = models.ImageField(verbose_name='Картинка фона', null=True, upload_to='carousel/%Y/')
    img_offset_x = models.FloatField(verbose_name='Смещение картинки x', default=0.0)
    img_offset_y = models.FloatField(verbose_name='Смещение картинки y', default=0.0)
    img_scale = models.FloatField(verbose_name='Масштаб картинки', default=100.0)
    collapsed_content = models.CharField(max_length=100, verbose_name='Контент для свёрнутого представления', null=True)
    position = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Позиция в карусели (0 - не отображать)',
        choices=POSITION,
    )
    project = models.ForeignKey('Project', null=True, blank=True, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = 'Карусель'
        verbose_name_plural = 'Карусель'
        ordering = ['position']


class DonateButton(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Сумма')
    show = models.BooleanField(default=True, verbose_name='Отображать на сайте')

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = 'Донат'
        verbose_name_plural = 'Донаты'
        ordering = ['amount']

    def get_hash(self):
        merchant_login = os.environ['PAYMENT_LOGIN']
        merchant_password_1 = os.environ['PAYMENT_PASSWORD1']
        return calculate_signature(merchant_login, self.amount, merchant_password_1)


class AboutUs(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(verbose_name='Имя', max_length=255),
        text=RichTextField(verbose_name='Текст', blank=True)
    )
    #position = models.IntegerField(default=0, verbose_name='Позиция в карусели (0 - не отображать)')

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        ordering = ['id']


@receiver(post_save, sender=Guest)
def set_guest_qr(sender, instance, **kwargs):
    if not instance.qr:
        project = Project.objects.get(pk=instance.project_id)
        new_qr = qrcode.QRCode(version=1, box_size=10, border=5)
        project_slug = str(project.slug)
        ticket_uid = instance.ticket_uid
        data = f'https://npokrona.ru/how-to/{project_slug}/{ticket_uid}'
        new_qr.add_data(data)
        fill_color, back_color = random.choice(list(COLORS.items()))
        image = new_qr.make_image(fill_color=fill_color, back_color=back_color)
        blob = BytesIO()
        image.save(blob, 'PNG')
        instance.qr.save(f'{ticket_uid}.PNG', File(blob), save=False)

        post_save.disconnect(set_guest_qr, sender=Guest)
        instance.save()
        post_save.connect(set_guest_qr, sender=Guest)


@receiver(post_save, sender=Document)
def set_doc_image(sender, instance, **kwargs):
    instance.clean()
    if not instance.image:
        filepath = instance.file.path
        name = os.path.split(filepath)[-1]
        stream = pdf2png(instance)
        instance.image.save(f'{name}.png', ContentFile(stream), save=False)

        post_save.disconnect(set_doc_image, sender=Document)
        instance.save()
        post_save.connect(set_doc_image, sender=Document)
