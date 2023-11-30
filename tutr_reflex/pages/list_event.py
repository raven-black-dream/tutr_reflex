import reflex as rx
from tutr_reflex.templates.template import template


@template(route="/events", title="Event List")
def event_list() -> rx.Component:
    return rx.container(
    )