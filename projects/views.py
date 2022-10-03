import mimetypes

import stripe
from django import forms
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView, DetailView
from phonenumber_field.formfields import PhoneNumberField
from dotenv import load_dotenv

from projects.forms import AddGuestForm
from projects.models import Project, SimpleDocument, ReportDocument, Carousel, TeamMate, Guest, DonateButton

load_dotenv()

YOUR_DOMAIN = 'http://127.0.0.1:8000/'


class AddGuestView(FormView):
    form_class = AddGuestForm
    template_name = 'projects/guest-registration.html'
    # success_url = reverse_lazy('main_page')
    # raise_exception = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['project_slug']
        context["event"] = Project.objects.get(slug=slug)
        return context


class GuestList(ListView):
    template_name = 'projects/guest-list.html'
    # queryset = Guest.objects.filter(project=project)


def main_page(request):
    title = 'Krone'
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
    }
    return render(request, 'projects/team.html', context)


class DocumentListView(ListView):
    model = SimpleDocument
    template_name = 'projects/documents.html'


class ReportListView(ListView):
    model = ReportDocument
    template_name = 'projects/reports.html'


def projects(request):
    projects = Project.objects.all()
    context = {
        'title': 'Projecti',
        'projects': projects,
    }
    return render(request, 'projects/projects.html', context)


def contacts(request):
    return render(request, 'projects/contacts.html')


def donate(request):
    donation_options = DonateButton.objects.all()
    print(donation_options)
    context = {
        'donations': donation_options
    }
    return render(request, 'projects/donate.html', context)


def create_checkout_session(request, ):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


def sitemap(request):
    return render(request, 'projects/sitemap.html')


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
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def display(request, pk):
    document = get_object_or_404(ReportDocument, pk=pk)
    context = {
        'document': document,
    }
    return render(request, 'projects/display.html', context)
