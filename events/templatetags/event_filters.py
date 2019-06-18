from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_attendee(context, event):
    return 0 == len(event.event_attendee.filter(attendee=context['request'].user))
