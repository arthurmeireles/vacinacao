from django import template

register = template.Library()


@register.filter(name='add_css_class')
def add_css_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='remove_underline')
def remove_underline(value):
    return value.replace('_', ' ')


@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60

    return '{} dias {} horas {} minutos'.format(days, hours, minutes)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
