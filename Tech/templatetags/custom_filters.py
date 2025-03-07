from django import template
from datetime import timedelta
import datetime

register = template.Library()

@register.filter
def add_days(value, days):
    """
    Añade un número de días a una fecha o datetime.
    :param value: La fecha o datetime a la que se le añadirán los días.
    :param days: El número de días a añadir.
    :return: La nueva fecha o datetime con los días añadidos.
    """
    if isinstance(value, (datetime.date, datetime.datetime)):
        try:
            # Añadir los días al valor y devolverlo
            return value + timedelta(days=int(days))
        except (ValueError, TypeError):
            return value  # Si days no es un número válido, devolvemos el valor original
    return value  # Si el valor no es una fecha, devolvemos el valor original

@register.filter
def trim(value):
    """Elimina los espacios en blanco al principio y al final de la cadena."""
    if isinstance(value, str):
        return value.strip()
    return value

@register.filter
def split(value, delimiter):
    """ Divide una cadena en una lista usando un delimitador. """
    if isinstance(value, str):
        return value.split(delimiter)
    return value

@register.filter
def multiply(value, arg):
    """Multiplica el valor por un número determinado."""
    try:
        return value * arg
    except (ValueError, TypeError):
        return 0
