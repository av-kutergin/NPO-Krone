import mimetypes
import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from dotenv import load_dotenv

from projects.forms import AddGuestForm
from projects.models import Project, SimpleDocument, ReportDocument, Carousel, TeamMate, Guest, DonateButton
from projects.utils import calculate_signature, parse_response, check_signature_result, generate_payment_link, check_success_payment

load_dotenv()


def set_arrived(request, ticket_uid):
    guest = Guest.objects.get(ticket_uid=ticket_uid)
    project = guest.project
    guest.set_arrived()
    return redirect('guest_list', project.slug)


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
    else:
        form = AuthenticationForm()
    return render(request, 'projects/login.html', {'form': form})


@login_required()
def guest_list(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    list_of_guests = project.guest_set.all()
    context = {
        'project': project,
        'list_of_guests': list_of_guests,
        'title': _('Список гостей')
    }
    return render(request, 'projects/guest_list.html', context)


@login_required()
def service_page(request, project_slug, ticket_uid):
    try:
        project = Project.objects.get(slug=project_slug)
        guest = Guest.objects.get(ticket_uid=ticket_uid)
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


def how_to_view(request, project_slug, ticket_uid):
    project = Project.objects.get(slug=project_slug)
    guest = Guest.objects.get(ticket_uid=ticket_uid)
    context = {
        'project': project,
        'guest': guest,
        'title': _('Как нас найти'),
    }
    return render(request, 'projects/how_to_page.html', context)


def add_guest(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    context = {'event': project,
               'title': _('Регистрация на мероприятие')}
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
            # return redirect('payment_success', new_guest.ticket_uid)
    else:
        form = AddGuestForm()
    context['form'] = form
    return render(request, 'projects/guest-registration.html', context)


def payment_success(request):
    if check_success_payment(request):
        param_request = parse_response(request)
        description = param_request['description']
        if description != 'donation':
            guest = Guest.objects.get(ticket_uid=description)
            # project = guest.project
            # image_data = bytes(guest.qr.read())
            # message_text = _(f'''К сообщению прикреплён Ваш QR для входа на мероприятие: {project.name}
            # За сутки до мероприятия на странице, на которую ведёт Ваш QR, появится подробная интрукция о том, как нас найти.
            # ''')
            # message = EmailMessage(
            #     _(f'Ваш QR для входа на мероприятие: {project.name}'),
            #     message_text,
            #     os.environ['EMAIL_HOST_USER'],
            #     [guest.email]
            # )
            # message.attach(guest.qr.name, image_data, 'image/png')
            # message.send()

            context = {
                'title': _('Успешная оплата'),
                'guest': guest,
                }
            return render(request, 'projects/payment-succeed-qr.html', context)

        else:
            context = {'title': _('Успешная оплата'), }
            return render(request, 'projects/payment-succeed-qr.html', context)


def main_page(request):
    title = _('НКО Крона')
    projects = Project.objects.all()
    carousel = Carousel.objects.all()
    teammates = TeamMate.objects.filter(show=True).filter(high_rank=True)
    context = {
        'title': title,
        'carousel': carousel,
        'projects': projects,
        'teammates': teammates,
    }
    return render(request, 'projects/index.html', context)


class ShowProject(DetailView):
    model = Project
    template_name = 'projects/project_page.html'
    slug_url_kwarg = 'project_slug'
    context_object_name = 'project'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProject, self).get_context_data(*args, **kwargs)
        slug = self.kwargs['project_slug']
        project = Project.objects.get(slug=slug)
        context['title'] = project.name
        return context


def team(request):
    high_teammates = TeamMate.objects.filter(show=True).filter(high_rank=True)
    ordinary_teammates = TeamMate.objects.filter(show=True).filter(high_rank=False)
    context = {
        'high_teammates': high_teammates,
        'ordinary_teammates': ordinary_teammates,
        'title': _('Команда')
    }
    return render(request, 'projects/team.html', context)


class DocumentListView(ListView):
    model = SimpleDocument
    template_name = 'projects/documents.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DocumentListView, self).get_context_data(*args, **kwargs)
        context['title'] = _('Документы')
        return context


class ReportListView(ListView):
    model = ReportDocument
    template_name = 'projects/reports.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ReportListView, self).get_context_data(*args, **kwargs)
        context['title'] = _('Отчёты')
        return context


def projects(request):
    projects = Project.objects.all()
    context = {
        'title': _('Проекты'),
        'projects': projects,
    }
    return render(request, 'projects/projects.html', context)


def contacts(request):
    return render(request, 'projects/contacts.html', {'title': _('Контакты')})


def donate(request):
    donation_options = DonateButton.objects.all()
    context = {
        'donations': donation_options,
        'title': _('Донат'),
    }
    return render(request, 'projects/donate.html', context)


def sitemap(request):
    return render(request, 'projects/sitemap.html', {'title': _('Карта сайта')})


def download_file(request, file_type, pk):
    document = None
    guest = None
    if file_type == 'report':
        document = get_object_or_404(ReportDocument, pk=pk)
    elif file_type == 'document':
        document = get_object_or_404(SimpleDocument, pk=pk)
    elif file_type == 'qr_image':
        guest = get_object_or_404(Guest, pk=pk)

    if document:
        filepath = document.file.path
        mime_type, _ = mimetypes.guess_type(filepath)
        extension = mimetypes.guess_extension(filepath)
        name = filepath.split('/')[-1]
        print(name)
        with open(filepath, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename={name}'
            return response

    elif guest:
        filepath = guest.qr.path
        mime_type, _ = mimetypes.guess_type(filepath)
        extension = mimetypes.guess_extension(filepath)
        name = filepath.split('/')[-1]
        print(name)
        with open(filepath, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename={name}'
            return response

    return HttpResponseNotFound(_('<h1>Страница не найдена</h1>'))


def display_document(request, pk):
    document = get_object_or_404(ReportDocument, pk=pk)
    merchant_login = os.environ['PAYMENT_LOGIN']
    context = {
        'merchant_login': merchant_login,
        'document': document,
        'title': f'{document.name}',
    }
    return render(request, 'projects/display_document.html', context)


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
