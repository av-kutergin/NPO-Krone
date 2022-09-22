from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, TemplateView, DetailView

from projects.forms import AddGuestForm
from projects.models import Guest, Project, SimpleDocument, ReportDocument, Carousel

menu = ['about', 'contacts', 'upcoming events']


class AddGuestView(FormView):
    form_class = AddGuestForm
    template_name = 'projects/guest-registration.html'
    success_url = reverse_lazy('main_page')
    raise_exception = True


class GuestList(ListView):
    template_name = 'projects/guest-list.html'
    # queryset = Guest.objects.filter(project=project)


def main_page(request):
    title = 'Krone'
    projects = Project.objects.all()
    carousel = Carousel.objects.all()
    context = {
        'title': title,
        'carousel': carousel,
        'projects': projects,

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
    return render(request, 'projects/team.html')


class DocumentListView(ListView):
    model = SimpleDocument
    template_name = 'projects/documents.html'


class ReportListView(ListView):
    model = ReportDocument
    template_name = 'projects/reports.html'


def projects(request):
    return render(request, 'projects/projects.html')


def contacts(request):
    return render(request, 'projects/contacts.html')


def donate(request):
    return render(request, 'projects/donate.html')


def sitemap(request):
    return render(request, 'projects/sitemap.html')
