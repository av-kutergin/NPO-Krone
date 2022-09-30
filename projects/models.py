import datetime

from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Project(models.Model):
    name_ru = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    content_brief_ru = models.TextField(blank=True)
    content_brief_en = models.TextField(blank=True)
    content_ru = models.TextField(blank=True)
    content_en = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    total_places = models.PositiveIntegerField()
    vacant_places = models.PositiveIntegerField()
    qr_reveal_date = models.DateField()
    howto_ru = models.CharField(max_length=200)
    howto_en = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=None)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('show_project', kwargs={'project_slug': self.slug})

    def is_coming(self):
        return datetime.date.today() < self.date

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ticket_uid = models.CharField(max_length=50)
    arrived = models.BooleanField()


class TeamMate(models.Model):
    name_ru = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    high_rank = models.BooleanField()
    avatar = models.ImageField(blank=True)
    show = models.BooleanField(default=True)
    # django_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)


class Document(models.Model):
    name_ru = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    file = models.FileField()
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=None)

    class Meta:
        abstract = True

    def clean(self):
        if not self.name_ru:
            self.name_ru = self.file.url.split('/')[-1]
        if not self.name_en:
            self.name_en = self.file.url.split('/')[-1]

    def get_absolute_url(self):
        return reverse('display', kwargs={'pk': self.id})

    def download(self):
        pass


class SimpleDocument(Document):
    def download(self):
        return reverse('download_file', kwargs={'pk': self.id, 'file_type': 'document'})


class ReportDocument(Document):
    def download(self):
        return reverse('download_file', kwargs={'pk': self.id, 'file_type': 'report'})


class Carousel(models.Model):
    display_name_ru = models.CharField(max_length=100)
    display_name_en = models.CharField(max_length=100)
    background_image_ru = models.ImageField()
    background_image_en = models.ImageField()
    content_ru = models.TextField()
    content_en = models.TextField()
