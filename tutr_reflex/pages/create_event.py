import reflex as rx
from tutr_reflex.templates.template import template

@template(route="/events/create", title="Create Event")
def create_event() -> rx.Component:
    return rx.container(
    )