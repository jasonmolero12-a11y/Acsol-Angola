from django import template

from core.models import SiteConfig

register = template.Library()


@register.simple_tag
def acsol_site_config():
    return SiteConfig.objects.first()
