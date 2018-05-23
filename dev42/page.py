from django.db import models
from wagtail.core import models as wagtailmodels


class Page(wagtailmodels.Page):
    # Disable the creation of the related field accessor on Page
    # This prevents conflicts with model names and field names
    page_ptr = models.OneToOneField(
        wagtailmodels.Page, parent_link=True, related_name='+',
        on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def get_template(self, request, *args, **kwargs):
        return 'layouts/{meta.app_label}/{meta.model_name}.html'.format(
            meta=self._meta)
