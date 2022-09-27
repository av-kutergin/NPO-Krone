from django.contrib import admin

from .models import Project, Guest, TeamMate, SimpleDocument, ReportDocument, Carousel


admin.site.register(Project)
admin.site.register(Guest)
admin.site.register(TeamMate)
admin.site.register(SimpleDocument)
admin.site.register(ReportDocument)
admin.site.register(Carousel)
