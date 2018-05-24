import json
from functools import wraps

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel


def auto_clone(init):
    @wraps(init)
    def new_init(self, *args, **kwargs):
        self.constructor_args = args
        self.constructor_kwargs = kwargs
        return init(self, *args, **kwargs)
    return new_init


class LocationPanel(FieldRowPanel):
    template = "edit_handlers/location_panel.html"

    @auto_clone
    def __init__(self, lat_field, lng_field,
                 initial_center=[0, 0], initial_zoom=0, selected_zoom=12,
                 map_options=None, decimal_places=10, **kwargs):

        super().__init__([
            FieldPanel(lat_field),
            FieldPanel(lng_field),
        ], **kwargs)

        self.map_options = map_options or {}
        self.initial_center = initial_center
        self.initial_zoom = initial_zoom
        self.selected_zoom = selected_zoom
        self.decimal_places = decimal_places

    def clone(self):
        return self.__class__(*self.constructor_args, **self.constructor_kwargs)

    def render(self):
        lat_field, lng_field = [child.bound_field for child in self.children]
        return mark_safe(render_to_string(self.template, {
            'panel': self,
            'self': self,
            'lat_field': lat_field,
            'lng_field': lng_field,
        }))

    def id_for_map(self):
        return f"{self.id_for_label()}-map"

    @property
    def js_options(self):
        return mark_safe(json.dumps({
            'initialCenter': self.initial_center,
            'initialZoom': self.initial_zoom,
            'selectedZoom': self.selected_zoom,
            'decimalPlaces': self.decimal_places,
            'mapOptions': self.map_options,
        }))
