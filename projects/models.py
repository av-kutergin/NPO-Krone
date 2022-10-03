import datetime

from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    content_brief = models.TextField(blank=True, verbose_name='Контент кратко')
    content = models.TextField(blank=True, verbose_name='Контент')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость входа')
    date = models.DateField(verbose_name='Дата проведения')
    total_places = models.PositiveIntegerField(verbose_name='Общее количество мест')
    vacant_places = models.PositiveIntegerField(verbose_name='Количество свободных мест')
    qr_reveal_date = models.DateField(verbose_name='Дата, когда откроется qr-код')
    howto = models.CharField(max_length=200, verbose_name='Как добраться')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=None)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-date']

    def __str__(self):
        return self.name

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    ticket_uid = models.CharField(max_length=50, verbose_name='UID билета')
    arrived = models.BooleanField(verbose_name='Пришёл')

    def __str__(self):
        return self.firstname, self.lastname

    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'


class TeamMate(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(blank=True, verbose_name='Описание')
    high_rank = models.BooleanField(verbose_name='Верхнее звено')
    avatar = models.ImageField(blank=True, verbose_name='Фото')
    show = models.BooleanField(default=True, verbose_name='Отображать на сайте')
    # django_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Член команды'
        verbose_name_plural = 'Команда'


class Document(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name='Название')
    file = models.FileField(verbose_name='Файл')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    def clean(self):
        if not self.name:
            self.name_ru = self.file.url.split('/')[-1]

    def get_absolute_url(self):
        return reverse('display', kwargs={'pk': self.id})

    def download(self):
        pass


class SimpleDocument(Document):
    def __str__(self):
        return self.name

    def download(self):
        return reverse('download_file', kwargs={'pk': self.id, 'file_type': 'document'})

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class ReportDocument(Document):
    def __str__(self):
        return self.name

    def download(self):
        return reverse('download_file', kwargs={'pk': self.id, 'file_type': 'report'})

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'


class Carousel(models.Model):
    display_name = models.CharField(max_length=100, verbose_name='Наименование')
    background_image = models.ImageField(verbose_name='Картинка фона', blank=True)
    content = models.TextField(verbose_name='Контент', blank=True)
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
        return self.amount

    class Meta:
        verbose_name = 'Донат'
        verbose_name_plural = 'Донаты'
        ordering = ['amount']
