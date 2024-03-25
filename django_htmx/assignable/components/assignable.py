import logging

from django_components import component
from django_components import types as t


logger = logging.getLogger(__name__)


@component.register("assignable")
class Assignable(component.Component):
    def get_context_data(self, assignable_instance):
        return {
            "assignable_instance": assignable_instance,
        }

    template: t.django_html = """
        <div class="card-body">
            <div class="mb-3">
                <label for="assigned-to" class="form-label">Assigned To</label>
                <select id="assigned-to" class="form-select" hx-patch="/assignable/assign-to/{{task.content_type}}/{{task.id}}/">
                    <option value="">Unassigned</option>
                {% for user in assignable_instance.assignable_users %}
                    <option value="{{ user.id }}"{% if assignable_instance.assigned_to == user %} selected="selected"{% endif %}>{{ user.get_full_name }}</option>
                {% endfor %}
                </select>
            </div>
            <div class="mb-3">
            {% if request.user == assignable_instance.assigned_to %}
                <button type="button" class="btn btn-primary float-end" disabled="">Assigned to you <i class="bi bi-person-fill-check"></i></button>
            {% else %}
                <button type="button" class="btn btn-primary float-end" hx-patch="/assignable/assign-to-me/{{task.content_type}}/{{task.id}}/" hx-swap="outerHTML">Assign to me <i class="bi bi-person-raised-hand"></i></button>
            {% endif %}
            </div>
        </div>
    """

    css: t.css = None

    js: t.js = None
