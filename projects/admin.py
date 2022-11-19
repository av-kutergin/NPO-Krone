from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin, SortedRelatedFieldListFilter

from projects.models import Project, Guest, TeamMate, SimpleDocument, ReportDocument, Carousel, DonateButton, AboutUs

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
              'total_places', 'date', 'qr_reveal_date', 'slug', 'photo', 'back_photo',
              )
    actions = [make_carousel]

    def get_queryset(self, request):
        qs = super().get_queryset(request).prefetch_related('translations')
        print(qs)
        return qs

    # def generate_carousel_item(self, obj):
    #     return mark_safe(f'<div class="button" onclick="{obj.create_carousel}">Sozdat</div>')


@admin.register(TeamMate)
class TeamMateAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'high_rank', 'show')
    list_display_links = ('name',)
    # list_filter = ('name', 'high_rank', 'show')
    pass


@admin.register(SimpleDocument)
class SimpleDocumentAdmin(TranslatableAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    # list_filter = (('name', SortedRelatedFieldListFilter),)
    pass


@admin.register(ReportDocument)
class ReportDocumentAdmin(TranslatableAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    # list_filter = (('name', SortedRelatedFieldListFilter),)


@admin.register(Carousel)
class CarouselAdmin(TranslatableAdmin):
    list_display = ('id', 'display_name')
    list_display_links = ('display_name',)
    # list_filter = (
    #     ('display_name', SortedRelatedFieldListFilter),
    #     ('position', SortedRelatedFieldListFilter),
    # )


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
