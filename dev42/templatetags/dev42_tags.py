from django import template
from django.conf import settings
from django.utils.html import format_html

register = template.Library()


@register.simple_tag()
def google_maps_url():
    return format_html('https://maps.googleapis.com/maps/api/js?v=3&key={}', settings.GOOGLE_MAPS_API_KEY)
