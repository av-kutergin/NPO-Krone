import mimetypes
import os

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from dotenv import load_dotenv

from projects.forms import AddGuestForm
from projects.models import Project, Document, Carousel, TeamMate, Guest, DonateButton, AboutUs
from projects.utils import calculate_signature, parse_response, check_signature_result, generate_payment_link, \
    check_success_payment

load_dotenv()


def main_page(request):
    title = _('НКО Крона')
    projects_for_main = Project.objects.prefetch_related('translations').filter(show_on_main=True)
    carousel = Carousel.objects.prefetch_related('translations').all()
    teammates = TeamMate.objects.prefetch_related('translations').filter(show=True).filter(high_rank=True)
    about_us = AboutUs.objects.prefetch_related('translations').all()
    project_w_photo = None
    for proj in projects_for_main:
        if proj.photo:
            project_w_photo = proj
            break

    context = {
        'title': title,
        'carousel': carousel,
        'projects_for_main': projects_for_main,
        'teammates': teammates,
        'about_us': about_us,
        'project_w_photo': project_w_photo,
    }
    return render(request, 'projects/index.html', context)


def team(request):
    teammates = TeamMate.objects.prefetch_related('translations').filter(show=True)
    high_teammates = teammates.filter(high_rank=True)
    ordinary_teammates = teammates.filter(high_rank=False)
    context = {
        'high_teammates': high_teammates,
        'ordinary_teammates': ordinary_teammates,
        'title': _('Команда')
    }
    return render(request, 'projects/team.html', context)


def projects(request):
    all_projects = Project.objects.all()
    context = {
        'title': _('Проекты'),
        'all_projects': all_projects,
    }
    return render(request, 'projects/projects.html', context)


class ShowProject(DetailView):
    model = Project
    template_name = 'projects/project.html'
    slug_url_kwarg = 'project_slug'
    context_object_name = 'project'


