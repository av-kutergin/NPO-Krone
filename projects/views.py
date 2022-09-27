import mimetypes

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView

from projects.forms import AddGuestForm
from projects.models import Project, SimpleDocument, ReportDocument, Carousel, TeamMate

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
    teammates = TeamMate.objects.filter(show=True).filter(high_rank=True)
    context = {
        'title': title,
        'carousel': carousel,
        'projects': projects,
        'teammates': teammates

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
    print(high_teammates[0].avatar.path)
    return render(request, 'projects/team.html', context)


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


# def download_document(request, pk):
#     document = get_object_or_404(SimpleDocument, pk=pk)
#     filepath = document.file.path
#     mime_type, _ = mimetypes.guess_type(filepath)
#     with open(filepath, 'rb') as file:
#         response = HttpResponse(file.read(), content_type=mime_type)  # mimetypes.guess_type(filepath)
#         response['Content-Disposition'] = f'attachment;filename={document.name_ru}'
#         return response


# def download_report(request, pk, obj):
#     document = get_object_or_404(ReportDocument, pk=pk)
#     filepath = document.file.path
#     mime_type, _ = mimetypes.guess_type(filepath)
#     with open(filepath, 'rb') as file:
#         response = HttpResponse(file.read(), content_type=mime_type)
#         response['Content-Disposition'] = f'attachment; filename={document.name_ru}'
#         return response


def display(request, file_type, pk):
    # document = None
    # if file_type == 'report':
    document = get_object_or_404(ReportDocument, pk=pk)
    # elif file_type == 'document':
    #     document = get_object_or_404(SimpleDocument, pk=pk)

    if document:
        # filepath = document.file.path
        # mime_type, _ = mimetypes.guess_type(filepath)
        # context = {
        #     'document': document,
        #     'type': mime_type,
        # }
        return render(request, 'projects/display.html', document)

    # report = get_object_or_404(ReportDocument, pk=pk)
    # filepath = report.file.path
    # mime_type, _ = mimetypes.guess_type(filepath)
    # # if filepath.endswith('pdf'):
    # with open(filepath, 'rb') as file:
    #     response = HttpResponse(file.read(), content_type=mime_type)
    #     response['Content-Disposition'] = f'inline;filename={report.name_ru}'
    #     return response
    # else:
    #     raise TypeError
