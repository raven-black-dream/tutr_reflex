import reflex as rx
from tutr_reflex.templates.template import template
from tutr_reflex.components.event_form import event_form

@template(route="/events/create", title="Create Event")
def create_event() -> rx.Component:
    return event_form()