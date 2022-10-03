from modeltranslation.translator import register, TranslationOptions
from .models import Project, TeamMate, ReportDocument, SimpleDocument, Carousel


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('name', 'content_brief', 'content', 'howto')


@register(TeamMate)
class TeamMateTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(SimpleDocument)
class DocumentTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ReportDocument)
class DocumentTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Carousel)
class CarouselTranslationOptions(TranslationOptions):
    fields = ('display_name', 'content', 'background_image')
