import reflex as rx
from tutr_reflex.templates.template import template

@template(route="/events/[pid]", title="Event Details")
def event_detail() -> rx.Component:
    return rx.container(
    )