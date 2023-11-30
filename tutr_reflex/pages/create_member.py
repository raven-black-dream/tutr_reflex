import reflex as rx
from tutr_reflex.templates.template import template
from tutr_reflex.components.member_form import member_form


@template(route="/members/create", title="Create Member")
def person_create() -> rx.Component:
    return member_form()