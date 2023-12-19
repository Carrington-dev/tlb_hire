import markdown
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


# @register.inclusion_tag('tutors.html', takes_context=True)
# def show_tutors(context):
#     tutors = NewUser.objects.filter(is_teacher = True)[:3]
#     context['quantity'] = tutors
#     return context

