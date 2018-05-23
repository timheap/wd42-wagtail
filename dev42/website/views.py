import datetime

from django.shortcuts import render

from dev42.events.models import Event


def homepage(request, homepage):

    current_event = Event.objects\
        .filter(start_datetime__gt=datetime.datetime.now())\
        .order_by('start_datetime')\
        .first()

    context = homepage.get_context(request)
    context['current_event'] = current_event
    return render(request, homepage.get_template(request), context)
