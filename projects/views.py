from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from projects.forms import AddGuestForm

menu = ['about', 'contacts', 'upcoming events']


class AddGuestView(CreateView):
    form_class = AddGuestForm
    template_name = 'projects/guest-registration.html'
    success_url = reverse_lazy('main_page')
    raise_exception = True


def main_page(request):
    return render(request, 'projects/index.html', {'menu': menu, 'title': 'Main page'})


