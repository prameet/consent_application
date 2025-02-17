
from django import template
from django.contrib.auth.decorators import login_required
from django.urls import resolve

from django.views.decorators.http import require_http_methods


register = template.Library()


@register.filter()
def to_int(value):
    """
    This tag is used to convert string value to number.
    :param value:
    :return: integer
    """
    return int(value)

@login_required
@require_http_methods(["GET"])

@register.inclusion_tag("consent_form/consent_form.html")
def consent_form_tag(request, service_id, service, service_access,consent_forms):
    print(consent_forms)
    # print(f"\x1b[31m^^^^^^^^^__request def consent_form_tag : {request}\x1b[0m")
    # print('##### namespace in def weekly_plan_tag : ', resolve(request.path).namespace)
    # r = resolve(request.path)
    # app_name = r.app_name


    return {
        'well_objects': None,
        'consent_forms':consent_forms
    }

