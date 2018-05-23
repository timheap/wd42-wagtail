from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Event


@modeladmin_register
class EventAdmin(ModelAdmin):
    model = Event
    menu_icon = 'date'
    menu_order = 150

    list_display = ['title', 'start_datetime', 'end_datetime']
