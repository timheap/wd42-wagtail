from __future__ import absolute_import, unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel)


class ScheduleItem(models.Model):
    title = models.CharField(max_length=255)
    time = models.TimeField()
    speaker = models.CharField(max_length=255, blank=True)

    event = ParentalKey('events.Event', related_name='schedule')

    panels = [
        FieldPanel('time'),
        FieldPanel('title'),
        FieldPanel('speaker'),
    ]

    class Meta:
        ordering = ['time']


class Event(ClusterableModel):
    title = models.CharField(max_length=255)
    start_datetime = models.DateTimeField('Start')
    end_datetime = models.DateTimeField('End')
    signup_link = models.URLField(blank=True)

    panels = [
        FieldPanel('title', classname="full title"),
        MultiFieldPanel([FieldRowPanel([
            FieldPanel('start_datetime', classname='col6'),
            FieldPanel('end_datetime', classname='col6'),
        ])], 'Dates'),
        InlinePanel('schedule', label="Schedule"),
        FieldPanel('signup_link'),
    ]

    def __str__(self):
        return self.title
