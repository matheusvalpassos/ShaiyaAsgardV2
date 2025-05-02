from django import template

register = template.Library()

@register.filter
def add_class(field, css):
    # Verifica se o campo é um BoundField válido
    if not hasattr(field, 'field'):
        return field  # Retorna o campo original se não for válido
    # Obtém classes existentes e combina com a nova
    existing_classes = field.field.widget.attrs.get('class', '')
    combined_classes = f"{existing_classes} {css}".strip()
    return field.as_widget(attrs={"class": combined_classes})