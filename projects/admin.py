from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin, SortedRelatedFieldListFilter

from Krone.settings import BASE_DIR
from projects.models import Project, Guest, TeamMate, Document, Carousel, DonateButton, AboutUs

admin.site.unregister(Group)
admin.site.site_title = _('Админ-панель НКО "Крона"')
admin.site.site_header = _('Админ-панель НКО "Крона"')


@admin.action(description=_('Сделать карусель'))
def make_carousel(self, request, queryset):
    for obj in queryset:
        new_obj = Carousel.objects.create(display_name='', background_image=b'', content='')
        obj.set_current_language('ru')
        new_obj.set_current_language('ru')
        new_obj.display_name = obj.name
        new_obj.background_image = obj.photo
        new_obj.content = obj.content
        obj.set_current_language('en')
        new_obj.set_current_language('en')
        new_obj.display_name = obj.name
        new_obj.background_image = obj.photo
        new_obj.content = obj.content
        new_obj.save()


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'date', 'total_places',)
    list_display_links = ('name',)
    list_filter = ('date',)
    fields = ('name', 'content', 'content_brief', 'howto',
              'total_places', 'date', 'price', 'qr_reveal_date', 'slug', 'photo', 'show_on_main'
              )
    actions = [make_carousel]

    def get_prepopulated_fields(self, request, obj=None):
        # can't use `prepopulated_fields = ..` because it breaks the admin validation
        # for translated fields. This is the official django-parler workaround.
        return {
            'slug': ('name',)
        }


@admin.register(TeamMate)
class TeamMateAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'high_rank', 'show')
    list_display_links = ('name',)
    list_filter = ('high_rank', 'show')


@admin.register(Document)
class SimpleDocumentAdmin(TranslatableAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    # list_filter = (('name', SortedRelatedFieldListFilter),)


@admin.register(Carousel)
class CarouselAdmin(TranslatableAdmin):
    list_display = ('id', 'display_name')
    list_display_links = ('display_name',)
    list_filter = (
        # ('translations__display_name', SortedRelatedFieldListFilter),
        # 'position',
    )

    change_list_template = str(BASE_DIR) + '/templates/admin/change_list_carousel.html'
    change_form_template = str(BASE_DIR) + '/templates/admin/change_form_carousel.html'


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
class AboutUsAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'text')
    list_display_links = ('name',)
    list_filter = ('id',)


# admin.site.register(Project, ProjectAdmin)
# admin.site.register(TeamMate, TeamMateAdmin)
# admin.site.register(SimpleDocument, SimpleDocumentAdmin)
# admin.site.register(ReportDocument, ReportDocumentAdmin)
# admin.site.register(Carousel, ProjectAdmin)
# admin.site.register(Guest, GuestAdmin)
# admin.site.register(DonateButton, DonateButtonAdmin)
# admin.site.register(AboutUs, AboutUsAdmin)
