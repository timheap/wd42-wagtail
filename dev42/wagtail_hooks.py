from django.templatetags.static import static
from django.utils.html import format_html_join
from wagtail.core import hooks

from dev42.templatetags.dev42_tags import google_maps_url


@hooks.register('insert_global_admin_js')
def admin_js():
    return format_html_join('\n', '<script src="{}"></script>', [
        (static('js/admin.js'),),
        (google_maps_url(),),
    ])
