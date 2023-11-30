import reflex as rx
from tutr_reflex.state import ClassUpdateState
from tutr_reflex.templates.template import template
from tutr_reflex.components.event_form import event_form

@template(route="/events/[pid]/update", title="Update Event")
def update_event():
    return event_form()

