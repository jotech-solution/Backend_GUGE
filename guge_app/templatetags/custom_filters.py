from django import template

register = template.Library()

@register.filter
def get_dict_value(dictionary, key):
    """
    Récupère une valeur d'un dictionnaire en utilisant une clé.
    Utilisation: {{ dict|get_dict_value:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(str(key), '')
    return ''

@register.filter
def is_list(value):
    """
    Vérifie si une valeur est une liste.
    Utilisation: {% if value|is_list %}...{% endif %}
    """
    return isinstance(value, list)


