import os.path

import wagtail.admin.urls
import wagtail.core.urls
import wagtail.documents.urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from dev42.views import ErrorView

handler500 = ErrorView.as_view(template_name='layouts/500.html', status=500)
handler404 = ErrorView.as_view(template_name='layouts/404.html', status=404)


urlpatterns = [
    path('500/', handler500),
    path('404/', handler404),
    path('admin/', include(wagtail.admin.urls)),
    path('documents/', include(wagtail.documents.urls)),
    path('', include(wagtail.core.urls)),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + 'images/',
        document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
