import mimetypes

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.edit import FormMixin
from phonenumber_field.formfields import PhoneNumberField
from dotenv import load_dotenv

from projects.forms import AddGuestForm
from projects.models import Project, SimpleDocument, ReportDocument, Carousel, TeamMate, Guest, DonateButton

load_dotenv()


def guest_list(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    list_of_guests = project.guest_set.all()
    context = {
        'project': project,
        'list_of_guests': list_of_guests,
        'title': _('Список гостей')
    }
    return render(request, 'projects/how_to_page.html', context)


def service_page(request, project_slug):

    return render(request, 'projects/service_page.html')

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
            return redirect('payment_success', new_guest.ticket_uid)
    else:
        form = AddGuestForm()
    context['form'] = form
    return render(request, 'projects/guest-registration.html', context)


def payment_success(request, ticket_uid):
    guest = Guest.objects.get(ticket_uid=ticket_uid)
    context = {'guest': guest,
               'title': _('Успешная оплата')}
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


# class ShowSimpleDocument(DetailView):
#     model = SimpleDocument
#     template_name = 'projects/simple_document.html'
#     context_object_name = 'document'
#
#
# class ShowReportDocument(DetailView):
#     model = ReportDocument
#     template_name = 'projects/report_document.html'
#     context_object_name = 'document'


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
    print(donation_options)
    context = {
        'donations': donation_options,
        'title': _('Донат'),
    }
    return render(request, 'projects/donate.html', context)


def sitemap(request):
    return render(request, 'projects/sitemap.html', {'title': _('Карта сайта')})


def download_file(request, file_type, pk):
    document = None
    if file_type == 'report':
        document = get_object_or_404(ReportDocument, pk=pk)
    elif file_type == 'document':
        document = get_object_or_404(SimpleDocument, pk=pk)

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
    return HttpResponseNotFound(_('<h1>Страница не найдена</h1>'))


def display_document(request, pk):
    document = get_object_or_404(ReportDocument, pk=pk)
    context = {
        'document': document,
        'title': f'{document.name}',
    }
    return render(request, 'projects/display_document.html', context)
