import datetime
import os
import random
from io import BytesIO

import qrcode
from ckeditor.fields import RichTextField
from django.core.files import File
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.fields import TranslatedField
from parler.models import TranslatedFields, TranslatableModel
from phonenumber_field.modelfields import PhoneNumberField

from projects.utils import get_uuid_id, COLORS, get_day_word, calculate_signature


class Project(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name='Название'),
        content_brief=RichTextField(blank=True, verbose_name='Контент кратко'),
        content=RichTextField(blank=True, verbose_name='Контент'),
        howto=models.TextField(max_length=200, verbose_name='Как добраться'),
    )
    price = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Стоимость входа')
    date = models.DateTimeField(verbose_name='Дата проведения')
    total_places = models.PositiveIntegerField(verbose_name='Количество мест')
    qr_reveal_date = models.DateField(verbose_name='Дата, когда откроется qr-код')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=None)
    photo = models.ImageField(blank=True, verbose_name='Фото')
    back_photo = models.ImageField(blank=True, verbose_name='ФотоПозади')
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
        return (self.date - datetime.datetime.now()).days < -1

    def is_it_time_to_reveal_howto(self):
        return datetime.date.today() >= self.qr_reveal_date

    def days_to_event(self):
        return (self.date - datetime.datetime.now()).days
        # days = (self.date - datetime.datetime.now()).days
        # return _(f'До мероприятия осталось: {days} {get_day_word(days)}')
        # YAGNI

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

    @staticmethod
    def make_carousel(instance):
        new_obj = Carousel.objects.create(display_name='', background_image=b'', content='')
        instance.set_current_language('ru')
        new_obj.set_current_language('ru')
        new_obj.display_name = instance.name
        new_obj.background_image = instance.photo
        new_obj.content = instance.content
        instance.set_current_language('en')
        new_obj.set_current_language('en')
        new_obj.display_name = instance.name
        new_obj.background_image = instance.photo
        new_obj.content = instance.content
        new_obj.save()


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
    email = models.EmailField(verbose_name='Электронная почта')
    telegram = models.CharField(max_length=30, verbose_name='Телеграм')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект')
    ticket_uid = models.CharField(default=get_uuid_id, verbose_name='UID билета',
                                  max_length=40, unique=True)
    qr = models.ImageField(blank=True, editable=False)
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
    avatar = models.ImageField(blank=True, verbose_name='Фото')
    show = models.BooleanField(default=True, verbose_name='Отображать на сайте')
    telegram = models.CharField(max_length=100, verbose_name='Телеграм', default='@telegram')

    # django_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Член команды'
        verbose_name_plural = 'Команда'


class Document(models.Model):
    name = TranslatedField()
    file = models.FileField(verbose_name='Файл')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    def clean(self):
        if not self.name:
            self.name_ru = self.file.url.split('/')[-1]

    def get_absolute_url(self):
        return reverse('display_document', kwargs={'pk': self.id})

    def download(self):
        pass


class SimpleDocument(Document, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=True, verbose_name='Название'),
    )

    def download(self):
        return reverse('download_file', kwargs={'pk': self.id, 'file_type': 'document'})

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class ReportDocument(Document, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=True, verbose_name='Название'),
    )

    def download(self):
        return reverse('download_file', kwargs={'pk': self.id, 'file_type': 'report'})

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'


class Carousel(TranslatableModel):
    translations = TranslatedFields(
        display_name=models.CharField(max_length=100, verbose_name='Наименование', default=_('Некоторое')),
        content=RichTextField(verbose_name='Контент', null=True, default=_('')),
    )
    background_image = models.ImageField(verbose_name='Картинка фона', null=True)
    img_offset_x = models.FloatField(verbose_name='Смещение картинки x', default=0.0)
    img_offset_y = models.FloatField(verbose_name='Смещение картинки y', default=0.0)
    img_scale = models.FloatField(verbose_name='Масштаб картинки', default=0.0)
    collapsed_content = models.CharField(max_length=100, verbose_name='Контент для свёрнутого представления', null=True)
    position = models.IntegerField(default=0, verbose_name='Позиция в карусели (0 - не отображать)')

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

