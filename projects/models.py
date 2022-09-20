from django.contrib.auth.models import User
from django.db import models
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
    django_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Document(models.Model):
    name_ru = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    file = models.FileField()

    def clean(self):
        if not self.name_ru:
            self.name_ru = self.file.url.split('/')[-1]
        if not self.name_en:
            self.name_en = self.file.url.split('/')[-1]

    class Meta:
        abstract = True


class SimpleDocument(Document):
    pass


class ReportDocument(Document):
    pass


