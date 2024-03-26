import logging
from django import template

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag(takes_context=True)
def request_user_can_assign(context, assignable_instance):
    request = context["request"]
    logger.debug(f"Checking if {request.user} can assign {assignable_instance}")
    return assignable_instance.user_can_assign(request.user)
