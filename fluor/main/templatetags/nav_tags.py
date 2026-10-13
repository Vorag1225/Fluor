from django import template
import main.utils as utils

register = template.Library()

@register.simple_tag
def navpan(request):
    return utils.navpan(request)