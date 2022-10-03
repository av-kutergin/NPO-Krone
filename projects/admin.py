from django.contrib import admin
from django.contrib.auth.models import Group
from modeltranslation.admin import TranslationAdmin

from .models import Project, Guest, TeamMate, SimpleDocument, ReportDocument, Carousel, DonateButton

admin.site.unregister(Group)


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'date', 'total_places', 'vacant_places')
    list_display_links = ('name',)
    list_filter = ('date',)


@admin.register(TeamMate)
class TeamMateAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'high_rank', 'show')
    list_display_links = ('name',)
    list_filter = ('name', 'high_rank', 'show')


@admin.register(SimpleDocument)
class SimpleDocumentAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    list_filter = ('name',)


@admin.register(ReportDocument)
class ReportDocumentAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    list_filter = ('name',)


@admin.register(Carousel)
class CarouselAdmin(TranslationAdmin):
    list_display = ('id', 'display_name')
    list_display_links = ('display_name',)
    list_filter = ('display_name', 'position')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'phone', 'email', 'telegram', 'project', 'arrived')
    list_display_links = ('firstname',)
    list_filter = ('project', 'arrived')


@admin.register(DonateButton)
class DonateButtonAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'show')
    list_display_links = ('amount',)
    list_filter = ('amount', 'show')
