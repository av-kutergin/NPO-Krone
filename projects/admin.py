from django.contrib import admin

from .models import Project, Guest, TeamMate


admin.site.register(Project)
admin.site.register(Guest)
admin.site.register(TeamMate)
