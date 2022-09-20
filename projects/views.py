from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView

from projects.forms import AddGuestForm
from projects.models import Guest

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
    return render(request, 'projects/index.html', {'menu': menu, 'title': 'Main page'})


def team(request):
    return render(request, 'projects/team.html')


def documents(request):
    return render(request, 'projects/documents.html')


def reports(request):
    return render(request, 'projects/reports.html')


def projects(request):
    return render(request, 'projects/projects.html')


def contacts(request):
    return render(request, 'projects/contacts.html')


def donate(request):
    return render(request, 'projects/donate.html')


def sitemap(request):
    return render(request, 'projects/sitemap.html')
