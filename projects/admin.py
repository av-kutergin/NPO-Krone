from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

from projects.models import Project, Guest, TeamMate, SimpleDocument, ReportDocument, Carousel, DonateButton, AboutUs

admin.site.unregister(Group)
admin.site.site_title = _('Админ-панель НКО "Крона"')
admin.site.site_header = _('Админ-панель НКО "Крона"')


@admin.action(description='Sdelat carousel')
def make_carousel(self, request, queryset):
    for obj in queryset:
        Carousel.objects.create(display_name=obj.name, background_image=obj.photo, content=obj.content)


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'date', 'total_places',)
    list_display_links = ('name',)
    list_filter = ('date',)
    actions = [make_carousel]

    # def generate_carousel_item(self, obj):
    #     return mark_safe(f'<div class="button" onclick="{obj.create_carousel}">Sozdat</div>')


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
    list_filter = ('show',)


@admin.register(AboutUs)
class DonateButtonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text')
    list_display_links = ('name',)
    list_filter = ('id',)