def participate(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    context = {
        'event': project,
        'title': _('Регистрация на мероприятие')
    }
    if request.method == 'POST':
        form = AddGuestForm(request.POST)
        if form.is_valid():
            new_guest = form.save(commit=False)
            new_guest.project = project
            new_guest.save()
            context['guest'] = new_guest
            payment_link = generate_payment_link(
                cost=project.price,
                description=str(new_guest.ticket_uid),
            )
            return redirect(payment_link)
    else:
        form = AddGuestForm()
    context['form'] = form
    return render(request, 'projects/participate.html', context)


def payment_success(request):
    if check_success_payment(request):
        param_request = parse_response(request)
        description = param_request['description']
        if description != 'donation':
            guest = Guest.objects.get(ticket_uid=description)
            project = guest.project
            qr_link = f'https://npokrona.ru/how-to/{project.slug}/{guest.ticket_uid}'
            context = {
                'title': _('Успешная оплата'),
                'guest': guest,
                'qr_link': qr_link,
                }
        else:
            context = {'title': _('Успешная оплата'), }
        return render(request, 'projects/payment_success.html', context)
    else:
        context = {'title': _('Ошибка оплаты')}
        return render(request, 'projects/payment_error.html', context)


def payment_error(request):
    context = {'title': _('Ошибка оплаты')}
    return render(request, 'projects/payment_error.html', context)


def donate(request):
    donation_options = DonateButton.objects.all()
    context = {
        'donations': donation_options,
        'title': _('Донат'),
    }
    return render(request, 'projects/support.html', context)


class DocumentListView(ListView):
    model = Document
    template_name = 'projects/docs.html'

    def get_queryset(self):
        return [{"doc": x, "right_is_empty": i % 6 == 2, "left_is_empty": i % 6 == 3} for i, x in enumerate(super().get_queryset())]

    def get_context_data(self, *args, **kwargs):
        context = super(DocumentListView, self).get_context_data(*args, **kwargs)
        context['title'] = _('Документы')
        return context


####___________________________________####
# def sitemap(request):
#     return render(request, 'projects/sitemap.html', {'title': _('Карта сайта')})


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def download_file(request, file_type, pk):
    document = None
    guest = None
    if file_type == 'document':
        document = get_object_or_404(Document, pk=pk)
    elif file_type == 'qr_image':
        guest = get_object_or_404(Guest, pk=pk)

    if document:
        filepath = document.file.path
        mime_type, _ = mimetypes.guess_type(filepath)
        extension = mimetypes.guess_extension(filepath)
        name = filepath.split('/')[-1]
        with open(filepath, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename={name}'
            return response

    elif guest:
        filepath = guest.qr.path
        mime_type, _ = mimetypes.guess_type(filepath)
        extension = mimetypes.guess_extension(filepath)
        _, name = os.path.split(filepath)
        with open(filepath, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename={name}'
            return response


def how_to_view(request, project_slug, ticket_uid):
    guest = Guest.objects.select_related('project').get(ticket_uid=ticket_uid)
    project = guest.project
    if not request.user.is_authenticated:
        context = {
            'project': project,
            'guest': guest,
            'title': _('Инструкция'),
        }
        return render(request, 'projects/how_to_page.html', context)
    else:
        return redirect('service_page', project_slug=project_slug, ticket_uid=ticket_uid)


@login_required()
def set_arrived(request, ticket_uid):
    guest = Guest.objects.select_related('project').get(ticket_uid=ticket_uid)
    project = guest.project
    if guest.paid:
        guest.arrived = True
        guest.save(update_fields=['arrived'])
        messages.add_message(request, messages.INFO, f'Гость {guest} отмечен пришедшим.')
    return redirect('guest_list', project.slug)


@login_required()
def service_page(request, project_slug, ticket_uid):
    try:
        guest = Guest.objects.select_related('project').get(ticket_uid=ticket_uid)
        project = guest.project
        context = {
            'project': project,
            'guest': guest,
            'title': _('Сервис'),
            'flag': True
        }
        return render(request, 'projects/service_page.html', context)
    except ObjectDoesNotExist:
        context = {
            'title': _('Сервис'),
            'flag': False
        }
        return render(request, 'projects/service_page.html', context)


@login_required()
def guest_list(request, project_slug):
    project = Project.objects.prefetch_related('guest_set').get(slug=project_slug)
    list_of_guests = project.guest_set.all()
    context = {
        'project': project,
        'list_of_guests': list_of_guests,
        'title': _('Список гостей')
    }
    return render(request, 'projects/guest_list.html', context)


# Получение уведомления об исполнении операции (ResultURL).

def result_payment(request: str) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    merchant_password_2 = os.environ['PAYMENT_PASSWORD2']
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']
    description = param_request['description']

    signature = calculate_signature(cost, number, signature)

    if check_signature_result(number, cost, signature, merchant_password_2):
        if description != 'donation':
            guest = Guest.objects.get(ticket_uid=description)
            guest.set_paid()
        return f'OK{number}'
    return "bad sign"


def projects_list(request):
    list_of_p = Project.objects.all()
    context = {
        'list_of_p': list_of_p,
        'title': _('Список проектов')
    }
    return render(request, 'projects/p_list.html', context)


def make_carousel_from_project(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    new_carousel = Carousel.objects.create(display_name='', background_image=b'', content='')
    for lang in ['ru', 'en']:
        project.set_current_language(lang)
        new_carousel.set_current_language(lang)
        new_carousel.display_name = project.name
        new_carousel.background_image = project.photo
        new_carousel.content = project.summary
        new_carousel.project = project
    new_carousel.save()
    return HttpResponseRedirect(reverse('admin:projects_carousel_change', args=(new_carousel.pk,)))


def make_carousel_default(request):
    new_carousel = Carousel.objects.create(display_name='', background_image='carousel/2022/p-2.jpg', content='')

    new_carousel.set_current_language('ru')
    new_carousel.display_name = 'Наша задача'
    new_carousel.collapsed_content = 'НКО «Крона»'
    new_carousel.content = 'Мы объединяем людей и помогаем в реализации их инициатив, затрагиявая социально значимые вопросы, используя методы игрофикации и развлекательный контент'
    new_carousel.img_offset_x = 110
    new_carousel.save()
    new_carousel.set_current_language('en')
    new_carousel.display_name = 'Our mission'
    new_carousel.collapsed_content = 'Krone'
    new_carousel.content = '...'
    new_carousel.save()
    return redirect(reverse('admin:projects_carousel_change', args=(new_carousel.pk,)))
