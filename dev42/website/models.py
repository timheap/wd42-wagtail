from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel)
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image

from dev42.edit_handlers import LocationPanel
from dev42.page import Page
from dev42.utils.views import ModelViewProxy

views = ModelViewProxy('dev42.website.views')

COMMON_PANELS = (
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
)


class ContentPage(Page):
    body = RichTextField(blank=True)

    indexed_fields = ('body', )
    search_name = None

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full"),
    ]

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    ]


class Sponsor(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()

    # Must be `null=True, on_delete=models.SET_NULL` to prevent cascading
    # deletion when the image is removed. `blank=False` makes it required when
    # adding/editing it through forms though.
    logo = models.ForeignKey(
        Image, blank=True, null=True, on_delete=models.SET_NULL)

    page = ParentalKey('website.HomePage', related_name='sponsors')

    panels = [
        FieldPanel('title'),
        FieldPanel('link'),
        ImageChooserPanel('logo'),
    ]

    class Meta:
        ordering = ['title']


class HomePage(Page):
    body = RichTextField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    github = models.URLField(blank=True)

    location_link = models.URLField(
        help_text="Link to a map of the event location")
    location_lng = models.DecimalField(max_digits=10, decimal_places=7)
    location_lat = models.DecimalField(max_digits=10, decimal_places=7)

    ical_feed = models.URLField(blank=True)

    serve = views.homepage

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full title"),
        MultiFieldPanel([
            FieldPanel('location_link'),
            LocationPanel(
                'location_lat', 'location_lng',
                initial_center=[-42.87936, 147.32941], initial_zoom=10,
                selected_zoom=15, decimal_places=7),
        ], "Where"),
        MultiFieldPanel([
            FieldPanel('ical_feed'),
        ], "When"),
        MultiFieldPanel([
            FieldPanel('twitter'),
            FieldPanel('facebook'),
            FieldPanel('email'),
            FieldPanel('github'),
        ], "Social media accounts"),
        InlinePanel('sponsors', label="Sponsors"),
    ]
