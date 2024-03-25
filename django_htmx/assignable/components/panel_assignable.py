import logging

from django.contrib.contenttypes.models import ContentType
from django.http import QueryDict
from django_components import component
from django_components import types as t


logger = logging.getLogger(__name__)


@component.register("panel_assignable")
class PanelAssignable(component.Component):
    def get_context_data(self, assignable_instance):
        return {
            "assignable_instance": assignable_instance,
        }

    template: t.django_html = """
        <div class="card-body panel-assignable">
            <div class="mb-3">
                <form id="assign-to" name="assign-to">
                    <input type="hidden" name="action" value="assign_to">
                    <input type="hidden" name="content_type_id" value="{{ assignable_instance.content_type_id }}">
                    <input type="hidden" name="pk" value="{{ assignable_instance.pk }}">            
                    <label for="assigned-to" class="form-label">Assigned To</label>
                    <select id="assigned-to" name="assign_to" class="form-select" hx-patch="/assignable" hx-indicator="#loading-spinner-assign-to" hx-swap="outerHTML" hx-target="closest .panel-assignable">
                        <option value="">Unassigned</option>
                        {% for user in assignable_instance.assignable_users %}
                        <option value="{{ user.pk }}"{% if assignable_instance.assigned_to == user %} selected="selected"{% endif %}>{{ user.get_full_name }}</option>
                        {% endfor %}
                    </select>
                </form>
            </div>
            <div class="mb-3">
                <form id="assign-to-me" name="assign-to-me">
                    <input type="hidden" name="action" value="assign_to_me">
                    <input type="hidden" name="content_type_id" value="{{ assignable_instance.content_type_id }}">
                    <input type="hidden" name="pk" value="{{ assignable_instance.pk }}">
                    {% if request.user == assignable_instance.assigned_to %}
                    <button type="button" class="btn btn-primary float-end" disabled="">Assigned to you <i class="bi bi-person-fill-check"></i></button>
                    {% else %}
                    <button type="button" class="btn btn-primary float-end" hx-patch="/assignable" hx-swap="outerHTML" hx-target="closest .panel-assignable">Assign to me <i class="bi bi-person-raised-hand"></i></button>
                    {% endif %}
                </form>
            </div>
        </div>
    """

    def patch(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        action = data.get("action", None)
        content_type_id = data.get("content_type_id", None)
        pk = data.get("pk", None)

        # TODO add logic to reject request if model is not assignable
        # or if user is not in list of assignable users

        content_type = ContentType.objects.get_for_id(content_type_id)
        assignable_instance = content_type.get_object_for_this_type(pk=pk)

        if action == "assign_to":
            assign_to = data.get("assign_to", None)
            assignable_instance.assigned_to_id = assign_to
        elif action == "assign_to_me":
            assignable_instance.assigned_to = request.user

        assignable_instance.save()

        context = {
            "request": request,
            "assignable_instance": assignable_instance,
        }

        return self.render_to_response(context)
