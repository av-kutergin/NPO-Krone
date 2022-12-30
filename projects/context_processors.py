from datetime import datetime

from projects.models import Project


def get_projects(request):
    all_projects = Project.objects.all()
    not_over = [i for i in all_projects if i.date > datetime.now()]
    return {
        'not_over': not_over,
    }
